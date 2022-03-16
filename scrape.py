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

    for line in l[0:]:

        seed = line.split('<span class="overline color_lvl_-5 " data-v-a92af722 data-v-108f8bd2>')[1][0:2].replace('<', '')
        team = line.split('data-v-2dc29664 data-v-108f8bd2>')[1].split('</p>')[0]

        counter += 1

        teams[div[index]][counter] = {
            'seed': seed,
            'team': team
        }

        if counter % 16 == 0:
            index += 1


# with open('test.txt', 'w+') as file:
#     for line in l:
#         file.write(line + "\n___________________________\n")


with open('teams.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(teams, ensure_ascii=False, indent =4))
