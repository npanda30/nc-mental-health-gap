import pandas as pd

def load_ncdetect(filepath, year):
    df = pd.read_csv(filepath, encoding='utf-16', sep='\t')
    df.columns = ['county', 'metric', 'state', 'value']
    crude = df[df['metric'] == 'Crude Rate'][['county', 'value']].copy()
    crude['value'] = pd.to_numeric(crude['value'], errors='coerce')
    crude = crude.reset_index(drop=True)
    crude['year'] = year
    return crude

si_years = range(2017, 2025)
sii_years = range(2021, 2025)

si_frames = [load_ncdetect(f'data/ncdetect_suicidal_ideation_{y}.csv', y) for y in si_years]
sii_frames = [load_ncdetect(f'data/ncdetect_self_inflicted_{y}.csv', y) for y in sii_years]

si_all = pd.concat(si_frames, ignore_index=True)
sii_all = pd.concat(sii_frames, ignore_index=True)

si_all.columns = ['county', 'si_crude_rate', 'year']
sii_all.columns = ['county', 'sii_crude_rate', 'year']

print("=== SUICIDAL IDEATION ALL YEARS ===")
print(si_all.shape)
print(si_all.head(10))
print(f"Years: {sorted(si_all['year'].unique())}")
print(f"Missing values: {si_all['si_crude_rate'].isna().sum()}")

print("\n=== SELF INFLICTED INJURY ALL YEARS ===")
print(sii_all.shape)
print(sii_all.head(10))
print(f"Years: {sorted(sii_all['year'].unique())}")
print(f"Missing values: {sii_all['sii_crude_rate'].isna().sum()}")

si_all.to_csv('data/si_trend.csv', index=False)
sii_all.to_csv('data/sii_trend.csv', index=False)

print("\nSaved si_trend.csv and sii_trend.csv to data folder.")