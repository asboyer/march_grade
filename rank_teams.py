import json

with open('big_data/teams.json', 'r') as file:
    stats = json.load(file)

ranks = {}
for player in stats:
    ranks[player] = {}

categories =  [
        "FG",
        "FGA",
        "FG%",
        "2P",
        "2PA",
        "2P%",
        "3P",
        "3PA",
        "3P%",
        "FT",
        "FTA",
        "FT%",
        "ORB",
        "DRB",
        "TRB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "PF",
        "PTS",
        "o_FG",
        "o_FGA",
        "o_FG%",
        "o_2P",
        "o_2PA",
        "o_2P%",
        "o_3P",
        "o_3PA",
        "o_3P%",
        "o_FTA",
        "o_ORB",
        "o_DRB",
        "o_TRB",
        "o_AST",
        "o_STL",
        "o_BLK",
        "o_TOV",
        "o_PF",
        "o_PTS"
]

high_bad = ['TOV', 'o_FG', 'o_FGA', 'o_FG%', "o_2P", "o_2PA", "o_2P%",
                    "o_3P", "o_3PA", "o_3P%", "o_FTA", "o_ORB", "o_DRB", "o_TRB",
                    "o_AST", "o_STL", "o_BLK", "PF", "o_PTS"]

def rank(category):
    category_rankings = []
    for player in stats:
        category_rankings.append([player, float(stats[player][category])])
    category_rankings = sorted(category_rankings, key=lambda x: x[1])
    if category in high_bad:
        pass
    else:
        category_rankings.reverse()

    for i in range(len(category_rankings)):
        name = category_rankings[i][0]
        value = category_rankings[i][1]
        ranks[name][category] = i + 1

for category in categories:
    rank(category)

for player in ranks:
    score = 0
    for category in ranks[player]:
        score += ranks[player][category]
    ranks[player]['grade'] = int(score/len(categories))
    ranks[player]['score'] = int(score)
    ranks[player]['seed'] = stats[player]['seed']
    

final_ranks = []
for player in ranks:
    final_ranks.append([player, int(ranks[player]['grade'])])
final_ranks = sorted(final_ranks, key=lambda x: x[1])

final_string = ""
for i in range(len(final_ranks)):
    name = final_ranks[i][0]
    grade = final_ranks[i][1]
    if i == len(final_ranks) - 1:
        final_string += f"{str(i + 1)}. {name} (score: {str(grade)})"
    else:
        final_string += f"{str(i + 1)}. {name} (score: {str(grade)})\n"  

with open('team_ranks.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(ranks, ensure_ascii=False, indent =4))

with open('final.txt', 'w+', encoding='utf8') as file:
    file.write(final_string)