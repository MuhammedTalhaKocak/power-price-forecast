WITH windows AS (
    SELECT
        date_berlin,
        hour_berlin,
        price_eur_mwh,
        is_day_off,

        SUM(price_eur_mwh) OVER (
            PARTITION BY date_berlin
            ORDER BY ts_utc
            ROWS BETWEEN CURRENT ROW AND 5 FOLLOWING
        ) AS block_sum,

        COUNT(*) OVER (
            PARTITION BY date_berlin
            ORDER BY ts_utc
            ROWS BETWEEN CURRENT ROW AND 5 FOLLOWING
        ) AS block_len
    FROM {{ref('fct_prices_hourly')}}
)
SELECT
    date_berlin,
    MAX(is_day_off) AS is_day_off,
    SUM(CASE WHEN hour_berlin BETWEEN 10 AND 15 THEN price_eur_mwh END) AS rule_cost,
    MIN(CASE WHEN block_len = 6 THEN block_sum END) AS oracle_cost
FROM windows
GROUP BY date_berlin