import json
import os
import re
import subprocess

import requests


def convert_to_markdown(equipment):
    markdown = f"""---
obsidianUIMode: preview
tags:
- starship-equipment
aliases: ["{equipment['name']}"]
SourceType: "Starship Equipment"
NoteIcon: starship-equipment
contentSource: {equipment.get('contentSource')}
contentType: {equipment.get('contentType')}
name: {equipment.get('name')}
type: {equipment.get('type')}
description: "{equipment.get('description')}"
cost: {equipment.get('cost')}
---

**Source:** {equipment.get('contentSource')}

**Cost:** {equipment.get('cost')}

`=this.description`
"""

    return markdown


os.makedirs("CLI/Starship Equipment", exist_ok=True)


def fetch_equipment():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/StarshipEquipment?language=en"
    )
    starship_equipment = response.json()

    with open("json-files/starship-equipment.json", "w") as f:
        json.dump(starship_equipment, f, indent=2)
        print(f"Starship equipment count: {len(starship_equipment)}")

    for table in starship_equipment:
        markdown = convert_to_markdown(table)

        with open(f"CLI/Starship Equipment/{table['name']}.md", "w") as f:
            markdown = markdown.replace("\ufffd", ",")
            markdown = markdown.replace("\r\n", "\r")
            f.write(markdown)


fetch_equipment()


subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
