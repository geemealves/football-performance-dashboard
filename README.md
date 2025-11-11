# ⚽ Football Performance Dashboard  

Um **dashboard interativo** construído com [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/) e [Plotly](https://plotly.com/python/), voltado para a **análise de desempenho em partidas de futebol**.

> 🧠 Este projeto utiliza **dados gerados aleatoriamente** — não representam clubes ou partidas reais.  
> O objetivo é demonstrar o uso de ferramentas de análise de dados e visualização em Python.

---

## 🚀 Funcionalidades
- Upload de um arquivo CSV com dados de partidas, ou geração automática de amostra (`sample_matches.csv`);
- Filtros por temporada e por time;
- Indicadores (KPIs) de desempenho do time selecionado;
- Gráficos de:
  - Gols e xG (gols esperados) ao longo do tempo;
  - Comparação de times (ranking de gols);
  - Relação entre posse de bola e chutes (gráfico de bolhas);
- Interface responsiva e moderna usando **Plotly Express** e **Streamlit**.

---

## 🧩 Estrutura do projeto
```bash
football-performance-dashboard/
│
├── dashboard/
│   └── app.py             # Arquivo principal do Streamlit
│
├── src/
│   ├── etl.py             # Funções de transformação e limpeza dos dados
│   └── generate_data.py   # Geração de dados simulados (sample_matches.csv)
│
├── data/
│   └── sample_matches.csv # Dados de exemplo gerados automaticamente
│
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo :)

---

## 💻 Como executar o projeto

---

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/geemealves/football-performance-dashboard.git
cd football-performance-dashboard
```

### 2️⃣ Criar ambiente virtual e instalar dependências
```bash
python -m venv venv
venv\Scripts\activate     # no Windows

# ou, no macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3️⃣ Executar o dashboard
```bash
streamlit run dashboard/app.py
```

O aplicativo será iniciado no navegador, geralmente em:  
👉 [http://localhost:8501](http://localhost:8501)

---

## 🧠 Tecnologias utilizadas
- **Python 3.12+**
- **Streamlit**
- **Pandas**
- **Plotly Express**
- **NumPy**

---

## 📊 Sobre os dados
Os dados foram **gerados automaticamente** usando o script `src/generate_data.py`.  
Eles **não representam times, ligas ou partidas reais** — são apenas exemplos para fins de aprendizado e demonstração de visualização de dados esportivos.

---

## 📜 Licença
Este projeto está licenciado sob a licença **MIT** — você pode usar, modificar e distribuir à vontade, desde que mantenha a atribuição.
