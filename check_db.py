import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""
    SELECT * FROM fct_prices_hourly ORDER BY ts_utc LIMIT 5
""").df())

print(conn.execute("""
    SELECT hour_berlin,
           ROUND(AVG(price_eur_mwh), 1) AS ort_fiyat
    FROM fct_prices_hourly
    GROUP BY 1
    ORDER BY 1
""").df())

conn.close()
