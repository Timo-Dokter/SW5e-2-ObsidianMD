import json
import os
import subprocess

import requests


def convert_to_markdown(improvement):
    markdown = f"""---
obsidianUIMode: preview
tags:
- splash-class-improvement
aliases: ["{improvement['name']}"]
SourceType: "Splash Class Improvement
NoteIcon: splash-class-improvement
contentSource: {improvement.get('contentSource')}
contentType: {improvement.get('contentType')}
name: {improvement.get('name')}
prerequisite: {improvement.get('prerequisite')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {improvement.get('contentSource')}\n"

    markdown += f"_**Prerequisite:** `=this.prerequisite`_\n"
    markdown += f"\n{improvement.get('description')}\n"

    return markdown


os.makedirs("CLI/Customization Options/Splash Class Improvements", exist_ok=True)


def fetch_improvements():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/SplashclassImprovement?language=en"
    )
    improvements = response.json()
    with open("json-files/splash-class-improvements.json", "w") as f:
        json.dump(improvements, f)
        print(f"Splash Class Improvements count: {len(improvements)}")

    for improvement in improvements:
        markdown = convert_to_markdown(improvement)
        with open(
            f"CLI/Customization Options/Splash Class Improvements/{improvement['name']}.md",
            "w",
        ) as f:
            markdown = markdown.replace("\ufffd", "-")
            f.write(markdown)


fetch_improvements()

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
