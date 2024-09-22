import json
import os
import subprocess

import requests


def convert_force_powers_to_markdown(force_power):
    markdown = f"""---
obsidianUIMode: preview
tags:
- force-power
aliases: ["{force_power['name']}"]
SourceType: "Force Power"
NoteIcon: force-power
contentSource: {force_power.get('contentSource')}
name: {force_power.get('name')}
level: {"At-will" if force_power.get('level') == 0 else force_power.get('level')}
forceAlignment: {force_power.get('forceAlignment')}
castingPeriod: {force_power.get('castingPeriodText')}
range: {force_power.get('range')}
duration: {force_power.get('duration')}
concentration: {"Concentration" if force_power.get('concentration') else "-"}
{f"prerequesite: {force_power.get('prerequisite')}" if force_power.get('prerequisite') else ""}
---

**Source:** `=this.contentSource`

{"_**Prerequisite** `=this.prerequisite`_" if force_power.get('prerequisite') else ""}
**Level:** `=this.level`
**Force Alignment:** `=this.forceAlignment`
**Casting Period:** `=this.castingPeriod`
**Range:** `=this.range`
**Duration:** `=this.duration`
**Concentration:** `=this.concentration`

{force_power.get('description')}
"""

    return markdown


def convert_tech_powers_to_markdown(tech_power):
    markdown = f"""---
obsidianUIMode: preview
tags:
- tech-power
aliases: ["{tech_power['name']}"]
SourceType: "Tech Power"
NoteIcon: tech-power
contentSource: {tech_power.get('contentSource')}
name: {tech_power.get('name')}
level: {"At-will" if tech_power.get('level') == 0 else tech_power.get('level')}
castingPeriod: {tech_power.get('castingPeriodText')}
range: {tech_power.get('range')}
duration: {tech_power.get('duration')}
concentration: {"Concentration" if tech_power.get('concentration') else "-"}
---

**Source:** `=this.contentSource`

**Level:** `=this.level`
**Casting Period:** `=this.castingPeriod`
**Range:** `=this.range`
**Duration:** `=this.duration`
**Concentration:** `=this.concentration`

{tech_power.get('description')}
"""

    return markdown


os.makedirs("CLI/Powers", exist_ok=True)


def fetch_powers():
    response = requests.get("https://sw5eapi.azurewebsites.net/api/power?language=en")
    powers = response.json()

    with open("json-files/powers.json", "w") as f:
        json.dump(powers, f, indent=2)
        print(f"Power count: {len(powers)}")

    for power in powers:
        if power["powerType"] == "Force":
            markdown = convert_force_powers_to_markdown(power)
        else:
            markdown = convert_tech_powers_to_markdown(power)        

        with open(f"CLI/Powers/{power['name'].replace("/", "-")}.md", "w") as f:
            markdown = markdown.replace("\ufffd", ",")
            f.write(markdown)


fetch_powers()

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
