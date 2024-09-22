import json
import os
import subprocess

import requests


def convert_to_markdown(maneuver):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{maneuver['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {maneuver.get('contentSource')}
contentType: {maneuver.get('contentType')}
name: {maneuver.get('name')}
prerequisite: {maneuver.get('prerequisite')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {maneuver.get('contentSource')}\n"

    markdown += f"_**Prerequisite:**_ {maneuver.get('prerequisite')}\n"

    markdown += f"\n{maneuver.get('description')}\n"

    return markdown


def fetch_maneuvers():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/Maneuvers?language=en"
    )
    maneuvers = response.json()
    with open("json-files/maneuvers.json", "w") as f:
        json.dump(maneuvers, f)
        print(f"Maneuver count: {len(maneuvers)}")
    return maneuvers


maneuvers = fetch_maneuvers()

os.makedirs("CLI/Maneuvers", exist_ok=True)

for maneuver in maneuvers:
    markdown = convert_to_markdown(maneuver)
    with open(
        f"CLI/Maneuvers/{maneuver['rowKey']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
