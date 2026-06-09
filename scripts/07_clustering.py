from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

master = pd.read_csv('data/master.csv')

clustdf = master[['burden_score', 'capacity_score', 'pct_children_poverty', 'avg_mentally_unhealthy_days']]

# create scaler object
scaler = StandardScaler()

clustdf_scaled = scaler.fit_transform(clustdf) # a numpy array with 4 variables on same scale
print(clustdf_scaled.shape)
