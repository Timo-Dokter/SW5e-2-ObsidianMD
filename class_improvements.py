import json
import os
import subprocess

import requests


def convert_to_markdown(class_improvement):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{class_improvement['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {class_improvement.get('contentSource')}
contentType: {class_improvement.get('contentType')}
name: {class_improvement.get('name')}
prerequisite: {class_improvement.get('prerequisite')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {class_improvement.get('contentSource')}\n"

    markdown += f"_**Prerequisite:** `=this.prerequisite`_\n"
    markdown += f"\n{class_improvement.get('description')}\n"

    return markdown


def fetch_class_improvements():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/ClassImprovement?language=en"
    )
    class_improvements = response.json()
    with open("json-files/class-improvements.json", "w") as f:
        json.dump(class_improvements, f)
        print(f"Class improvement count: {len(class_improvements)}")
    return class_improvements


class_improvements = fetch_class_improvements()

os.makedirs("CLI/Customization Options/Class Improvements", exist_ok=True)

for class_improvement in class_improvements:
    markdown = convert_to_markdown(class_improvement)
    with open(
        f"CLI/Customization Options/Class Improvements/{class_improvement['name']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
