import json
import os
import subprocess

import requests


def convert_to_markdown(lightsaber_form):
    markdown = f"""---
obsidianUIMode: preview
tags:
- customization-option
- class-improvement
aliases: ["{lightsaber_form['name']}"]
SourceType: "Class Improvement"
NoteIcon: class-improvement
contentSource: {lightsaber_form.get('contentSource')}
contentType: {lightsaber_form.get('contentType')}
name: {lightsaber_form.get('name')}
"""

    markdown += "---\n"
    markdown += f"**Source:** {lightsaber_form.get('contentSource')}\n"

    markdown += f"\n{lightsaber_form.get('description')}\n"

    return markdown


def fetch_lightsaber_forms():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/LightsaberForm?language=en"
    )
    lightsaber_forms = response.json()
    with open("json-files/lightsaber-forms.json", "w") as f:
        json.dump(lightsaber_forms, f)
        print(f"Lightsaber form count: {len(lightsaber_forms)}")
    return lightsaber_forms


lightsaber_forms = fetch_lightsaber_forms()

os.makedirs("CLI/Customization Options/Lightsaber Forms", exist_ok=True)

for lightsaber_form in lightsaber_forms:
    markdown = convert_to_markdown(lightsaber_form)
    with open(
        f"CLI/Customization Options/Lightsaber Forms/{lightsaber_form['name']}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
