import pandas as pd

chr_raw = pd.read_excel(
    'data/county_health_rankings_2025.xlsx',
    sheet_name='Select Measure Data',
    header=1
)

cols_needed = [
    'FIPS', 'County',
    'Mental Health Provider Rate',
    'Mental Health Provider Ratio',
    '% Uninsured',
    '% Unemployed',
    '% Children in Poverty',
    'Average Number of Mentally Unhealthy Days'
]

chr_df = chr_raw[cols_needed].copy()
chr_df = chr_df[chr_df['FIPS'] != 37000].reset_index(drop=True)

print(chr_df.shape)
print(chr_df.head(10))
print(f"\nMissing values:\n{chr_df.isna().sum()}")

chr_df.to_csv('data/chr_2025.csv', index=False)
print("\nSaved chr_2025.csv to data folder.")
