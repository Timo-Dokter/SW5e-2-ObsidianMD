import json
import os
import subprocess
from pprint import pprint

import requests


def markdown_statblock_to_json(statblock):
    lines = statblock.split("\n")
    lines = [line for line in lines if line.startswith(">")]

    creature_name = lines[0].split("##")[1].strip()

    line_two = lines[1]
    size = line_two.split("*")[1].split(" ")[0]
    type = line_two.split("*")[1].split(" ")[1]
    sub_type_start_index = line_two.split("*")[1].find("(")
    sub_type_end_index = line_two.split("*")[1].find(")")
    if sub_type_start_index == -1 or sub_type_end_index == -1:
        sub_type = None
    else:
        sub_type = line_two.split("*")[1][sub_type_start_index + 1 : sub_type_end_index]
    alignment = line_two.split(",")[1].replace("*", "").strip()

    indices = [i for i, line in enumerate(lines) if "___" in line]
    if len(indices) >= 2:
        first_index = indices[0]
        second_index = indices[1]
        third_index = indices[2]
        fourth_index = indices[3]
    else:
        first_index = None
        second_index = None
        third_index = None
        fourth_index = None

    armor_class_line = lines[first_index + 1]
    armor_class = armor_class_line.split("**")[2].strip().split(" ")[0]
    armor_type = armor_class_line.split("(")[1].split(")")[0]

    hit_points_line = lines[first_index + 2]
    hit_points = hit_points_line.split("**")[2].strip().split(" ")[0]
    hit_point_roll = hit_points_line.split("(")[1].split(")")[0]

    speeds_line = lines[first_index + 3]
    speeds = speeds_line.split("**")[2].strip()

    stat_line = lines[third_index - 1]
    stats = stat_line.split("|")[1:]
    stats = [stat.strip() for stat in stats]
    strength = stats[0].split(" ")[0]
    strength_modifier = stats[0].split(" ")[1]
    dexterity = stats[1].split(" ")[0]
    dexterity_modifier = stats[1].split(" ")[1]
    constitution = stats[2].split(" ")[0]
    constitution_modifier = stats[2].split(" ")[1]
    intelligence = stats[3].split(" ")[0]
    intelligence_modifier = stats[3].split(" ")[1]
    wisdom = stats[4].split(" ")[0]
    wisdom_modifier = stats[4].split(" ")[1]
    charisma = stats[5].split(" ")[0]
    charisma_modifier = stats[5].split(" ")[1]

    saving_throws = []
    skills = []
    damage_immunities = []
    damage_resistances = []
    damage_vulnerabilities = []
    condition_immunities = []
    senses = []
    languages = []
    challenge_rating = None
    information_lines = lines[third_index + 1 : fourth_index]
    for line in information_lines:
        if "Saving Throws" in line:
            saving_throws = line.split("**")[2].split(", ")
            saving_throws = [saving_throw.strip() for saving_throw in saving_throws]
        elif "Skills" in line:
            skills = line.split("**")[2].split(",")
            skills = [skill.strip() for skill in skills]
        elif "Damage Immunities" in line:
            damage_immunities = line.split("**")[2].split(", ")
            damage_immunities = [
                damage_immunity.strip() for damage_immunity in damage_immunities
            ]
        elif "Damage Resistances" in line:
            damage_resistances = line.split("**")[2].split(", ")
            damage_resistances = [
                damage_resistance.strip() for damage_resistance in damage_resistances
            ]
        elif "Damage Vulnerabilities" in line:
            damage_vulnerabilities = line.split("**")[2].split(", ")
            damage_vulnerabilities = [
                damage_vulnerability.strip()
                for damage_vulnerability in damage_vulnerabilities
            ]
        elif "Condition Immunities" in line:
            condition_immunities = line.split("**")[2].split(", ")
            condition_immunities = [
                condition_immunity.strip()
                for condition_immunity in condition_immunities
            ]
        elif "Senses" in line:
            senses = line.split("**")[2].split(", ")
            senses = [sense.strip() for sense in senses]
        elif "Languages" in line:
            languages = line.split("**")[2].split(", ")
            languages = [language.strip() for language in languages]
        elif "Challenge" in line:
            challenge_rating = line.split("**")[2].split(" ")[1]

    behaviors = []
    behavior_lines = lines[fourth_index + 1 :]
    behavior_lines = [line for line in behavior_lines if line.strip() != ">"]
    actions_start_index = None
    reactions_start_index = None
    legendary_actions_start_index = None
    for i, line in enumerate(behavior_lines):
        if "### Actions" in line:
            actions_start_index = i
        elif "### Reactions" in line:
            reactions_start_index = i
        elif "### Legendary Actions" in line:
            legendary_actions_start_index = i

    if actions_start_index is not None:
        trait_lines = behavior_lines[0:actions_start_index]
    elif reactions_start_index is not None:
        trait_lines = behavior_lines[0:reactions_start_index]
    elif legendary_actions_start_index is not None:
        trait_lines = behavior_lines[0:legendary_actions_start_index]
    else:
        trait_lines = behavior_lines[0:]

    last_trait_index = -1

    print(creature_name)

    for i, line in enumerate(trait_lines):
        if (
            line.startswith("> ***")
            or line.startswith(">***")
            or line.startswith(">**")
        ):
            last_trait_index += 1
            try:
                name = line.split("***")[1].strip()
            except IndexError:
                name = line.split("**")[1].strip()
            if "(" in name:
                restrictions = name.split("(")[1].split(")")[0]
            else:
                restrictions = None
            updated_name = name.split("(")[0].strip()

            try:
                description = line.split("***")[2].strip()
            except IndexError:
                description = line.split("**")[2].strip()

            try:
                description_with_links = line.split("***")[2].strip()
            except IndexError:
                description_with_links = line.split("**")[2].strip()

            behavior = {
                "name": updated_name,
                "monsterBehaviorTypeEnum": 1,
                "monsterBehaviorType": "Trait",
                "description": description,
                "descriptionWithLinks": description_with_links,
                "attackTypeEnum": 0,
                "attackType": "None",
                "restrictions": restrictions,
            }
            behaviors.append(behavior)
        else:
            behavior = behaviors[last_trait_index]
            behavior["description"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behavior["descriptionWithLinks"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behaviors[last_trait_index] = behavior

    if actions_start_index is not None:
        if reactions_start_index is not None:
            action_lines = behavior_lines[
                actions_start_index + 1 : reactions_start_index
            ]
        elif legendary_actions_start_index is not None:
            action_lines = behavior_lines[
                actions_start_index + 1 : legendary_actions_start_index
            ]
        else:
            action_lines = behavior_lines[actions_start_index + 1 :]
    else:
        action_lines = []

    last_action_index = last_trait_index
    for i, line in enumerate(action_lines):
        if line.startswith("> **"):
            last_action_index += 1
            try:
                name = line.split("***")[1].strip()
            except IndexError:
                name = line.split("**")[1].strip()
            attack_type = (
                "RangedWeapon"
                if "Ranged Weapon Attack" in line
                else "MeleeWeapon" if "Melee Weapon Attack" in line else "None"
            )
            if "(" in name:
                restrictions = name.split("(")[1].split(")")[0]
            else:
                restrictions = None

            updated_name = name.split("(")[0].strip()

            try:
                description = line.split("***")[2].strip()
            except IndexError:
                description = line.split("**")[2].strip()

            try:
                description_with_links = line.split("***")[2].strip()
            except IndexError:
                description_with_links = line.split("**")[2].strip()

            behavior = {
                "name": updated_name,
                "monsterBehaviorTypeEnum": 2,
                "monsterBehaviorType": "Action",
                "description": description,
                "descriptionWithLinks": description_with_links,
                "attackType": attack_type,
                "restrictions": restrictions,
            }
            behaviors.append(behavior)
        else:
            if line.startswith("> #####"):
                break
            print(line)
            print(len(behaviors), last_action_index)
            behavior = behaviors[last_action_index]
            behavior["description"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behavior["descriptionWithLinks"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behaviors[last_action_index] = behavior

    if reactions_start_index is not None:
        if legendary_actions_start_index is not None:
            reaction_lines = behavior_lines[
                reactions_start_index + 1 : legendary_actions_start_index
            ]
        else:
            reaction_lines = behavior_lines[reactions_start_index + 1 :]
    else:
        reaction_lines = []

    last_reaction_index = last_action_index
    for i, line in enumerate(reaction_lines):
        if line.startswith("> ***"):
            last_reaction_index += 1
            try:
                name = line.split("***")[1].strip()
            except IndexError:
                name = line.split("**")[1].strip()
            if "(" in name:
                restrictions = name.split("(")[1].split(")")[0]
            else:
                restrictions = None
            updated_name = name.split("(")[0].strip()
            behavior = {
                "name": updated_name,
                "monsterBehaviorTypeEnum": 3,
                "monsterBehaviorType": "Reaction",
                "description": line.split("***")[2].strip(),
                "descriptionWithLinks": line.split("***")[2].strip(),
                "attackType": "None",
                "restrictions": restrictions,
            }
        else:
            behavior = behaviors[last_reaction_index]
            behavior["description"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
        behaviors.append(behavior)

    if legendary_actions_start_index is not None:
        legendary_action_lines = behavior_lines[legendary_actions_start_index + 1 :]
    else:
        legendary_action_lines = []

    last_legendary_action_index = last_reaction_index

    for i, line in enumerate(legendary_action_lines):
        if line.startswith("> **"):
            last_legendary_action_index += 1
            name = line.split("**")[1].strip()
            if "(" in name:
                restrictions = name.split("(")[1].split(")")[0]
            else:
                restrictions = None
            updated_name = name.split("(")[0].strip()
            behavior = {
                "name": updated_name,
                "monsterBehaviorTypeEnum": 4,
                "monsterBehaviorType": "Legendary",
                "description": line.split("**")[2].strip(),
                "descriptionWithLinks": line.split("**")[2].strip(),
                "attackType": "None",
                "restrictions": restrictions,
            }
            behaviors.append(behavior)
        else:
            behavior = behaviors[last_legendary_action_index]
            behavior["description"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behavior["descriptionWithLinks"] += (
                "\r\n" + line.strip()[1:].replace("<br>", "").strip()
            )
            behaviors[last_legendary_action_index] = behavior

    return {
        "name": creature_name,
        "flavorText": "",
        "sectionText": "",
        "size": size,
        "type": type,
        "subtype": sub_type,
        "alignment": alignment,
        "armorClass": armor_class,
        "armorType": armor_type,
        "hitPoints": hit_points,
        "hitPointRoll": hit_point_roll,
        "speeds": speeds,
        "strengthModifier": strength_modifier,
        "strength": strength,
        "dexterityModifier": dexterity_modifier,
        "dexterity": dexterity,
        "constitutionModifier": constitution_modifier,
        "constitution": constitution,
        "intelligenceModifier": intelligence_modifier,
        "intelligence": intelligence,
        "wisdomModifier": wisdom_modifier,
        "wisdom": wisdom,
        "charismaModifier": charisma_modifier,
        "charisma": charisma,
        "savingThrows": saving_throws,
        "skills": skills,
        "damageImmunities": damage_immunities,
        "damageResistances": damage_resistances,
        "damageVulnerabilities": damage_vulnerabilities,
        "conditionImmunities": condition_immunities,
        "senses": senses,
        "languages": languages,
        "challengeRating": challenge_rating,
        "behaviors": behaviors,
        "imageUrls": [],
    }


def get_markdown_stats(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


response = requests.get(
    "https://www.gmbinder.com/share/-MUJMn6W1EWr0m_Pzmzr/-MWPrPm_32vTvBXjaEmN/source"
)
response.raise_for_status()
markdown = response.text


first_stat_block_start_index = markdown.find("> ##")
markdown = markdown[first_stat_block_start_index:]
markdown = markdown.split("<style>")[0]

with open("markdown_file.md", "w", encoding="utf-8") as f:
    f.write(markdown)


statblock_array = markdown.split("\r\n")
statblock_array = [statblock for statblock in statblock_array if statblock.strip()]
statblock_array = [
    statblock for statblock in statblock_array if "\\pagebreakNum" not in statblock
]

markdown_statblocks = []

last_index = 0
just_updated_index = False
for line in statblock_array:
    if line == "___" and not just_updated_index:
        last_index += 1
        just_updated_index = True
    else:
        just_updated_index = False
        try:
            markdown_statblocks[last_index] = (
                markdown_statblocks[last_index] + "\n" + line
            )
        except IndexError:
            markdown_statblocks.append(line)

with open("statblock_array.json", "w", encoding="utf-8") as json_file:
    json.dump(markdown_statblocks, json_file, indent=4)

sv2_monsters_json = []
for statblock in markdown_statblocks:
    sv2_monsters_json.append(markdown_statblock_to_json(statblock))

with open("sv2_monsters.json", "w", encoding="utf-8") as json_file:
    json.dump(sv2_monsters_json, json_file, indent=4)
