import json
import os
import subprocess

import requests


def convert_to_markdown(fighting_mastery):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{fighting_mastery['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {fighting_mastery.get('contentSource')}
contentType: {fighting_mastery.get('contentType')}
name: {fighting_mastery.get('name')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {fighting_mastery.get('contentSource')}\n"

    markdown += f"\n{fighting_mastery.get('text')}\n"

    return markdown


def fetch_fighting_masteries():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/FightingMastery?language=en"
    )
    fighting_masteries = response.json()
    with open("json-files/fighting-masteries.json", "w") as f:
        json.dump(fighting_masteries, f)
        print(f"Fighting Mastery count: {len(fighting_masteries)}")
    return fighting_masteries


fighting_masteries = fetch_fighting_masteries()

os.makedirs("CLI/Customization Options/Fighting Masteries", exist_ok=True)

for fighting_mastery in fighting_masteries:
    markdown = convert_to_markdown(fighting_mastery)
    with open(
        f"CLI/Customization Options/Fighting Masteries/{fighting_mastery['name']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
