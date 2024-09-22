import json
import os
import subprocess

import requests


def convert_to_markdown(multi_class_improvement):
    markdown = f"""---
obsidianUIMode: preview
tags:
- multi-class-improvement
aliases: ["{multi_class_improvement['name']}"]
SourceType: "Multi-Class Improvement
NoteIcon: multi-class-improvement
contentSource: {multi_class_improvement.get('contentSource')}
contentType: {multi_class_improvement.get('contentType')}
name: {multi_class_improvement.get('name')}
prerequisite: {multi_class_improvement.get('prerequisite')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {multi_class_improvement.get('contentSource')}\n"

    markdown += f"_**Prerequisite:** `=this.prerequisite`_\n"
    markdown += f"\n{multi_class_improvement.get('description')}\n"

    return markdown


def fetch_multi_class_improvements():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/MulticlassImprovement?language=en"
    )
    multi_class_improvements = response.json()
    with open("json-files/multiclass-improvements.json", "w") as f:
        json.dump(multi_class_improvements, f)
        print(f"Multiclass Improvements count: {len(multi_class_improvements)}")
    return multi_class_improvements


multi_class_improvements = fetch_multi_class_improvements()

os.makedirs("CLI/Customization Options/Multiclass Improvements", exist_ok=True)

for multi_class_improvement in multi_class_improvements:
    markdown = convert_to_markdown(multi_class_improvement)
    with open(
        f"CLI/Customization Options/Multiclass Improvements/{multi_class_improvement['name']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
