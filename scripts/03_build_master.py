import pandas as pd
import geopandas as gpd
from scipy import stats

nc = gpd.read_file('zip://data/cb_2025_us_county_shapefile.zip')
nc = nc[nc['STATEFP']=='37'][['GEOID', 'NAME']].copy()
nc.columns=['fips','county']
nc['fips']=nc['fips'].astype(str)

print("NC COUNTIES FROM SHAPEFILE")
print(nc.shape)
print(nc.head(10))

si = pd.read_csv('data/si_trend.csv')
si_2024 = si[si['year'] == 2024][['county']].copy()

shapefile_names = set(nc['county'].str.strip())
ncdetect_names = set(si_2024['county'].str.strip())

only_in_shapefile = shapefile_names - ncdetect_names
only_in_ncdetect = ncdetect_names - shapefile_names

print("\nNAME COMPARISON")
print(f"Only in shapefile: {sorted(only_in_shapefile)}")
print(f"Only in NC DETECT: {sorted(only_in_ncdetect)}")


# merge FIPS codes onto NC detect data
si_2024 = si[si['year'] == 2024][['county', 'si_crude_rate']].copy()
sii = pd.read_csv('data/sii_trend.csv')
sii_2024 = sii[sii['year'] == 2024][['county', 'sii_crude_rate']].copy()

master = nc.merge(si_2024, on='county', how='left')
master = master.merge(sii_2024, on='county', how='left')

# merge county health rankings
chr_df = pd.read_csv('data/chr_2025.csv')
chr_df['fips'] = chr_df['FIPS'].astype(str).str.zfill(5)
chr_df = chr_df.drop(columns=['FIPS', 'County'])
master = master.merge(chr_df, on='fips', how='left')

print("\nMASTER DATAFRAME")
print(master.shape)
print(master.columns.tolist())
print(master.head(5))
print(f"\nMissing values:\n{master.isna().sum()}")

# clean column names

master.columns = ['fips', 'county', 'si_crude_rate', 'sii_crude_rate', 'mh_provider_rate', 'mh_provider_ratio_str', 'pct_uninsured', 'pct_unemployed', 'pct_children_poverty', 'avg_mentally_unhealthy_days']

# parse provider ratio string to float
master['mh_provider_ratio'] = (
    master['mh_provider_ratio_str']
    .str.split(':').str[0]
    .astype(float)
)
master = master.drop(columns=['mh_provider_ratio_str'])

print("\nCLEANED MASTER")
print(master.columns.tolist())
print(master.head(3))
print(f"\nMissing values:\n{master.isna().sum()}")

# fill missing provider rate value with column mean
master['mh_provider_rate'] = master['mh_provider_rate'].fillna(master['mh_provider_rate'].mean())

master['mh_provider_rate_z'] = stats.zscore(master['mh_provider_rate'])
master['capacity_score'] = master['mh_provider_rate_z']
master['si_crude_rate_z'] = stats.zscore(master['si_crude_rate'])
master['sii_crude_rate_z'] = stats.zscore(master['sii_crude_rate'])


# Calculate the burden score (average of the two conditions)
master['burden_score'] = ((master['si_crude_rate_z'] + master['sii_crude_rate_z'])/2)

# index score
master['gap_index'] = master['burden_score']-master['capacity_score']

print(master[['county', 'burden_score', 'capacity_score', 'gap_index']].sort_values('gap_index', ascending=False).head(15))

master.to_csv('data/master.csv', index=False)
print("\nSaved master.csv to data folder.")