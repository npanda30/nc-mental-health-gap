import pysal
import esda
import pandas as pd
import geopandas as gpd

master = pd.read_csv('data/master.csv')

nc = gpd.read_file('zip://data/cb_2025_us_county_shapefile.zip')
nc = nc[nc['STATEFP']=='37'][['GEOID', 'NAME', 'geometry']].copy()
# Note here the FIPS column is titled GEOID

# Merge on the nc[GEOID] and master[fips] columns
master['fips'] = master['fips'].astype(str).str.zfill(5)
merged = nc.merge(master, left_on='GEOID', right_on='fips', how='left')

print(merged[['GEOID', 'county', 'fips', 'gap_index', 'geometry']].head())
print(merged.shape)

from libpysal.weights import Queen
mergedwq = Queen.from_dataframe(merged, use_index=False)
print(mergedwq)
print(mergedwq.n)

mi = esda.Moran(merged['gap_index'], mergedwq)

print(mi.I)
print(mi.p_sim)
