import json
import os
import subprocess

import requests


def add_spaces_to_camel_case(text):
    return "".join([" " + char if char.isupper() else char for char in text]).strip()


def convert_weapon_to_markdown(weapon):
    markdown = f"""---
obsidianUIMode: preview
tags:
- equipment
- weapon
aliases: ["{weapon['name']}"]
SourceType: "equipment"
NoteIcon: weapon
contentSource: {weapon.get('contentSource', '')}
contentType: {weapon.get('contentType', '')}
name: {weapon.get('name')}
cost: {weapon.get('cost')}
weight: {weapon.get('weight')}
type: {add_spaces_to_camel_case(weapon.get('weaponClassification', ''))}
numberOfDamageDice: {weapon.get('damageNumberOfDice')}
damageDieType: {weapon.get('damageDieType')}
damageType: {weapon.get('damageType', '')}
"""

    properties = weapon.get("properties")
    if properties:
        markdown += "properties:\n"
        for property in properties:
            markdown += f"- {property.capitalize()}\n"

    markdown += f"""---

**Source:** `=this.contentSource`
    
**Type:** `=this.type`
**Properties:** `=this.properties`
**Cost:** `=this.cost`
**Weight:** `=this.weight`
**Damage:** `=this.numberOfDamageDice`d`=this.damageDieType` `=this.damageType`"""

    description = weapon.get("description")

    if description:
        markdown += f"\n\n{description}"

    return markdown


def convert_armor_to_markdown(armor):
    markdown = f"""---
obsidianUIMode: preview
tags:
- equipment
- armor
aliases: ["{armor['name']}"]
SourceType: "equipment"
NoteIcon: armor
contentSource: {armor.get('contentSource', '')}
contentType: {armor.get('contentType', '')}
name: {armor.get('name')}
cost: {armor.get('cost')}
weight: {armor.get('weight')}
armorClass: {armor.get('ac')}
stealthDisadvantage: {"Disadvantage" if armor.get('stealthDisadvantage') else "-"}
type: {add_spaces_to_camel_case(armor.get('armorClassification', ''))}
"""

    properties = armor.get("properties")

    if properties:
        markdown += "properties:\n"
        for property in properties:
            markdown += f"- {property.capitalize()}\n"

    markdown += f"""---

**Source:** `=this.contentSource`

**Type:** `=this.type`
**Properties:** `=this.properties`
**Cost:** `=this.cost`
**Weight:** `=this.weight`
**Armor Class:** `=this.armorClass`
**Stealth Disadvantage:** `=this.stealthDisadvantage`"""

    description = armor.get("description")

    if description:
        markdown += f"\n\n{description}"

    return markdown


def convert_gear_to_markdown(gear):
    markdown = f"""---
obsidianUIMode: preview
tags:
- equipment
- adventuring gear
aliases: ["{gear['name']}"]
SourceType: "equipment"
NoteIcon: adventuring gear
contentSource: {gear.get('contentSource', '')}
contentType: {gear.get('contentType', '')}
name: {gear.get('name')}
category: {add_spaces_to_camel_case(gear.get('equipmentCategory', ''))}
cost: {gear.get('cost')}
weight: {gear.get('weight')}
---

**Source:** `=this.contentSource`

**Category:** `=this.category`
**Cost:** `=this.cost`
**Weight:** `=this.weight`"""

    description = gear.get("description")

    if description:
        markdown += f"\n\n{description}"

    return markdown


def get_equipment():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/equipment?language=en"
    )
    equipment_items = response.json()
    weapons = []
    armor = []
    adventuring_gear = []
    for item in equipment_items:
        if item["equipmentCategory"] == "Weapon":
            weapons.append(item)
        elif item["equipmentCategory"] == "Armor":
            armor.append(item)
        else:
            adventuring_gear.append(item)

    with open("json-files/weapons.json", "w") as f:
        json.dump(weapons, f)
        print(f"Weapon count: {len(weapons)}")
    with open("json-files/armor.json", "w") as f:
        json.dump(armor, f)
        print(f"Armor count: {len(armor)}")
    with open("json-files/adventuring_gear.json", "w") as f:
        json.dump(adventuring_gear, f)
        print(f"Adventuring Gear count: {len(adventuring_gear)}")

    return weapons, armor, adventuring_gear


weapons, armor, adventuring_gear = get_equipment()

os.makedirs("CLI/Weapons", exist_ok=True)
os.makedirs("CLI/Armor", exist_ok=True)
os.makedirs("CLI/Adventuring Gear", exist_ok=True)

for weapon in weapons:
    markdown = convert_weapon_to_markdown(weapon)
    with open(f"CLI/Weapons/{weapon['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

for armor_piece in armor:
    markdown = convert_armor_to_markdown(armor_piece)
    with open(f"CLI/Armor/{armor_piece['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

for item in adventuring_gear:
    markdown = convert_gear_to_markdown(item)
    with open(f"CLI/Adventuring Gear/{item['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
