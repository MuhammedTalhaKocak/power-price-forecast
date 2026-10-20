SELECT 
    date_berlin,
    COUNT(hour_berlin) AS hour_counts
FROM {{ref("fct_prices_hourly")}}
GROUP BY date_berlin
HAVING hour_counts NOT IN (23,24,25)
