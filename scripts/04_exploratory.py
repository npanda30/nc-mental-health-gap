import pandas as pd
import matplotlib.pyplot as plt

master = pd.read_csv('data/master.csv')

top15 = master.sort_values('gap_index', ascending=False).head(15)

fig, ax = plt.subplots(figsize=(10,6))

ax.barh(top15['county'], top15['gap_index'], color='steelblue')
ax.invert_yaxis()
ax.set_xlabel('Gap Index (burden minus capacity, z-scores)')
ax.set_title('Top 15 Most Underserved NC Counties\nMental Health Crisis Burden vs. Response Capacity')
ax.axvline(x=0, color='black', linewidth=0.8, linestyle='--')

plt.tight_layout()
plt.savefig('outputs/gap_index_top15.png', dpi=150)
plt.show()
print("Saved to outputs/gap_index_top15.png")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

fig, ax = plt.subplots(figsize=(10, 8))

scatter = ax.scatter(
    master['capacity_score'], 
    master['burden_score'],
    c=master['gap_index'],
    cmap='RdYlGn_r',
    alpha=0.8, s=80,
    vmin=master['gap_index'].min(),
    vmax=master['gap_index'].max()
)

plt.colorbar(scatter, ax=ax, label='Gap Index (higher = more underserved)')

for _, row in master.iterrows():
    if row['gap_index'] > 1.8:
        ax.annotate(row['county'],
                    (row['capacity_score'], row['burden_score']),
                    fontsize=8, xytext=(5, 5),
                    textcoords='offset points')

ax.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
ax.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
ax.set_xlabel('Capacity Score (z-score of provider rate)')
ax.set_ylabel('Burden Score (z-score of ED visit rates)')
ax.set_title('Mental Health Crisis Burden vs. Response Capacity\nAll 100 NC Counties')

plt.tight_layout()
plt.savefig('outputs/burden_vs_capacity.png', dpi=150)
plt.show()

si_all = pd.read_csv('data/si_trend.csv')

top6 = ['Anson', 'Edgecombe', 'Alexander', 'McDowell', 'Scotland', 'Wilson']
si_top6 = si_all[si_all['county'].isin(top6)]

fig, ax = plt.subplots(figsize=(10, 6))

for county in top6:
    data = si_top6[si_top6['county'] == county]
    ax.plot(data['year'], data['si_crude_rate'], marker='o', label=county)

ax.set_xlabel('Year')
ax.set_ylabel('Suicidal Ideation ED Visit Rate (per 10,000)')
ax.set_title('Suicidal Ideation ED Visit Trends\nTop 6 Most Underserved NC Counties (2017–2024)')
state_avg = si_all.groupby('year')['si_crude_rate'].mean().reset_index()
ax.plot(state_avg['year'], state_avg['si_crude_rate'], 
        color='black', linewidth=2, linestyle='--', 
        marker='s', label='NC State Average')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/si_trends_top6.png', dpi=150)
plt.show()
print("Saved to outputs/si_trends_top6.png")