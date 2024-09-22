import json
import os
import subprocess

import requests


def convert_to_markdown(expanded_content):
    markdown = f"""---"""

    return markdown


def get_content():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/ExpandedContent?language=en"
    )
    expanded_content = response.json()
    with open("json-files/expanded_content.json", "w") as f:
        json.dump(expanded_content, f, indent=2)
        print(f"Expanded Content count: {len(expanded_content)}")
    return expanded_content


content = get_content()

os.makedirs("CLI/Expanded Content", exist_ok=True)

for expanded_content in content:
    markdown = """---
obsidianUIMode: preview
---

"""
    markdown += expanded_content["contentMarkdown"]
    with open(
        f"CLI/Expanded Content/{expanded_content.get('chapterName')}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        markdown = markdown.replace("||\r\n", "|\r")
        markdown = markdown.replace("\r\n", "\r")
        if expanded_content.get("chapterName") == "Archetypes":
            markdown = markdown.replace(
                "\r\r|",
                "\r\r||",
            )
            markdown = markdown.replace(
                "\r\r|||",
                "\r\r||",
            )
        elif expanded_content.get("chapterName") == "Enhanced Items":
            markdown = markdown.replace("|   |   |\r", "|   |\r")
        elif expanded_content.get("chapterName") == "Equipment":
            markdown = markdown.replace("|||\r", "||\r")
            markdown = markdown.replace("\u2014", "-")
        markdown = markdown.replace("|--:|", "|")
        markdown = markdown.replace(
            "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;", ""
        )
        markdown = markdown.replace("&emsp;&nbsp;&nbsp;", "")
        markdown = markdown.replace("&emsp;&emsp;&emsp;", "")
        markdown = markdown.replace("&emsp;&emsp;", "")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
