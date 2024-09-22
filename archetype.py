import json
import os
import subprocess

import requests


def get_metadata(archetype):
    metadata = {
        "casterRation": archetype.get("casterRatio"),
        "casterType": archetype.get("casterType"),
        "classCasterType": archetype.get("classCasterType"),
    }

    table = None

    leveled_table_headers_json = archetype.get("leveledTableHeadersJson")
    if leveled_table_headers_json:
        leveled_table_headers = json.loads(leveled_table_headers_json)
        leveled_table = json.loads(archetype.get("leveledTableJson"))
        table = {"headers": leveled_table_headers, "rows": leveled_table}

    metadata = {k: v for k, v in metadata.items() if v}

    return metadata, table

def convert_to_markdown(archetype):
    markdown = f"""---
obsidianUIMode: preview
tags:
- archetype
aliases: ["{archetype['name']}"]
SourceType: "Archetype"
NoteIcon: archetype
contentSource: {archetype.get('contentSource', 'Unknown Source')}
contentType: {archetype.get('contentType')}
className: {archetype.get('className')}
name: {archetype.get('name')}
"""

    metadata, table = get_metadata(archetype)

    for key, value in metadata.items():
        markdown += f"{key}: {value}\n"

    markdown += "---\n"
    markdown += f"\n**Source:** `=this.contentSource`\n\n"

    markdown += f"\n{archetype.get('text')}\n"

    if table != None:
        markdown += f"\n### The `=this.name`\n\n| {' | '.join(table['headers'])} |\n| {' | '.join(['---' for _ in table['headers']])} |\n"
        for level, row in table["rows"].items():
            markdown += f"| {level} | {' | '.join([cell['Value'] for cell in row])} |\n"

    return markdown


def fetch_archetypes():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/archetype?language=en"
    )
    archetypes = response.json()
    with open("json-files/archetypes.json", "w") as f:
        json.dump(archetypes, f, indent=4)
        print(f"Archetype count: {len(archetypes)}")
    return archetypes


archetype_array = fetch_archetypes()

os.makedirs("CLI/Archetypes", exist_ok=True)

for archetype in archetype_array:
    markdown = convert_to_markdown(archetype)
    with open(f"CLI/Archetypes/{archetype.get('name').replace("/", "")}.md", "w") as f:
        markdown = markdown.replace("\ufffd", ",")
        markdown = markdown.replace("\r\n- ", "\r- ")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
