import json
import os
import subprocess

import requests


def get_metadata(species):
    metadata = {
        "name": {"label": "Name", "value": species.get("name")},
        "colorScheme": {
            "label": "Color Scheme",
            "value": species.get("colorScheme"),
            "category": "Visual Characteristics",
        },
        "skinColorOptions": {
            "label": "Skin Color",
            "value": species.get("skinColorOptions"),
            "category": "Visual Characteristics",
        },
        "hairColorOptions": {
            "label": "Hair Color",
            "value": species.get("hairColorOptions"),
            "category": "Visual Characteristics",
        },
        "eyeColorOptions": {
            "label": "Eye Color",
            "value": species.get("eyeColorOptions"),
            "category": "Visual Characteristics",
        },
        "distinctions": {
            "label": "Distinctions",
            "value": species.get("distinctions"),
            "category": "Visual Characteristics",
        },
        "heightAverage": {
            "label": "Height",
            "value": species.get("heightAverage"),
            "category": "Physical Characteristics",
        },
        "heightRollMod": {
            "label": "Height",
            "value": species.get("heightRollMod"),
            "category": "Physical Characteristics",
        },
        "weightAverage": {
            "label": "Weight",
            "value": species.get("weightAverage"),
            "category": "Physical Characteristics",
        },
        "weightRollMod": {
            "label": "Weight",
            "value": species.get("weightRollMod"),
            "category": "Physical Characteristics",
        },
        "homeworld": {
            "label": "Homeworld",
            "value": species.get("homeworld"),
            "category": "Sociocultural Characteristics",
        },
        "manufacturer": {
            "label": "Manufacturer",
            "value": species.get("manufacturer"),
            "category": "Sociocultural Characteristics",
        },
        "language": {
            "label": "Language",
            "value": species.get("language"),
            "category": "Sociocultural Characteristics",
        },
    }

    metadata = {k: v for k, v in metadata.items() if v["value"]}

    return metadata


def get_infobox(metadata):
    infobox = """
> [!infobox]
> # `=this.file.name`
> ###### Visual Characteristics
>  |
> --- | --- |
"""

    for key, value in metadata.items():
        if value.get("category") == "Visual Characteristics":
            infobox += f"> **{value['label']}** | `=this.{key}` |\n"

    infobox += """> ##### Physical Characteristics
>  |
> --- | --- | --- |
> **Height** | `=this.heightAverage` | `=this.heightRollMod` |
> **Weight** | `=this.weightAverage` | `=this.weightRollMod` |
> ##### Sociocultural Characteristics
>  |
> --- | --- |\n"""

    for key, value in metadata.items():
        if value.get("category") == "Sociocultural Characteristics":
            infobox += f"> **{value['label']}** | `=this.{key}` |\n"

    return infobox


def convert_to_markdown(species):
    markdown = f"""---
obsidianUIMode: preview
cssclass: json5e-race
tags:
- race
aliases: ["{species['name']}"]
SourceType: "Race"
NoteIcon: race
contentSource: {species.get('contentSource', 'Unknown Source')}
"""

    metadata = get_metadata(species)

    for key, value in metadata.items():
        markdown += f"{key}: {value['value']}\n"

    markdown += "---\n"
    markdown += f"\n**Source:** `=this.contentSource`\n\n"

    markdown += get_infobox(metadata)

    if species.get("imageUrls"):
        markdown += f"\n![{species['name']}]({species['imageUrls'][0]})\n\n"
    else:
        print(f"No image for {species['name']}")

    markdown += f"\n{species.get('flavorText')}\n"

    markdown += """\n\n### `=this.name` Traits
As a `=this.name`, you have the following special traits.
\n"""

    for trait in species.get("traits"):
        markdown += f"\n**{trait['name']}.** {trait['description']}\n"

    return markdown


def fetch_species():
    response = requests.get("https://sw5eapi.azurewebsites.net/api/species?language=en")
    species = response.json()
    with open("json-files/species.json", "w") as f:
        json.dump(species, f, indent=4)
        print(f"Species count: {len(species)}")
    return species


species_array = fetch_species()

os.makedirs("CLI/Species", exist_ok=True)

for species in species_array:
    markdown = convert_to_markdown(species)
    with open(f"CLI/Species/{species['name']}.md", "w") as f:
        try:
            markdown = markdown.replace("\ufffd", ",")
            f.write(markdown)
        except UnicodeEncodeError as e:
            print(f"Error writing {species['name']}")
            print(e)
        except IndexError as e:
            print(f"Error writing {species['name']}")
            print(e)

# subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
