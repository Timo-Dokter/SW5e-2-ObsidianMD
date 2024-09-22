import json
import os
import subprocess

import requests


def convert_to_markdown(player_handbook_chapter):
    markdown = f"""---
obsidianUIMode: preview
tags:
- player-handbook
aliases: ["{player_handbook_chapter['chapterName']}"]
SourceType: "Player Handbook"
NoteIcon: player-handbook
contentSource: {player_handbook_chapter.get('contentSource')}
contentType: {player_handbook_chapter.get('contentType')}
chapterNumber: {player_handbook_chapter.get('chapterNumber')}
chapterName: {player_handbook_chapter.get('chapterName')}
---

{player_handbook_chapter.get('contentMarkdown')}
"""

    return markdown


def fetch_player_handbook_chapters():
    response = requests.get(
        "https://sw5eapi.azurewebsites.net/api/playerHandbookRule?language=en"
    )
    player_handbook_chapters = response.json()
    with open("json-files/player-handbook-chapters.json", "w") as f:
        json.dump(player_handbook_chapters, f)
        print(f"Player Handbook Chapters count: {len(player_handbook_chapters)}")
    return player_handbook_chapters


player_handbook_chapters = fetch_player_handbook_chapters()

os.makedirs("CLI/Rules/Player Handbook", exist_ok=True)

for player_handbook_chapter in player_handbook_chapters:
    if player_handbook_chapter["contentMarkdown"] == "":
        continue
    markdown = convert_to_markdown(player_handbook_chapter)
    markdown = markdown.replace(f"# Chapter {player_handbook_chapter["chapterNumber"]}: {player_handbook_chapter['chapterName']}\r\n\r\n", "")
    markdown = markdown.replace(f"# {player_handbook_chapter['chapterName']}\r\n\r\n", "")

    with open(
        f"CLI/Rules/Player Handbook/Chapter {player_handbook_chapter["chapterNumber"]} - {player_handbook_chapter['chapterName'].replace(":", "")}.md",
        "w",
    ) as f:
        markdown = markdown.replace("\ufffd", "-")
        f.write(markdown)

subprocess.run(["npx", "prettier", "**/*.md", "--write"], shell=True)
