# webscrape.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.ncaa.com/march-madness-live/bracket"
r = requests.get(url)

text = r.text
l = text.split('<div class="logo-container" data-v-108f8bd2>')[1:224]
teams = {}
index = 0
counter = 0
div = ['west', 'south', 'east', 'midwest']
for d in div:
    teams[d] = {}

team_list = []
for line in l:
    seed = line.split('<span class="overline color_lvl_-5 " data-v-a92af722 data-v-108f8bd2>')[1][0:2].replace('<', '')
    team = line.split('data-v-2dc29664 data-v-108f8bd2>')[1].split('</p>')[0]
    team_list.append([seed, team])

for d in div:
    for t in team_list[0:16]:

        seed = t[0]
        team = t[1]

        counter += 1

        teams[d][counter] = {
            'seed': seed,
            'team': team
        }

    for i in range(len(team_list[16:])):
        seed = team_list[i+16][0]
        if seed == "/":
            pass
        else:
            start = i + 16
            break
    team_list = team_list[start:]

with open('teams.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(teams, ensure_ascii=False, indent =4))