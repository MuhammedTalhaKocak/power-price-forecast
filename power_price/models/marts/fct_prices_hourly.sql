WITH base_extracted_features AS(
    SELECT
        ts_utc,
        ts_berlin,
        price_eur_mwh,
        CAST(ts_berlin AS DATE) AS date_berlin, -- Sütun tipi TIMESTAMP (zaman damgası - saatli tarih) olduğundan ve biz sadece gün/ay/yıl kısmını almak istediğimizden dolayı CAST fonksiyonu ile tarih formatındaki veriden sadece gün-ay-yıl kısmını çekiyoruz.
        HOUR(ts_berlin) AS hour_berlin, -- İlgili tarihin sadece SAAT kısmını almamızı sağlar.
        ISODOW(ts_berlin) AS day_of_week, -- Haftanın hangi gününde olduğumuzu Pazartesi=1, Pazar=7 olacak şekilde uluslararası standartta (ISO) sayısal olarak almak istiyoruz. Bunun için duckdb'de isodow fonksiyonunu kullanabiliriz.
        MONTH(ts_berlin) AS month -- Ay bilgisini sayısal olarak çekmek için MONTH fonksiyonu kullanılır. Örn: Kasım > 11, Ocak > 1 ..
        FROM {{ref('stg_prices')}}
)
SELECT 
*,
CASE
    WHEN day_of_week IN (6,7) THEN true
    ELSE false
END AS is_weekend
FROM base_extracted_features
