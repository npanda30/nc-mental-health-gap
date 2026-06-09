import pysal
import esda
import pandas as pd
import geopandas as gpd

master = pd.read_csv('data/master.csv')

nc = gpd.read_file('zip://data/cb_2025_us_county_shapefile.zip')
nc = nc[nc['STATEFP']=='37'][['GEOID', 'NAME', 'geometry']].copy()
# Note here the FIPS column is titled GEOID

# Merge on the nc[GEOID] and master[fips] columns