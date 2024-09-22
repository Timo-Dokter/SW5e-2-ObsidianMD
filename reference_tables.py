import json
import os
import subprocess

import requests


def convert_to_markdown(table):
    markdown = f"""---
obsidianUIMode: preview
tags:
- reference-table
aliases: ["{table['name']}"]
SourceType: "Reference Table"
NoteIcon: reference-table
contentType: {table.get('contentType')}
className: {table.get('className')}
name: {table.get('name')}
---

{table.get('content')}
"""

    return markdown


os.makedirs("CLI/Reference Tables", exist_ok=True)


def fetch_reference_tables():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/ReferenceTable?language=en"
    )
    tables = response.json()

    with open("json-files/tables.json", "w") as f:
        json.dump(tables, f, indent=2)
        print(f"Reference table count: {len(tables)}")

    for table in tables:
        markdown = convert_to_markdown(table)

        with open(f"CLI/Reference Tables/{table['name']}.md", "w") as f:
            markdown = markdown.replace("\ufffd", ",")
            markdown = markdown.replace("\r\n", "\r")
            f.write(markdown)


fetch_reference_tables()

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
