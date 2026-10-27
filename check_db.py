import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""
    SELECT * FROM fct_daily_block_costs ORDER BY date_berlin LIMIT 5
""").df())

conn.close()
