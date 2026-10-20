import holidays
import pandas as pd

holidays_dict = holidays.Germany(years=[2024, 2025, 2026, 2027])
df = pd.DataFrame(
    {"holiday_date": holidays_dict.keys(), "holiday_name": holidays_dict.values()}
).sort_values(by="holiday_date")
df.to_csv(path_or_buf="power_price/seeds/holidays_de.csv", index=False)
print(f"Tatil sayısı: {len(df)}")
print(df.head())
