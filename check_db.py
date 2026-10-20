import duckdb

conn = duckdb.connect("data/ptf.duckdb", read_only=True)

print(conn.execute("""SELECT is_holiday, COUNT(*) AS saat_sayisi
FROM fct_prices_hourly
GROUP BY 1""").df())

conn.close()
