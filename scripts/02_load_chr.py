import pandas as pd
import numpy as np

chr_raw = pd.read_excel(
    'data/county_health_rankings_2025.xlsx',
    sheet_name='Select Measure Data',
    header=1
)

amd_raw = pd.read_excel('data/county_health_rankings_2025.xlsx', sheet_name='Additional Measure Data', header=1)

amd_cols_needed = ['FIPS', '% Rural']

amd_df = amd_raw[amd_cols_needed].copy()
amd_df = amd_df[amd_df['FIPS'] != 37000].reset_index(drop=True)

cols_needed = [
    'FIPS', 'County',
    'Mental Health Provider Rate',
    'Mental Health Provider Ratio',
    '% Uninsured',
    '% Unemployed',
    '% Children in Poverty',
    'Average Number of Mentally Unhealthy Days',
    'Population'
]

chr_df = chr_raw[cols_needed].copy()
chr_df = chr_df[chr_df['FIPS'] != 37000].reset_index(drop=True)

chr_df = chr_df.merge(amd_df, on='FIPS', how='left')
# merged = nc.merge(master, left_on='GEOID', right_on='fips', how='left')

chr_df['log_population'] = np.log(chr_df['Population'])

print(chr_df.shape)
print(chr_df.head(10))
print(f"\nMissing values:\n{chr_df.isna().sum()}")

chr_df.to_csv('data/chr_2025.csv', index=False)
print("\nSaved chr_2025.csv to data folder.")
