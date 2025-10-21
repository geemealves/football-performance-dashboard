import pandas as pd


def load_data(path='data/sample_matches.csv'):
df = pd.read_csv(path, parse_dates=['date'])
return df


def prepare_team_metrics(df):
# Exemplo: agregação por time e por temporada
home = df.rename(columns=lambda c: c.replace('home_',''))
away = df.rename(columns=lambda c: c.replace('away_',''))


home = home[['date','season','league','team','goals','possession','shots','shots_on_target','passes_completed','yellow_cards','red_cards','xG']] if False else None
# Vamos seguir uma abordagem direta e criar linhas por time (home + away)
homes = df[['date','season','league','home_team','home_goals','home_possession','home_shots','home_shots_on_target','home_passes_completed','home_yellow_cards','home_red_cards','xG_home']]
homes = homes.rename(columns={
'home_team':'team','home_goals':'goals','home_possession':'possession','home_shots':'shots','home_shots_on_target':'shots_on_target','home_passes_completed':'passes_completed','home_yellow_cards':'yellow_cards','home_red_cards':'red_cards','xG_home':'xG'
})
aways = df[['date','season','league','away_team','away_goals','away_possession','away_shots','away_shots_on_target','away_passes_completed','away_yellow_cards','away_red_cards','xG_away']]
aways = aways.rename(columns={
'away_team':'team','away_goals':'goals','away_possession':'possession','away_shots':'shots','away_shots_on_target':'shots_on_target','away_passes_completed':'passes_completed','away_yellow_cards':'yellow_cards','away_red_cards':'red_cards','xG_away':'xG'
})
long = pd.concat([homes, aways], ignore_index=True)
return long
