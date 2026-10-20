WITH base_extracted_features AS (
    SELECT
        ts_utc,
        ts_berlin,
        price_eur_mwh,
        CAST(ts_berlin AS DATE) AS date_berlin, -- Sütun tipi TIMESTAMP olduğundan sadece gün/ay/yıl kısmını almak için CAST kullanıyoruz.
        HOUR(ts_berlin) AS hour_berlin, -- İlgili tarihin sadece SAAT kısmını alır.
        ISODOW(ts_berlin) AS day_of_week, -- Pazartesi=1, Pazar=7 olacak şekilde haftanın gününü sayısal olarak alır.
        MONTH(ts_berlin) AS month -- Ay bilgisini sayısal olarak çekmek için kullanılır.
    FROM {{ref('stg_prices')}}
), -- <--- İki CTE arasına virgül konur.

calculated_weekend_features AS (
    SELECT 
        *,
        CASE
            WHEN day_of_week IN (6, 7) THEN true
            ELSE false
        END AS is_weekend
    FROM base_extracted_features
)

SELECT 
    cwf.*,
    (hd.holiday_date IS NOT NULL) AS is_holiday,
    cwf.is_weekend OR (hd.holiday_date IS NOT NULL) AS is_day_off
FROM calculated_weekend_features cwf
LEFT JOIN {{ref('holidays_de')}} hd
ON cwf.date_berlin = hd.holiday_date

