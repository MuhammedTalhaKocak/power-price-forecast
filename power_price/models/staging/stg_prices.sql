WITH hourly_aggregated AS (
    SELECT
        -- 1. ts sütununu saat başına yuvarlıyoruz
        date_trunc('hour', ts) AS ts_utc,

        -- 2. O saatteki elektrik fiyatlarının ortalamasını alıyoruz
        AVG(price_eur_mwh) AS price_eur_mwh,

        -- 3. O saatte kaç satır (interval) olduğunu sayıyoruz
        COUNT(*) AS n_intervals,
    
    -- Bir önceki adımda YAML'da tanımladığımız ham kaynağı çağırıyoruz
    FROM {{ source('raw', 'raw_prices') }}

    -- Buradaki 1, SELECT içerisindeki birinci sütunu (yani ts_utc) temsil eder. DuckDB ve dbt projelerinde okunabilirliği artırmak için gruplama işlemlerinde sıkça tercih edilir.
    GROUP BY 1
)

SELECT
    ts_utc,
    price_eur_mwh,
    n_intervals,
    -- 4. ts_utc sütununu Berlin yerel saatine çeviriyoruz
    TIMEZONE('Europe/Berlin', ts_utc) AS ts_berlin
FROM hourly_aggregated