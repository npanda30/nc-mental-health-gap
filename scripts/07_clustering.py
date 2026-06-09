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


# General guidance - k should be smaller than sqrt n, and 2 clusters needed to mean anything
for i in [2, 3, 4, 5, 6, 7, 8]:
    k = KMeans(n_clusters=i, random_state=42).fit(clustdf_scaled)
    score = silhouette_score(clustdf_scaled, k.labels_)
    print(f"{i}: {score}")

k = KMeans(n_clusters = 3, random_state=42).fit(clustdf_scaled)
master['cluster_labels'] = k.labels_
print(master.groupby('cluster_labels')[['burden_score', 'capacity_score', 'pct_children_poverty', 'avg_mentally_unhealthy_days']].mean())

# Shows 3 clusters:
# 0: high need, under-resourced (high burden, high poverty, worst mental health)
# 1: rural limited access -- represents ascertainment/surveillance bias
#    moderate poverty, low capacity, potentially undercounting burden
# 2: well-resourced; low burden, high cpacity, lowest poverty

# Confirm why (?) cluster 1 has that pattern

cluster_names = {0: 'High Need, Under-Resourced',
    1: 'Under-Resourced, Moderate Need',
    2: 'Well-Resourced'}
master['cluster_name'] = master['cluster_labels'].map(cluster_names)

print(master['cluster_name'].value_counts())

print(master[master['cluster_name'] == 'High Need, Under-Resourced'][['county', 'burden_score', 'capacity_score', 'gap_index']].sort_values('gap_index', ascending=False))

master.to_csv('data/master.csv', index=False)
print("Saved master.csv with cluster labels")
print(master[['county', 'cluster_labels', 'cluster_name']].head())