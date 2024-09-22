import json
import os
import subprocess

import requests


def convert_to_markdown(base_size):
    markdown = f"""---
obsidianUIMode: preview
tags:
- starship-base-size
aliases: ["{base_size['name']}"]
SourceType: "Starship Base Size"
NoteIcon: starship-base-size
contentSource: {base_size.get('contentSource')}
contentType: {base_size.get('contentType')}
name: {base_size.get('name')}
---

**Source:** {base_size.get('contentSource')}

{base_size.get('fullText')}
"""

    return markdown


os.makedirs("CLI/Starship Base Sizes", exist_ok=True)


def fetch_base_sizes():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/StarshipBaseSize?language=en"
    )
    starship_base_sizes = response.json()

    with open("json-files/starship-base-sizes.json", "w") as f:
        json.dump(starship_base_sizes, f, indent=2)
        print(f"Starship base size count: {len(starship_base_sizes)}")

    for table in starship_base_sizes:
        markdown = convert_to_markdown(table)

        with open(f"CLI/Starship Base Sizes/{table['name']}.md", "w") as f:
            markdown = markdown.replace("\ufffd", ",")
            markdown = markdown.replace("\r\n", "\r")
            f.write(markdown)


fetch_base_sizes()

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
