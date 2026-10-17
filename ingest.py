import requests
import pandas as pd
import duckdb
import os
import time

os.makedirs(name="data", exist_ok=True)


def fetch_prices(start: str, end: str) -> pd.DataFrame:
    url = "https://api.energy-charts.info/price"
    params = {"bzn": "DE-LU", "start": start, "end": end}
    try:
        for deneme in range(4):
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 429:
                bekleme_suresi = 5 * 2**deneme
                print(f"429, {bekleme_suresi} sn bekleniyor")
                time.sleep(bekleme_suresi)
                continue
            r.raise_for_status()
            data = r.json()
            df = pd.DataFrame(
                {
                    "ts": pd.to_datetime(data["unix_seconds"], unit="s", utc=True),
                    "price_eur_mwh": data["price"],
                }
            )
            return df
        print(f"Vazgeçildi ({start} → {end}): 4 denemede de 429")
        return pd.DataFrame()
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


start = "2024-01-01"
end = "2026-10-17"  # yıl-ay-gün
tarih_araligi = pd.date_range(start=start, end=end, freq="MS")

conn = duckdb.connect(database="data/ptf.duckdb")
try:
    for ay_basi in tarih_araligi:
        ay_sonu = ay_basi + pd.offsets.MonthEnd(0)
        df = fetch_prices(
            start=ay_basi.strftime(format="%Y-%m-%d"),
            end=ay_sonu.strftime(format="%Y-%m-%d"),
        )
        load_prices(conn=conn, df=df)
        print(f"{ay_basi:%Y-%m}: {len(df)} satır")
        time.sleep(1)
finally:
    conn.close()
