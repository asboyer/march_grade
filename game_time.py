import json
from random import randint
from correct_name import correct_name

with open('teams.json', 'r') as file:
    bracket = json.load(file)
with open('goat_grade.json', 'r') as file:
    grades = json.load(file)

for conf in bracket:
    for team in bracket[conf]:
        if bracket[conf][team]['team'] == "":
            pass
        else:
            name = correct_name(bracket[conf][team]['team'])
            goat_grade = (grades[name]['goat_grade']) + (grades[name]['goat_rank']) + (grades[name]['seed']) + randint(-16, 16)
            bracket[conf][team]['goat_grade'] = goat_grade
with open('teams.json', 'w+') as file:
    file.write(json.dumps(bracket, indent=4))