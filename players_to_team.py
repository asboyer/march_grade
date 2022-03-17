import json, os

def players_to_team():
    final = {}

    with open('data/player_ranks.json', 'r') as file:
        players = json.load(file)
    with open('data/team_ranks.json', 'r') as file:
        teams = json.load(file)

    files = os.listdir('teams')

    rosters = {}
    for filename in files:
        with open(f'teams/{filename}', 'r') as file:
            team = json.load(file)
        count = 0
        for player in team[filename.split('.json')[0]]['players']:
            count += 1
        rosters[filename.split('.json')[0]] = count

    for team in teams:
        player_grade = 0
        for player in players:
            if player.split('(')[1].replace(')', '') == team:
                player_grade += players[player]['rank']
        final[team] = {
            'avg_player_grade': int(player_grade / (rosters[team])),
            'team_grade': teams[team]['grade'] * (rosters[team]),
            'seed': teams[team]['seed']
        }

    with open('data/final.json', 'w+', encoding='utf8') as file:
        file.write(json.dumps(final, indent=4))
