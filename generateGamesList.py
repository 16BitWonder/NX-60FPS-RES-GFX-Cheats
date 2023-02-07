import os
import urllib.request, urllib.parse
import json

response = urllib.request.urlopen(
    'https://raw.githubusercontent.com/HamletDuFromage/switch-cheats-db/master/versions.json')
allVersions = json.load(response)

table = """# Games List
A list of all games with cheats. Games with a 🟢 have cheats available for the latest version, and games with a 🔴 do not.

The database currently contains {numCheats} cheat files for {numTitles} titles, of which {numCheatsWithLatest} have cheats for the latest version.

| No | NAME | TITLE ID | BUILD ID | VERSION |
| --- | --- | --- | --- | --- |
"""

numCheats = 0
numCheatsWithLatest = 0
tableItems = []

for title in os.listdir("titles"):
    latestHasCheats = "🔴"
    cheats = [file.removesuffix(".txt") for file in os.listdir(os.path.join("titles", title, "cheats"))]
    names = [file.removesuffix(".txt") for file in os.listdir(os.path.join("titles", title)) if file.endswith(".txt")]
    if len(names) != 0:
        name = names[0]
    else:
        name = "Unknown"
    if(not title in allVersions):
        # print(f"Missing version information for {title}")
        versions = []
    else:
        versions = [version for version in allVersions[title].items() if version[1] in cheats]
        versions.sort(key=lambda x: int(x[0]))
        latest = [version[1] for version in allVersions[title].items() if version[0] == 'latest'] 
        if len(latest) > 0:
            latest = [version[1] for version in allVersions[title].items() if version[0] == str(latest[0])]
            if(len(latest) > 0 and latest[0] in cheats):
                latestHasCheats = "🟢"
                numCheatsWithLatest += 1
    
    # Add any cheats that don't have a version to the end of the list
    versions += [(-1, cheat) for cheat in cheats if cheat not in [version[1] for version in versions]]

    cheatsLinked = [f"[{version[1]}](titles/{title}/cheats/{version[1]}.txt)" for version in versions]
    versionsLinked = [f"[{version[0]}](titles/{title}/cheats/{version[1]}.txt)" for version in versions if version[0] != -1]

    nameLink = urllib.parse.quote(f"titles/{title}/{name}.txt")
    tableItems.append(f"[{name}]({nameLink}) | [{title}](titles/{title}) | {', '.join(cheatsLinked)} | {', '.join(versionsLinked)} {latestHasCheats}| ")
    numCheats += len(cheats)

table = table.replace("{numCheats}", str(numCheats))
table = table.replace("{numTitles}", str(len(tableItems)))
table = table.replace("{numCheatsWithLatest}", str(numCheatsWithLatest))

tableItems.sort(key=str.lower)
table += "\n".join([f"| {i+1} | {item}" for i, item in enumerate(tableItems)])

if(os.path.exists("GAMES.md")):
    existingGames = open("GAMES.md", "r", encoding="utf-16").read()
    if existingGames != table:
        open("GAMES.md", "w", encoding="utf-16").write(table)
        print("true")
    else:
        print("false")
else:
    open("GAMES.md", "w", encoding="utf-16").write(table)
    print("true")
