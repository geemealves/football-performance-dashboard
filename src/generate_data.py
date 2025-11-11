# src/generate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_matches(n: int = 100, start_date: str = "2020-01-01") -> pd.DataFrame:
    """
    Gera um DataFrame simples com n partidas a partir de start_date.
    """
    start = datetime.fromisoformat(start_date)
    dates = [start + timedelta(days=i) for i in range(n)]

    teams = [f"Team_{i}" for i in range(1, 21)]  # 20 times exemplo
    seasons = ["2020/2021", "2021/2022"]

    data = []
    for i in range(n):
        home = np.random.choice(teams)
        away = np.random.choice([t for t in teams if t != home])
        row = {
            "date": dates[i],
            "season": np.random.choice(seasons),
            "league": "Example League",
            "home_team": home,
            "away_team": away,
            "home_goals": np.random.randint(0, 6),
            "away_goals": np.random.randint(0, 6),
            "home_possession": np.random.randint(30, 71),
            "away_possession": 100 - np.random.randint(30, 71),
            "home_shots": np.random.randint(0, 20),
            "away_shots": np.random.randint(0, 20),
            "home_shots_on_target": np.random.randint(0, 10),
            "away_shots_on_target": np.random.randint(0, 10),
            "home_passes_completed": np.random.randint(100, 700),
            "away_passes_completed": np.random.randint(100, 700),
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # exemplo de uso: gera e salva CSV
    df = generate_sample_matches(n=200, start_date="2021-01-01")
    df.to_csv("data/sample_matches.csv", index=False)
    print("Arquivo data/sample_matches.csv gerado com", len(df), "linhas.")