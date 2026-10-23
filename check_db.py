import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""
    SELECT COUNT(*) AS satir, MIN(ts_berlin), MAX(ts_berlin)
    FROM 'data/fct_prices_hourly.parquet'
""").df())

conn.close()
