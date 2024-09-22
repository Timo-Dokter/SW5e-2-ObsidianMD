import json
import os
import subprocess

import requests


def get_metadata(feat):
    metadata = {
        "attributesIncreased": {
            "label": "Ability Score Increase",
            "value": (
                " or ".join(feat.get("attributesIncreased", []))
                if feat.get("attributesIncreased")
                else "-"
            ),
        },
        "prerequisite": {
            "label": "Prerequisite",
            "value": feat.get("prerequisite") if feat.get("prerequisite") else "-",
        },
    }

    return metadata


def convert_to_markdown(feat):
    markdown = f"""---
obsidianUIMode: preview
tags:
- feat
aliases: ["{feat['name']}"]
SourceType: "Feat"
NoteIcon: feat
contentSource: {feat.get('contentSource')}
name: {feat.get('name')}
"""

    metadata = get_metadata(feat)

    for key, value in metadata.items():
        markdown += f"{key}: {value["value"]}\n"

    markdown += "---\n"

    markdown += f"\n**Source:** `=this.contentSource`\n\n"

    for key, value in metadata.items():
        if key == "prerequisite":
            markdown += f"\n_**{value['label']}** `=this.{key}`_\n"
        else:
            markdown += f"**{value["label"]}:** `=this.{key}`\n"

    markdown += f"\n{feat.get('text')}\n"

    return markdown


def fetch_feats():
    response = requests.get("https://sw5eapi.azurewebsites.net/api/Feat?language=en")
    feats = response.json()
    with open("json-files/feats.json", "w") as f:
        json.dump(feats, f, indent=2)
        print(f"Feats count: {len(feats)}")
    return feats


feats = fetch_feats()

os.makedirs("CLI/Feats", exist_ok=True)

for feat in feats:
    markdown = convert_to_markdown(feat)
    with open(f"CLI/Feats/{feat['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", ",")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
