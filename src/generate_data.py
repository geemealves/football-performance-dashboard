"""Gerador de dados de exemplo para popular sample_matches.csv"""
import csv
from random import randint, uniform, choice
from datetime import date, timedelta


TEAMS = [
"Atlético", "Flamengo", "Palmeiras", "São Paulo", "Corinthians",
"Grêmio", "Internacional", "Santos", "Vasco", "Fluminense"
]


def generate_rows(n=200, start_date=date(2024,1,1)):
rows = []
for i in range(n):
d = start_date + timedelta(days=i)
home, away = choice(TEAMS), choice(TEAMS)
while away == home:
away = choice(TEAMS)
home_goals = randint(0,4)
away_goals = randint(0,4)
row = {
'date': d.isoformat(),
'season': d.year,
'league': 'Brasileirão',
'home_team': home,
'away_team': away,
'home_goals': home_goals,
'away_goals': away_goals,
'home_possession': round(uniform(40, 65),1),
'away_possession': round(100 - (round(uniform(40, 65),1)),1),
'home_shots': randint(5,20),
'away_shots': randint(3,18),
'home_shots_on_target': randint(1,10),
'away_shots_on_target': randint(0,9),
'home_passes_completed': randint(200,700),
'away_passes_completed': randint(150,650),
'home_yellow_cards': randint(0,3),
'away_yellow_cards': randint(0,3),
'home_red_cards': randint(0,1),
'away_red_cards': randint(0,1),
'xG_home': round(uniform(0,3),2),
'xG_away': round(uniform(0,3),2),
}
rows.append(row)
return rows


if __name__ == '__main__':
rows = generate_rows(300)
keys = list(rows[0].keys())
with open('data/sample_matches.csv','w',newline='',encoding='utf-8') as f:
writer = csv.DictWriter(f, fieldnames=keys)
writer.writeheader()
writer.writerows(rows)
print('Arquivo data/sample_matches.csv gerado com', len(rows), 'linhas')
