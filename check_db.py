import requests
import pandas as pd
import duckdb
import os

url = "https://api.energy-charts.info/price"
params = {"bzn": "DE-LU", "start": "2026-10-16", "end": "2026-10-17"}

r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
data = r.json()


def fetch_prices(start: str, end: str) -> pd.DataFrame:
    url = "https://api.energy-charts.info/price"
    params = {"bzn": "DE-LU", "start": start, "end": end}
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(
            {
                "ts": pd.to_datetime(data["unix_seconds"], unit="s", utc=True),
                "price_eur_mwh": data["price"],
            }
        )
        return df
    except (requests.RequestException, KeyError) as e:
        print(f"Hata ({start} → {end}): {e}")
        return pd.DataFrame()


def load_prices(conn, df: pd.DataFrame) -> None:
    if df.empty:
        return
    conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_prices(
                ts TIMESTAMPTZ PRIMARY KEY,
                price_eur_mwh DOUBLE
            )
        """)
    conn.execute("""
            INSERT OR IGNORE INTO raw_prices (ts, price_eur_mwh)
            SELECT ts, price_eur_mwh FROM df
        """)
