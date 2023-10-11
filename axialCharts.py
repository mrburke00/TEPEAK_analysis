import pandas as pd
import re
import random
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns 

df_fig = pd.read_csv('data/ere1_intron.csv')


df_fig['count_breed'] = df_fig['count_breed'] / 26 # gets allele frequency
df_fig['count_breed'] = df_fig['count_breed'].where(df_fig['count_breed'] <= 1.0, 1.0)

df_fig = df_fig.drop_duplicates(subset = ['breed_name','gene_id'])
ranges = [(0,0.09), (0.1, 0.5), (0.5, 1)]
counts = {}
for r in ranges:
	mask = (df_fig['count_breed'] > r[0]) & (df_fig['count_breed'] <= r[1])
	counts[r] = df_fig[mask].groupby('breed_name').size()

result = pd.DataFrame(counts)
print(result) ## prints out the number of rare, and common loci per breed


df_fig = df_fig.pivot(index='breed_name', columns='gene_id', values='count_breed')
df_fig.fillna(0, inplace=True)

categories = list(df_fig)
N = len(categories)

 
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))


for i, row in df_fig.iterrows():
	values = row.values.flatten().tolist()
	values += values[:1]
	ax.plot(angles, values, linewidth=2, label=i)
	ax.fill(angles, values, alpha=0.1)


ax.set_title('ERE1 - INTRON', fontsize=14, y=1.05)

# Draw axis lines for each angle and label
#ax.set_xticks(angles[:-1])
#ax.set_xticklabels(categories)
ax.set_xticks([])  # Remove x-axis tick labels and marks
#ax.set_yticks([])  # Remove y-axis tick labels and marks
# To make space for the labels
ax.yaxis.grid(True)

ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

plt.show()