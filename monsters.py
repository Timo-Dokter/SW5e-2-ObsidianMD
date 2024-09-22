import json
import os
import subprocess

import requests

from utils import get_prof_bonus_from_cr


def convert_to_markdown(monster):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{monster['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {monster.get('contentSource')}
contentType: {monster.get('contentType')}
name: {monster.get('name')}
type: {monster.get('types')[0]}
alignment: {monster.get('alignment')}
size: {monster.get('size')}
---

**Source:** `=this.contentSource`

{monster.get('flavorText')}

{monster.get("sectionText")}

```statblock
name: {monster['name']}
size: {monster['size']}
type: {monster['types'][0]}
alignment: {monster['alignment']}
ac: {monster['armorClass']} ({monster['armorType']})
hp: {monster['hitPoints']}
hit_dice: {monster['hitPointRoll']}
speed: {monster['speeds']}
stats: [{monster["strength"]}, {monster["dexterity"]}, {monster["constitution"]}, {monster["intelligence"]}, {monster["wisdom"]}, {monster["charisma"]}]
saves:
"""

    saves = monster.get("savingThrows", [])
    if saves:
        for save in saves:
            save_split = save.split(" +")
            save_name = ""
            if save_split[0] == "Str":
                save_name = "strength"
            elif save_split[0] == "Dex":
                save_name = "dexterity"
            elif save_split[0] == "Con":
                save_name = "constitution"
            elif save_split[0] == "Int":
                save_name = "intelligence"
            elif save_split[0] == "Wis":
                save_name = "wisdom"
            elif save_split[0] == "Cha":
                save_name = "charisma"
            try:
                markdown += f"  - {save_name}: {save_split[1]}\n"
            except IndexError:
                if len(save_name) > 0:
                    bonus = monster[save_name + "Modifier"]
                    markdown += f"  - {save_name}: {bonus + get_prof_bonus_from_cr(int(monster["challengeRating"]))}\n"

    markdown += "skillsaves:\n"

    skills = monster.get("skills", [])
    if skills:
        for skill in skills:
            skill_split = skill.split(" +")
            try:
                markdown += f"  - {skill_split[0].lower()}: {skill_split[1]}\n"
            except IndexError:
                skill_split = skill.split("+")
                markdown += f"  - {skill_split[0].lower()}: {skill_split[1]}\n"

    markdown += f"""damage_vulnerabilities: {",".join(monster.get("damageVulnerabilities", []))}
damage_resistances: {",".join(monster.get("damageResistances", []))}
damage_immunities: {",".join(monster.get("damageImmunities", []))}
condition_immunities: {",".join(monster.get("conditionImmunities", []))}
{"senses: " + ", ".join(monster.get("senses")) if monster.get("senses") else ""}
"""
    languages = monster.get("languages")

    if languages:
        merged_languages = []
        i = 0
        while i < len(languages):
            if languages[i].lower().startswith("glactic basic"):
                languages[i] = "Galactic Basic"
            if i < len(languages) - 1 and languages[i].lower().startswith("underst") and languages[i + 1].lower().startswith("s"):
                merged_languages.append(languages[i] + "and" + languages[i + 1])
                i += 2
            else:
                merged_languages.append(languages[i])
                i += 1
        markdown += f"languages: {', '.join(merged_languages)}\n"

    markdown += f"""cr: {monster.get("challengeRating")}
"""

    behaviors = monster.get("behaviors", [])

    traits = []
    actions = []
    reactions = []
    legendary_actions = []

    for behavior in behaviors:
        if behavior["monsterBehaviorType"] == "Action":
            actions.append(behavior)
        elif behavior["monsterBehaviorType"] == "Reaction":
            reactions.append(behavior)
        elif behavior["monsterBehaviorType"] == "Legendary":
            legendary_actions.append(behavior)
        elif behavior["monsterBehaviorType"] == "Trait":
            traits.append(behavior)
        else:
            print("Unknown behavior type:", behavior["monsterBehaviorType"])

    if traits:
        markdown += "traits:\n"
        for trait in traits:
            markdown += f"""  - name: {trait['name']}
    desc: "{trait['descriptionWithLinks'].replace("\r\n", "\\n - ").replace(f"{trait['name']}. ", "")}"
"""
            
    if actions:
        markdown += "actions:\n"
        for action in actions:
            markdown += f"""  - name: {action['name']}
    desc: "{action['descriptionWithLinks'].replace("\r\n", "\\n - ")}"
"""
            
    if reactions:
        markdown += "reactions:\n"
        for reaction in reactions:
            markdown += f"""  - name: {reaction['name']}
    desc: "{reaction['descriptionWithLinks'].replace("\r\n", "\\n - ")}"
"""
            
    if legendary_actions:
        markdown += "legendary_actions:\n"
        for legendary_action in legendary_actions:
            markdown += f"""  - name: {legendary_action['name']}
    desc: "{legendary_action['descriptionWithLinks'].replace("\r\n", "\\n - ")}"
"""

    return markdown


def fetch_monsters():
    response = requests.get("https://sw5eapi.azurewebsites.net/api/Monster?language=en")
    monsters = response.json()
    with open("json-files/monsters.json", "w") as f:
        json.dump(monsters, f)
        print(f"Monster count: {len(monsters)}")
    return monsters


monsters = fetch_monsters()

os.makedirs("CLI/Monsters", exist_ok=True)

for monster in monsters:
    markdown = convert_to_markdown(monster)
    with open(
        f"CLI/Monsters/{monster['rowKey']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
