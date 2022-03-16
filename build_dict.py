from get_team_stats import get_team_stats
from correct_name import correct_name
import json

with open('teams.json', 'r') as file:
	teams = json.load(file)
for conf in teams:
	for t in teams[conf]:
		n = correct_name(teams[conf][t]['team'])
		if n != '':
			j = get_team_stats(n)
			j[n]['seed'] = teams[conf][t]['seed']
			with open(f'teams/{n}.json', 'w+', encoding='utf8') as file:
				file.write(json.dumps(j, ensure_ascii=False, indent =4))

