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
