import json

with open('final.json', 'r') as file:
    d = json.load(file)

for team in d:
    d[team]['goat_grade'] = int((d[team]['player_grade'] + d[team]['team_grade']))
    del d[team]['player_grade']
    del d[team]['team_grade']

category_rankings = []
for team in d:
    category_rankings.append([team, float(d[team]['goat_grade'])])
category_rankings = sorted(category_rankings, key=lambda x: x[1])
for i in range(len(category_rankings)):
    name = category_rankings[i][0]
    value = category_rankings[i][1]
    d[name]['goat_rank'] = i + 1
    d[name]['seed'] = int(d[name]['seed'])

with open('goat_grade.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(d, indent=4))
