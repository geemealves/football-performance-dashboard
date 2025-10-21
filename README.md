# Projeto: Football Performance Dashboard

Um projeto completo (rascunho de repositório) para coletar, transformar e visualizar dados de desempenho de times de futebol. Inclui código, README, estrutura de pastas, e um dashboard criado com **Streamlit** (fácil de rodar localmente ou subir no Streamlit Cloud). Todo o conteúdo está em Português.

---

## Visão geral

**Objetivo:** criar um projeto replicável que permita ingerir dados de partidas (placar, posse, chutes, passes, cartões etc.), armazenar/transformar, e exibir métricas e visualizações interativas para comparar desempenho entre times e ao longo do tempo.

**Tecnologias:**

* Python 3.10+
* Pandas, SQLAlchemy
* Streamlit (dashboard)
* Plotly (gráficos interativos)
* Optional: Docker, GitHub Actions para CI

---

## Estrutura do repositório (sugestão)

```
football-performance-dashboard/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ data/
│  ├─ sample_matches.csv
├─ src/
│  ├─ etl.py
│  ├─ generate_data.py
│  ├─ metrics.py
│  └─ db.py
├─ dashboard/
│  └─ app.py
├─ notebooks/
│  └─ exploration.ipynb
├─ .github/
│  └─ workflows/ci.yml
└─ Dockerfile
```

---

## README (resumo do que incluir)

```markdown
# Football Performance Dashboard

Dashboard interativo para análise de desempenho de times de futebol.

## Funcionalidades
- Importar CSV com dados de partidas
- Calcular métricas de time (gols marcados/sofridos, xG, posse média, chutes por jogo, passes certos, cartões)
- Comparar séries temporais entre times
- Rankings e radar charts por time

## Como rodar localmente
1. Clonar o repositório
2. Criar e ativar ambiente virtual: `python -m venv venv && source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows)
3. Instalar dependências: `pip install -r requirements.txt`
4. Rodar dashboard: `streamlit run dashboard/app.py`

## Deploy
- Opcional: subir no Streamlit Cloud (link do repo) ou em container Docker

## Estrutura de dados (sample_matches.csv)
Colunas sugeridas:
- date (YYYY-MM-DD)
- season
- league
- home_team
- away_team
- home_goals
- away_goals
- home_possession
- away_possession
- home_shots
- away_shots
- home_shots_on_target
- away_shots_on_target
- home_passes_completed
- away_passes_completed
- home_yellow_cards
- away_yellow_cards
- home_red_cards
- away_red_cards
- xG_home
- xG_away
```

---

## Código exemplar

### requirements.txt

```
streamlit
pandas
plotly
sqlalchemy
python-dotenv
numpy
 matplotlib
```

### src/generate_data.py

```python
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
```

### src/etl.py

```python
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
```

### dashboard/app.py (Streamlit)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from src.etl import load_data, prepare_team_metrics

st.set_page_config(layout='wide', page_title='Football Performance Dashboard')

st.title('Football Performance Dashboard')

# Upload ou usar sample
uploaded = st.file_uploader('Escolha um CSV com partidas (ou deixe em branco para usar sample)', type='csv')
if uploaded:
    df = pd.read_csv(uploaded, parse_dates=['date'])
else:
    df = load_data('data/sample_matches.csv')

st.sidebar.header('Filtros')
seasons = sorted(df['season'].unique())
season = st.sidebar.selectbox('Season', seasons, index=len(seasons)-1)

teams = sorted(set(df['home_team']).union(set(df['away_team'])))
team = st.sidebar.selectbox('Time', teams)

# Mostrar KPIs simples
st.subheader(f'Métricas - {team} ({season})')
# Preparar dados long form
long = prepare_team_metrics(df[df['season']==season])
team_df = long[long['team']==team]

col1, col2, col3, col4 = st.columns(4)
col1.metric('Jogos', int(team_df.shape[0]))
col2.metric('Gols (total)', int(team_df['goals'].sum()))
col3.metric('xG (total)', round(team_df['xG'].sum(),2))
col4.metric('Posse média', round(team_df['possession'].mean(),1))

# Série temporal de gols/xG
fig = px.line(team_df.sort_values('date'), x='date', y=['goals','xG'], labels={'value':'Valor','date':'Data'}, title='Gols e xG ao longo do tempo')
st.plotly_chart(fig, use_container_width=True)

# Comparação entre times (ranking)
agg = long.groupby('team').agg({'goals':'sum','xG':'sum','shots':'mean','possession':'mean'}).reset_index()
rank_fig = px.bar(agg.sort_values('goals',ascending=False), x='team', y='goals', title='Total de gols por time (season)')
st.plotly_chart(rank_fig, use_container_width=True)

# Radar ou scatter com duas métricas
scatter = px.scatter(agg, x='possession', y='shots', size='goals', hover_name='team', title='Posse x Chutes (bolha = gols)')
st.plotly_chart(scatter, use_container_width=True)
```

---

## GitHub Actions (CI) exemplo

`.github/workflows/ci.yml`

```yaml
name: CI
on: [push]
jobs:
  lint-and-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run basic smoke
        run: python -m pip install pytest && pytest -q || true
```

---

## Próximos passos e customizações sugeridas

* Adicionar autenticação e permissões se for expor o dashboard (Streamlit share + teams)
* Subir base real: integrar com API (Football-Data.org, Opta, or public APIs) — atenção a limites e licença
* Adicionar cálculo de métricas avançadas: xG por 90, PPDA, pressing, expected points
* Frontend React + D3 se quiser visual mais custom (possesion maps, heatmaps)

---

Se quiser, eu posso:

* Gerar os arquivos concretos para fazer `git init` localmente (cada arquivo pronto)
* Criar a versão em React/Next.js + Tailwind em vez de Streamlit
* Fazer o Dockerfile e o workflow completos

Diga qual opção prefere (gerar arquivos prontos para baixar / criar repo no GitHub / trocar a stack para React).
