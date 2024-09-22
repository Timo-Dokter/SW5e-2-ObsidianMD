import json
import os
import subprocess

import requests


def get_metadata(background):
    metadata= {
        "skillProficiencies": {"label": "Skill Proficiencies", "value": background.get("skillProficiencies")},
        "toolProficiencies": {"label": "Tool Proficiencies", "value": background.get("toolProficiencies")},
        "languages": {"label": "Languages", "value": background.get("languages")},
        "equipment": {"label": "Equipment", "value": background.get("equipment")},
    }

    metadata = {k: v for k, v in metadata.items() if v}

    return metadata


def convert_to_markdown(background):
    markdown = f"""---
obsidianUIMode: preview
tags:
- background
aliases: ["{background['name']}"]
SourceType: "Background"
NoteIcon: background
contentSource: {background.get('contentSource', 'Unknown Source')}
contentType: {background.get('contentType')}
className: {background.get('className')}
name: {background.get('name')}
"""
    
    metadata = get_metadata(background)

    for key, value in metadata.items():
        markdown += f"{key}: {value["value"]}\n"

    markdown += "---\n"
    markdown += f"\n**Source:** `=this.contentSource`\n\n"

    markdown += f"\n{background.get('flavorText')}\n"

    for key, value in metadata.items():
        markdown += f"\n**{value["label"]}:** `=this.{key}`"

    markdown += f"""\n### Feature: {background.get('featureName')}
{background.get('featureText')}
### Background Feat\n
| d8 | Feat |
| --- | --- |
"""

    feat_options = background.get("featOptions")

    for feat_option in feat_options:
        markdown += f"| {feat_option['roll']} | {feat_option['name']} |\n"

    markdown += f"""\n### Suggested Characteristics\n\n
{background.get('suggestedCharacteristics')}\n
| d8 | Personality Trait |
| --- | --- |
"""
    
    personality_traits = background.get("personalityTraitOptions")

    for personality_trait in personality_traits:    
        markdown += f"| {personality_trait['roll']} | {personality_trait['description']} |\n"

    markdown += f"""\n| d6 | Ideal |
| --- | --- |
"""
    
    ideals = background.get("idealOptions")

    for ideal in ideals:
        markdown += f"| {ideal['roll']} | {ideal['description']} |\n"

    markdown += f"""\n| d6 | Bond |
| --- | --- |
"""

    bonds = background.get("bondOptions")

    for bond in bonds:
        markdown += f"| {bond['roll']} | {bond['description']} |\n"

    markdown += f"""\n| d6 | Flaw |
| --- | --- |
"""
    
    flaws = background.get("flawOptions")

    for flaw in flaws:
        markdown += f"| {flaw['roll']} | {flaw['description']} |\n"

    return markdown



def fetch_backgrounds():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/background?language=en"
    )
    backgrounds = response.json()
    with open("json-files/backgrounds.json", "w") as f:
        json.dump(backgrounds, f, indent=2)
        print(f"Background count: {len(backgrounds)}")
    return backgrounds

backgrounds = fetch_backgrounds()

os.makedirs("CLI/Backgrounds", exist_ok=True)

for background in backgrounds:
    markdown = convert_to_markdown(background)
    with open(f"CLI/Backgrounds/{background.get('name').replace("/", "")}.md", "w") as f:
        markdown = markdown.replace("\ufffd", ",")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
