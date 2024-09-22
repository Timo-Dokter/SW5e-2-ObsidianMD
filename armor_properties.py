import json
import os
import subprocess

import requests


def get_metadata(property):
    pass

def convert_to_markdown(property):
    markdown = f"""---
obsidianUIMode: preview
tags:
- property
aliases: ["{property['name']}"]
SourceType: "Property"
NoteIcon: property
contentSource: {property.get('contentSource')}
contentType: {property.get('contentType')}
name: {property.get('name')}
---

**Source:** `=this.contentSource`

{property.get('content')}
"""
    
    return markdown

def fetch_armor_properties():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/ArmorProperty?language=en"
    )
    properties = response.json()
    with open("json-files/armor_properties.json", "w") as f:
        json.dump(properties, f, indent=2)
        print(f"Armor Property count: {len(properties)}")
    return properties

armor_properties = fetch_armor_properties()

os.makedirs("CLI/Armor Properties", exist_ok=True)

for property in armor_properties:
    markdown = convert_to_markdown(property)
    with open(f"CLI/Armor Properties/{property.get('name').replace("/", "")}.md", "w") as f:
        markdown = markdown.replace("\ufffd", ",")
        f.write(markdown)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
