SELECT 
    date_berlin 
FROM {{ref('fct_daily_block_costs')}}
WHERE oracle_cost > rule_cost