import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""
    SELECT * FROM stg_prices ORDER BY ts_utc LIMIT 5
""").df())

print(conn.execute("""
    SELECT n_intervals, COUNT(*) AS saat_sayisi
    FROM stg_prices
    GROUP BY 1
    ORDER BY 1
""").df())

conn.close()
