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
