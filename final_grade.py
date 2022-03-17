import json
from random import randint

def final_grade(player_weight=1, team_weight=1.5):
    with open('data/final.json', 'r') as file:
        d = json.load(file)
    for team in d:
        goat_grade = d[team]['avg_player_grade'] * player_weight
        goat_grade += d[team]['team_grade'] * team_weight
        # goat_grade += d[team]['seed'] * seed_weight
        # goat_grade += randint(-randomness, randomness)
        d[team]['goat_grade'] = int(goat_grade)
        del d[team]['avg_player_grade']
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

    with open('data/goat_grade.json', 'w+', encoding='utf8') as file:
        file.write(json.dumps(d, indent=4))
