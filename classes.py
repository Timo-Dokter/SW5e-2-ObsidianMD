import json
import os
import subprocess

import requests


def get_metadata(class_):
    metadata = {
        "hitDiceDieType": class_.get("hitDiceDieType"),
        "hitPointsAtFirstLevel": class_.get("hitPointsAtFirstLevel"),
        "hitPointsAtHigherLevels": class_.get("hitPointsAtHigherLevels"),
        "armorProficiencies": class_.get("armorProficiencies"),
        "weaponProficiencies": class_.get("weaponProficiencies"),
        "toolProficiencies": class_.get("toolProficiencies"),
        "savingThrows": class_.get("savingThrows"),
        "skillChoices": class_.get("skillChoices"),
        "skillChoicesList": class_.get("skillChoicesList"),
        "equipmentLines": class_.get("equipmentLines"),
        "startingWealthVariant": class_.get("startingWealthVariant"),
        "archetypeFlavorName": class_.get("archetypeFlavorName"),
    }

    metadata = {k: v for k, v in metadata.items() if v}

    table = None

    level_change_headers_json = class_.get("levelChangeHeadersJson")
    if level_change_headers_json:
        level_change_headers = json.loads(level_change_headers_json)
        level_change_table = class_.get("levelChanges")
        table = {"headers": level_change_headers, "rows": level_change_table}

    return metadata, table


def convert_to_markdown(class_):
    markdown = f"""---
obsidianUIMode: preview
tags:
- class
aliases: ["{class_['name']}"]
SourceType: "class"
NoteIcon: class
contentSource: {class_.get('contentSource')}
contentType: {class_.get('contentType')}
name: {class_.get('name')}
"""

    metadata, table = get_metadata(class_)

    for key, value in metadata.items():
        markdown += f"{key}: {value}\n"

    markdown += "---\n"
    markdown += f"**Source:** {class_.get('contentSource')}\n"

    images = class_.get("imageUrls")
    for image in images:
        markdown += f"![]({image})\n"

    markdown += f"\n{class_.get('flavorText')}\n"
    markdown += f"\n{class_.get('creatingText')}\n"
    markdown += f"\n#### Quick Build\n"
    markdown += f"\n{class_.get('quickBuildText')}\n"

    if table != None:
        markdown += f"\n### The `=this.name`\n\n| {' | '.join(table['headers'])} |\n| {' | '.join(['---' for _ in table['headers']])} |\n"
        for level, row_data in table["rows"].items():
            markdown += "|"
            for key, value in row_data.items():
                value.replace("\ufffd", "-")
                markdown += f"{value} |"
            markdown += "\n"

    markdown += f"""
#### Class Features
As a `=this.name`, you gain the following class features.

###### Hit Points
**Hit Dice:** 1d`=this.hitDiceDieType` per `=this.name` level
**Hit Points at 1st Level:** `=this.hitPointsAtFirstLevel`
**Hit Points at Higher Levels:** `=this.hitPointsAtHigherLevels`

###### Proficiencies
**Armor:** `=this.armorProficiencies`
**Weapons:** `=this.weaponProficiencies`
**Tools:** `=this.toolProficiencies`

**Saving Throws:** `=this.savingThrows`
**Skills:** `=this.skillChoices`

###### Equipment
You start with the following equipment, in addition to the equipment granted by your background
"""

    for equipment in class_.get("equipmentLines"):
        markdown += f"{equipment}\n"

    markdown += f"""###### Variant: Starting Wealth
In lieu of the equipment granted by your class and background, you can elect to purchase your starting gear. If you do so, you receive no equipment from your class and background, and instead roll for your starting wealth using the criteria below:

| Class | Funds |
|-------|-------|
| `=this.name` | `=this.startingWealthVariant` |

{class_.get('classFeatureText')}

### `=this.archetypeFlavorName`

```dataview
TABLE WITHOUT ID file.link as Name, contentSource as Source, casterType as "Caster Type"
FROM #archetype
WHERE className=this.file.name
SORT file.name
```
"""

    return markdown


def fetch_classes():
    response = requests.get("https://sw5eapi.azurewebsites.net/api/class?language=en")
    classes = response.json()
    with open("json-files/classes.json", "w") as f:
        json.dump(classes, f)
        print(f"Class count: {len(classes)}")
    return classes


classes = fetch_classes()

os.makedirs("CLI/Classes", exist_ok=True)

for class_ in classes:
    markdown = convert_to_markdown(class_)
    with open(f"CLI/Classes/{class_['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
