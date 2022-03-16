from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_team_stats(team):
    url = f"https://www.sports-reference.com/cbb/schools/{team}/2022.html"

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  

    rows = soup.findAll('tr')[1:]
    stats = {}
    players = []
    f = 0
    for i in range(len(rows)):
        player = rows[i].findAll('th')[0]
        if player.getText() == 'Rk':
            if f == 0:
                ind = i
                f += 1
            elif f == 1:
                end = i
                break

    headers = []
    hs = rows[ind].findAll('th')
    for h in hs:
        headers.append(h.getText())
    headers = headers[2:]
    
    for p in rows[ind+1:end]:
        h = 0
        tds = p.findAll('td')
        stats[f"{tds[0].getText()} ({team})"] = {}
        for td in tds[1:]:
            if td.getText() == '':
                num = 0.0
            else:
                num = td.getText()
            stats[f"{tds[0].getText()} ({team})"][headers[h]] = float(num)
            h += 1

    stats1 = {}
    f = 0
    for i in range(len(rows)):
        player = rows[i].findAll('th')[0]
        if player.getText() == 'Rk':
            if f == 8:
                adv_ind = i
            elif f == 9:
                end = i
                break
            f += 1

    headers = []
    hs = []
    hs = rows[adv_ind].findAll('th')
    for h in hs:
        headers.append(h.getText())
    headers = headers[2:]
    for p in rows[adv_ind+1:end]:
        h = 0
        tds = p.findAll('td')
        stats1[f"{tds[0].getText()} ({team})"] = {}
        for td in tds[1:]:
            if td.getText() == '':
                num = 0.0
            else:
                num = td.getText()
            stats1[f"{tds[0].getText()} ({team})"][headers[h]] = float(num)
            h += 1

    final_stats = {}

    for player in stats:
        stats[player].update(stats1[player])
        del stats[player]["\u00a0"]

    final_stats = stats

    team_stats = {}
    categories = []
    for i in range(len(rows)):
            player = rows[i].findAll('th')[0]
            if player.getText() == 'Team':
                ind = i
                heads = rows[i-1].findAll('th')[3:]
                for h in heads:
                    categories.append(h.getText())    
                break

    tds = rows[ind].findAll('td')[2:]
    h = 0
    ts = {}
    for td in tds:
        ts[categories[h]] = float(td.getText())
        h += 1

    tds = rows[ind + 2].findAll('td')[2:]
    h = 0
    os = {}
    for td in tds:
        os["o_" + categories[h]] = float(td.getText())
        h += 1

    tds = rows[ind + 1].findAll('td')[2:]
    h = 0
    t = {}
    for td in tds:
        t[categories[h]] = int(td.getText().split('s')[0].split('n')[0].split('r')[0].split('t')[0])
        h += 1

    tds = rows[ind + 3].findAll('td')[2:]
    h = 0
    o = {}
    for td in tds:
        o[categories[h]] = int(td.getText().split('s')[0].split('n')[0].split('r')[0].split('t')[0])
        h += 1
    team_stats = {
        'team_stats': ts,
        'opponent_stats': os,
        'team_ranks': t,
        'opponent_ranks': o
    }

    j = {}
    j[team] = {
        'players': final_stats,
        'team': team_stats
    }

    return j

if __name__ == '__main__':
    data = get_team_stats('gonzaga')
    with open('test.json', 'w+') as file:
        file.write(json.dumps(data, indent = 4))