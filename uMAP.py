import pandas as pd 
import plotly.express as px
import pandas as pd
import re
import random
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns 
import umap
cluster_file = "data/horse/ere1_merged_final.bed"
sra_info_file = 'data/horse/horse_pca.csv'
af_threshold = 0.7


breed_samples_count = {'QUARTER HORSE': 27, 'THOROUGHBRED': 26, 'ARABIAN': 26, \
					   'MONGOLIAN': 26, 'TIBETAN': 21, 'STANDARDBRED': 11, \
					   'JEJU HORSE': 14, 'FREIBERGER': 13,  \
					   'AKHAL-TEKE': 11, 'FRIESIAN': 9, 'HANOVERIAN': 10}




def makeColorDict(df):
	df['colors'] = df['breed'].map(dict(zip(df['breed'].unique(),
									   px.colors.qualitative.Alphabet[:len(df['breed'].unique())])))
	return df
entries = []
loci = []
lengths = []
with open(cluster_file) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		#if line[0] not in ['X','Y']:
		t = line[0]+","+line[1]+","+str(line[2])
		#if len(line[3]) > 0 and len(line[3]) < 2000:
		#if line[0] == '22' and int(line[1]) >= 0 and int(line[2]) >= 0 :
		if t not in loci:
			loci.append(t)
		entries.append((t,line[-1]))
meta_data = pd.read_csv(sra_info_file)
meta_data=meta_data.dropna(axis=1, how='all')
meta_data=meta_data.dropna(axis=0, how='all')
print(len(loci))
print(len(entries))
if len(meta_data.columns) > 2:
	meta_data = meta_data.drop(meta_data.columns[2:len(meta_data.columns)], axis=1)
meta_data.columns = ['sra','breed']
meta_data = makeColorDict(meta_data)
breed_rename = []
for index, row in meta_data.iterrows():
	rename = row['breed'] + str(random.randint(0,999))
	breed_rename.append(rename)

samples_breed={}
for i,(coord, sample_name) in enumerate(entries):
	if sample_name in meta_data['sra'].values:
		breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
		if breed_name not in samples_breed.keys():
			samples_breed[breed_name] = np.zeros(len(loci))
		if coord.split(',')[0] not in ['X','Y']: # check which SV in reference to TE loci 
			idx = loci.index(coord)
			samples_breed[breed_name][idx] += 1
meta_data['breed'] = breed_rename    
samples={}
for i,(coord, sample_name) in enumerate(entries):
	if sample_name in meta_data['sra'].values:
		breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
		if breed_name not in samples.keys():
			samples[breed_name] = np.zeros(len(loci))
		if coord.split(',')[0] not in ['X','Y']: # check which SV in reference to TE loci 
			idx = loci.index(coord)
			samples[breed_name][idx] = 1


df=pd.DataFrame.from_dict(samples_breed,orient='index').transpose()
cols = list(df.columns.values)
cols = sorted(cols, key=str.lower)
df_new = df[cols]
df_breeds = df_new

#df_breeds = df_breeds.filter(like='QUARTER HORSE', axis=1)

for i,row in df_breeds.iterrows():
	for breed_name in list(row.index):
		t = row[breed_name]/breed_samples_count[breed_name.rstrip(string.digits)]
		if t > 1:
			t = 1
		row[breed_name] = t

df=pd.DataFrame.from_dict(samples,orient='index').transpose()
cols = list(df.columns.values)
cols = sorted(cols, key=str.lower)
df_new = df[cols]
df_final = df_new

#df_final = df_final.filter(like='QUARTER HORSE', axis=1)

print(df_breeds.shape)
dropped_idxs = []
for i,row in df_breeds.iterrows():
	rare_allele = True
	for breed_name in list(row.index):
		if row[breed_name] > af_threshold:
			rare_allele = False
			break
	if rare_allele:
		dropped_idxs.append(i)
		df_breeds = df_breeds.drop(i, axis = 0)
		df_breeds.reset_index(drop=True)

df_final = df_final.drop(dropped_idxs)
X = np.array(list(df_final.T.values))
umap_model = umap.UMAP(n_components=2, random_state=42)
X_umap = umap_model.fit_transform(X)
y = list(df_final.T.index)

color_map = {'AKHAL-TEKE':'#004949', 'ARABIAN': '#b66dff', 'QUARTER HORSE' : '#DDCC77', \
			'THOROUGHBRED' : '#117733', 'MONGOLIAN' : '#24ff24', 'FRIESIAN' : '#882255', \
			'JEJU HORSE' : '#44AA99', 'TIBETAN' : '#490092', 'STANDARDBRED' : '#ff6db6', \
			'HANOVERIAN' : '#FFCCCC', 'FREIBERGER' : '#BBCCEE'} 

def extract_breed_without_number(breed):
	return ''.join([i for i in breed if not i.isdigit()])

pca_df = pd.DataFrame(
	data=X_umap, 
	columns=['PC1', 'PC2'])
pca_df['target'] = y

pca_df['breed'] = pca_df['target'].apply(extract_breed_without_number)
pca_df['color'] = pca_df['breed'].map(color_map)


plt.figure(figsize=(7, 7)) 


for category, group in pca_df.groupby('breed'):
	plt.scatter(group['PC1'], group['PC2'], label=category, color = group['color'])
plt.gca().set_facecolor('none')
plt.grid(True, linestyle='--', linewidth=0.1, color='gray', alpha=0.7)

plt.legend(loc='upper right',prop={'size': 6.5}), #bbox_to_anchor=(1.25, 1), title='Legend')

plt.xlabel('UMAP1', fontsize=14)
plt.ylabel('UMAP2', fontsize=14)
plt.tick_params(axis='both', labelsize=9)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()