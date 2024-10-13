import json
import os
import subprocess

import requests


def convert_to_markdown(deployment):
    markdown = f"""---
obsidianUIMode: preview
tags:
- starship-deployment
aliases: ["{deployment['name']}"]
SourceType: "Starship Deployment"
NoteIcon: starship-deployment
contentSource: {deployment.get('contentSource')}
contentType: {deployment.get('contentType')}
name: {deployment.get('name')}
description: "{deployment.get('description')}"
---

**Source:** {deployment.get('contentSource')}

{deployment.get('featureText')}
"""

    return markdown


os.makedirs("CLI/Starship Deployments", exist_ok=True)


def fetch_deployments():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/StarshipDeployment?language=en"
    )
    starship_deployments = response.json()

    with open("json-files/starship-deployments.json", "w") as f:
        json.dump(starship_deployments, f, indent=2)
        print(f"Starship deployment count: {len(starship_deployments)}")

    for table in starship_deployments:
        markdown = convert_to_markdown(table)

        with open(f"CLI/Starship Deployments/{table['name']}.md", "w") as f:
            markdown = markdown.replace("\ufffd", ",")
            markdown = markdown.replace("\r\n", "\r")
            f.write(markdown)


fetch_deployments()

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
