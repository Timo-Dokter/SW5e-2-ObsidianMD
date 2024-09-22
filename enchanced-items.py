import json
import os
import subprocess

import requests


def get_metadata(item):
    metadata = {
        "type": {"label": "Type", "value": item.get("type")},
        "subtype": {"label": "Subtype", "value": item.get("subtype")},
        "rarity": {"label": "Rarity", "value": item.get("searchableRarity")},
        "prerequisite": {"label": "Prerequisite", "value": item.get("prerequisite")},
        "attunement": {
            "label": "Attunement",
            "value": "No" if item.get("requiresAttunement") is False else "Yes",
        },
    }

    metadata["subtype"]["value"].replace("-", "")
    subtype_list = metadata["subtype"]["value"].split(" ")
    for i, subtype in enumerate(subtype_list):
        if i == 0:
            metadata["subtype"]["value"] = subtype.capitalize()
        else:
            metadata["subtype"]["value"] += f" {subtype.capitalize()}"

    return metadata


def convert_to_markdown(item):
    markdown = f"""---
obsidianUIMode: preview
tags:
- enhanced-item
aliases: ["{item['name']}"]
SourceType: "enhanced-item"
NoteIcon: enhanced-item
contentSource: {item.get('contentSource')}
contentType: {item.get('contentType')}
name: {item.get('name')}
"""

    metadata = get_metadata(item)

    for key, value in metadata.items():
        markdown += f"{value['label']}: {value['value']}\n"

    markdown += f"---\n"
    markdown += f"\n**Source:** `=this.contentSource`\n\n"
    
    for key, value in metadata.items():
        if key == "prerequisite":
            markdown += f"\n_**{value['label']}** `=this.{key}`_\n"
        else:
            markdown += f"\n**{value["label"]}:** `=this.{key}`"

    markdown += f"\n\n{item.get('text')}"

    return markdown


def get_enhanced_items():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/enhancedItem?language=en"
    )
    enhanced_items = response.json()
    with open("json-files/enhanced-items.json", "w") as f:
        json.dump(enhanced_items, f)
        print(f"Enhanced Item count: {len(enhanced_items)}")
    return enhanced_items


enhanced_items = get_enhanced_items()

os.makedirs("CLI/Enhanced Items", exist_ok=True)

for item in enhanced_items:
    markdown = convert_to_markdown(item)
    with open(f"CLI/Enhanced Items/{item['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
