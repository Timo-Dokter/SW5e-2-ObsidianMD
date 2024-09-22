import json
import os
import subprocess

import requests


def convert_to_markdown(fighting_style):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{fighting_style['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {fighting_style.get('contentSource')}
contentType: {fighting_style.get('contentType')}
name: {fighting_style.get('name')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {fighting_style.get('contentSource')}\n"

    markdown += f"\n{fighting_style.get('description')}\n"

    return markdown


def fetch_fighting_styles():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/FightingStyle?language=en"
    )
    fighting_styles = response.json()
    with open("json-files/fighting-styles.json", "w") as f:
        json.dump(fighting_styles, f)
        print(f"Fighting Style count: {len(fighting_styles)}")
    return fighting_styles


fighting_styles = fetch_fighting_styles()

os.makedirs("CLI/Customization Options/Fighting Styles", exist_ok=True)

for fighting_style in fighting_styles:
    markdown = convert_to_markdown(fighting_style)
    with open(
        f"CLI/Customization Options/Fighting Styles/{fighting_style['name']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
