# dashboard/app.py
import sys
import os

# --- Garante que a raiz do projeto está no sys.path ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# ------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

# importa as funções principais (assume que existam)
from src.generate_data import generate_sample_matches
from src.etl import load_data, prepare_team_metrics

st.set_page_config(layout='wide', page_title='Football Performance Dashboard')
st.title('Football Performance Dashboard')

# -------------------- carregamento / geração de sample --------------------
uploaded = st.file_uploader(
    'Escolha um CSV com partidas (ou deixe em branco para usar sample)', 
    type='csv'
)

# caminho absoluto para o arquivo de exemplo
sample_path = os.path.join(ROOT, "data", "sample_matches.csv")
# garante que a pasta data/ existe
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)

# carrega df dependendo de upload / arquivo / gerador
if uploaded:
    try:
        df = pd.read_csv(uploaded, parse_dates=['date'])
    except Exception as e:
        st.error(f"Erro ao ler o CSV enviado: {e}")
        st.stop()
else:
    if os.path.exists(sample_path):
        try:
            df = load_data(sample_path)
        except Exception as e:
            st.error(f"Erro ao ler o sample em {sample_path}: {e}")
            st.stop()
    else:
        st.warning("Gerando arquivo de amostra (sample_matches.csv)...")
        try:
            df = generate_sample_matches(n=200, start_date="2021-01-01")
            df.to_csv(sample_path, index=False)
            st.success(f"Arquivo salvo em {sample_path}")
        except Exception as e:
            st.error(f"Falha ao gerar sample automaticamente: {e}")
            st.stop()
# -------------------------------------------------------------------------

# --- DEBUG: mostrar colunas e preview do df carregado ---
st.write("### Colunas do DataFrame carregado")
st.write(df.columns.tolist())

st.write("### Preview (5 primeiras linhas)")
st.dataframe(df.head())
# ---------------------------------------------------------

# segurança: transformar nomes de colunas para padrão conhecido (ex.: home_team / away_team)
# mas não alteramos; apenas validamos existência de colunas necessárias
required_pairs = [
    ("home_team", "away_team"),
    ("home_goals", "away_goals"),
    ("home_possession", "away_possession"),
]

# Avisar se faltam colunas importantes (mas não interromper)
missing_important = []
for left, right in required_pairs:
    if left not in df.columns or right not in df.columns:
        missing_important.append((left, right))

if missing_important:
    st.warning(
        "Algumas colunas esperadas não foram encontradas no CSV. "
        "O dashboard tentará adaptar, mas alguns gráficos/indicadores podem ficar incompletos. "
        f"Colunas faltantes (ex.: pares home/away): {missing_important}"
    )

# -------------------- filtros e preparação --------------------
# seasons
if 'season' in df.columns:
    seasons = sorted(df['season'].dropna().unique().tolist())
else:
    seasons = ["unknown"]
    df['season'] = "unknown"

# escolha de season
season = st.sidebar.selectbox('Season', seasons, index=max(0, len(seasons) - 1))

# times: tenta extrair nomes a partir de home_team/away_team; se não existirem, usa fallback 'team'
if 'home_team' in df.columns and 'away_team' in df.columns:
    teams = sorted(set(df['home_team'].dropna().unique()).union(set(df['away_team'].dropna().unique())))
elif 'team' in df.columns:
    teams = sorted(df['team'].dropna().unique().tolist())
else:
    teams = []
    st.warning("Não foi possível identificar nomes de times no CSV (procure por home_team / away_team).")

team = st.sidebar.selectbox('Time', teams) if teams else None

st.subheader(f'Football Performance Dashboard' + (f" — {team} ({season})" if team else ""))

# Filtra por season (se existir)
df_season = df[df['season'] == season] if 'season' in df.columns else df.copy()

# prepara dados no formato long (vai lidar com prefixos home_/away_ ou já normalizado)
try:
    long = prepare_team_metrics(df_season)
except Exception as e:
    st.error(f"Erro ao preparar métricas: {e}")
    st.stop()

# se não escolheu time (por falta de times), mostra apenas o table
if not team:
    st.info("Nenhum time selecionável encontrado. Mostrando tabela de dados simples.")
    st.dataframe(long.head())
    st.stop()

team_df = long[long['team'] == team]

# segurança: se não houver linhas para o time escolhido
if team_df.empty:
    st.warning(f"Não foram encontradas partidas para o time {team} na season {season}.")
    st.stop()

# Certificar colunas numéricas usadas
numeric_cols_defaults = {
    'goals': 0,
    'xG': 0.0,
    'possession': 0.0,
    'shots': 0.0,
}
for c, default in numeric_cols_defaults.items():
    if c not in team_df.columns:
        # cria coluna com valor default se faltar (para não quebrar métricas)
        team_df[c] = default
        long[c] = long.get(c, default)

# KPIs básicos (com proteção para NaN)
col1, col2, col3, col4 = st.columns(4)
col1.metric('Jogos', int(team_df.shape[0]))
col2.metric('Gols (total)', int(team_df['goals'].sum()))
# xG pode não existir ou ter NaN -> tratamos com fillna
col3.metric('xG (total)', round(team_df.get('xG', pd.Series([0])).fillna(0).sum(), 2))
col4.metric('Posse média', round(team_df.get('possession', pd.Series([0])).fillna(0).mean(), 1))

# Série temporal de gols/xG (proteção caso xG não exista)
y_cols = ['goals']
if 'xG' in team_df.columns:
    y_cols.append('xG')

fig = px.line(
    team_df.sort_values('date'), 
    x='date', 
    y=y_cols, 
    labels={'value': 'Valor', 'date': 'Data'}, 
    title='Gols e xG ao longo do tempo'
)
st.plotly_chart(fig, use_container_width=True)

# Comparação entre times (ranking) - usando 'long' (já agregável)
agg = long.groupby('team').agg({
    'goals': 'sum',
    'xG': 'sum' if 'xG' in long.columns else 'sum',
    'shots': 'mean',
    'possession': 'mean'
}).reset_index()

# preencher NaN para evitar erros no gráfico
for col in ['goals', 'xG', 'shots', 'possession']:
    if col in agg.columns:
        agg[col] = agg[col].fillna(0)

rank_fig = px.bar(
    agg.sort_values('goals', ascending=False),
    x='team', 
    y='goals',
    title='Total de gols por time (season)'
)
st.plotly_chart(rank_fig, use_container_width=True)

# Scatter posse x chutes
if 'possession' in agg.columns and 'shots' in agg.columns:
    scatter = px.scatter(
        agg,
        x='possession',
        y='shots',
        size='goals' if 'goals' in agg.columns else None,
        hover_name='team',
        title='Posse x Chutes (bolha = gols)'
    )
    st.plotly_chart(scatter, use_container_width=True)
else:
    st.info("Não há colunas 'possession' e 'shots' suficientes para gerar o scatter.")