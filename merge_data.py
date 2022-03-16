import json
import os

files = os.listdir('teams')

players = {}
teams = {}

for filename in files:
    with open(f'teams/{filename}', 'r') as file:
        team = json.load(file)
        players.update(team[filename.split('.json')[0]]['players'])
        teams[filename.split('.json')[0]] = team[filename.split('.json')[0]]['team']['team_stats']
        teams[filename.split('.json')[0]].update(team[filename.split('.json')[0]]['team']['opponent_stats'])
        teams[filename.split('.json')[0]]['seed'] = team[filename.split('.json')[0]]['seed']
with open('big_data/players.json', 'w+') as file:
    file.write(json.dumps(players, indent=4))
with open('big_data/teams.json', 'w+') as file:
    file.write(json.dumps(teams, indent=4))