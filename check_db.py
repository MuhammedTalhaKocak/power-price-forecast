import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""
    SELECT COUNT(*) AS gun, MIN(date_berlin), MAX(date_berlin)
    FROM 'data/fct_daily_block_costs.parquet'
""").df())

conn.close()
