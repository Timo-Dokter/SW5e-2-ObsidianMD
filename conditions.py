import json
import os
import subprocess

import requests


def convert_to_markdown(condition):
    markdown = f"""---
obsidianUIMode: preview
tags:
- condition
aliases: ["{condition['name']}"]
SourceType: "condition"
NoteIcon: condition
contentSource: {condition.get('contentSource')}
contentType: {condition.get('contentType')}
name: {condition.get('name')}
---

**Source:** `=this.contentSource`

{condition.get('description')}
"""

    return markdown


def get_conditions():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/conditions?language=en"
    )
    conditions = response.json()
    for condition in conditions:
        condition["description"] = condition["description"].replace("\\r", "\r")
        condition["description"] = condition["description"].replace("\\n", "\n")
    with open("json-files/conditions.json", "w") as f:
        json.dump(conditions, f)
        print(f"Condition count: {len(conditions)}")
    return conditions


conditions = get_conditions()

os.makedirs("CLI/Conditions", exist_ok=True)

for condition in conditions:
    markdown = convert_to_markdown(condition)
    with open(f"CLI/Conditions/{condition['name']}.md", "w") as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
