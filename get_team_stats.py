from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_team_stats(team):
    url = f"https://www.sports-reference.com/cbb/schools/{team}/2022.html"

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  

    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll('tr')[1:]

    stats = {}
    players = []
    for i in range(len(rows)):
        player = rows[i].findAll('th')[0]
        # print("'" + player.getText() + "'")
        if player.getText() == 'Team':
            players = players[0:len(players) - 1]
            break
        else:
            players.append([player.getText(), rows[i].findAll('td')])
    for player in players:
        h = 0
        stats[player[0]] = {}
        for td in player[1]:
            stats[player[0]][headers[h]] = td.getText()
            h += 1

    final_stats = {}
    for player in stats:
        final_stats[player] = {}
        if stats[player]["RSCI Top 100"] == "":
            final_stats[player]['hs_rank'] = 101
        else:
            final_stats[player]['hs_rank'] = int(stats[player]["RSCI Top 100"].split(' ')[0])
        summary_str = stats[player]['Summary']
        cats = ['Pts', 'Reb', 'Ast']
        if summary_str == '':
            for c in range(len(cats)):
                final_stats[player][cats[c]] = 0.0
        else:
            sum_list = summary_str.split(',')
            for i in range(len(sum_list)):
                sum_list[i] = sum_list[i].strip()
            pstats = []
            for i in range(len(sum_list)):
                pstats.append(float(sum_list[i].split(' ')[0]))
            for c in range(len(cats)):
                final_stats[player][cats[c]] = pstats[c]

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