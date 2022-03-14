# webscrape.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

year = 2021

def scrape(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  
    
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll('tr')[1:]

    stats = {}
    for i in range(len(rows)):
        tds = rows[i].findAll("td")
        if len(tds) > 0:
            name = tds[0].getText()
            try:
                if stats[name] != {}:
                    h = 0
                    player_dict = {}
                    for td in tds:
                        header = headers[h]
                        if header == 'MP' and 'advanced' in url:
                            header = 'TMP'
                        stats[name][header] = td.getText()
                    if player_dict["Tm"] == "TOT":
                        stats[name] = player_dict
                    else:
                        pass
            except:
                stats[name] = {}
                h = 0
                for td in tds:
                    header = headers[h]
                    if header == 'MP' and 'advanced' in url:
                        header = 'TMP'
                    stats[name][header] = td.getText()
                    h += 1
    return stats

reg_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
adv_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"

https://www.sports-reference.com/cbb/schools/duke/2022.html

reg_stats = scrape(reg_stats_url)
adv_stats = scrape(adv_stats_url)

for player in reg_stats:
    reg_stats[player].update(adv_stats[player])
    del reg_stats[player][" "]

with open('stats.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(reg_stats, ensure_ascii=False, indent =4))
