# src/etl.py
import pandas as pd
from typing import List


def load_data(path: str = "data/sample_matches.csv") -> pd.DataFrame:
    """Carrega CSV e parseia coluna 'date'."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def _detect_prefixes(df: pd.DataFrame):
    """
    Retorna True se existir colunas com home_ e away_.
    """
    cols = set(df.columns)
    if any(c.startswith("home_") for c in cols) and any(c.startswith("away_") for c in cols):
        return True
    return False


def _safe_cast_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Tenta converter colunas para numérico; se não existir, ignora."""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def prepare_team_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe DataFrame no formato wide com home_* / away_* e retorna DataFrame long
    com colunas padronizadas:
      ['date','season','league','team','goals','xG','possession','shots',
       'shots_on_target','passes_completed','yellow_cards','red_cards','home_away']
    """
    df = df.copy()

    # garante date como datetime (se não estiver)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    has_prefix = _detect_prefixes(df)

    if has_prefix:
        # cria views e remove prefixo para cada view
        home = df[[c for c in df.columns if c.startswith("home_") or c in ("date", "season", "league")]].copy()
        away = df[[c for c in df.columns if c.startswith("away_") or c in ("date", "season", "league")]].copy()

        # renomeia removendo prefixos
        home.columns = [c.replace("home_", "") for c in home.columns]
        away.columns = [c.replace("away_", "") for c in away.columns]
    else:
        # se já estiver sem prefixos, usamos as mesmas tabelas
        home = df.copy()
        away = df.copy()

    # colunas desejadas no formato final (xG é opcional)
    desired = [
        "date", "season", "league", "team", "goals", "xG", "possession",
        "shots", "shots_on_target", "passes_completed", "yellow_cards", "red_cards"
    ]

    def ensure_columns(frame: pd.DataFrame) -> pd.DataFrame:
        for col in desired:
            if col not in frame.columns:
                frame[col] = pd.NA
        # seleciona na ordem desejada
        return frame[[c for c in desired]]

    homes = ensure_columns(home)
    aways = ensure_columns(away)

    # marca casa/fora
    homes["home_away"] = "home"
    aways["home_away"] = "away"

    # converte colunas numéricas
    numeric_cols = ["goals", "xG", "possession", "shots", "shots_on_target", "passes_completed", "yellow_cards", "red_cards"]
    homes = _safe_cast_numeric(homes, numeric_cols)
    aways = _safe_cast_numeric(aways, numeric_cols)

    long = pd.concat([homes, aways], ignore_index=True)

    # garantias extras
    if "date" in long.columns:
        long["date"] = pd.to_datetime(long["date"], errors="coerce")
    if "season" in long.columns:
        long["season"] = long["season"].astype(str)

    return long