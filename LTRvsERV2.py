import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

#FIGURE 9

# Note if you want to remove the dendogram tree uncomment the second to last line

####REQUIRED VARIABLES######
ltr_file = 'ltr_merged_pop_vcf.bed'
erv_file = 'ltr_erv2_int_final.bed'
####################################################

sra_info_file = 'horse_sra_simple2.csv'



breed_samples_count = {'QUARTER HORSE': 27, 'THOROUGHBRED': 26, 'ARABIAN': 26, \
					   'MONGOLIAN': 26, 'TIBETAN': 21, 'STANDARDBRED': 15, \
					   'JEJU HORSE': 14, 'FREIBERGER': 13,  \
					   'AKHAL-TEKE': 11, 'FRIESIAN': 9, 'HANOVERIAN': 10}



erv_entries = []
erv_loci = []
lengths = []
with open(erv_file) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		t = line[0]+","+line[1]+","+str(line[2])
		if t not in erv_loci:
			erv_loci.append(t)
		erv_entries.append((t,line[-1]))
		
ltr_entries = []
ltr_loci = []
map_idx_erv = []
with open(ltr_file) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		t = line[0]+","+line[1]+","+str(line[2])
		if t not in ltr_loci:
			ltr_loci.append(t)    
		ltr_entries.append((t,line[-1]))
for e in ltr_loci:
	if e in erv_loci:
		map_idx_erv.append(1)
	else:
		map_idx_erv.append(0)


meta_data = pd.read_csv(sra_info_file)
meta_data=meta_data.dropna(axis=1, how='all')
meta_data=meta_data.dropna(axis=0, how='all')

if len(meta_data.columns) > 2:
	meta_data = meta_data.drop(meta_data.columns[2:len(meta_data.columns)], axis=1)
meta_data.columns = ['sra','breed']


ltr_samples={}
for i,(coord, sample_name) in enumerate(ltr_entries):
	if sample_name in meta_data['sra'].values:
		breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
		if breed_name not in ltr_samples.keys():
			ltr_samples[breed_name] = np.zeros(len(ltr_loci))
		if coord.split(',')[0] not in ['X', 'Y']: # check which SV in reference to TE loci 
			idx = ltr_loci.index(coord)
			ltr_samples[breed_name][idx] += 1
erv_samples={}
for i,(coord, sample_name) in enumerate(erv_entries):
	if sample_name in meta_data['sra'].values:
		breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
		if breed_name not in erv_samples.keys():
			erv_samples[breed_name] = np.zeros(len(erv_loci))
		if coord.split(',')[0] not in ['X', 'Y']: # check which SV in reference to TE loci 
			idx = erv_loci.index(coord)
			erv_samples[breed_name][idx] += 1

df_ltr=pd.DataFrame.from_dict(ltr_samples,orient='index').transpose()
cols = list(df_ltr.columns.values)
cols = sorted(cols, key=str.lower)
df_new = df_ltr[cols]
df_ltr = df_new
for i,row in df_ltr.iterrows():
	for breed_name in list(row.index):
		t = (row[breed_name]/breed_samples_count[breed_name])
		if t > 1:
			t = 1
		row[breed_name] = t


for i,row in df_ltr.iterrows():
	rare_allele = True
	for breed_name in list(row.index):
		if row[breed_name] > .25:
			rare_allele = False
			break
	if rare_allele:
		df_ltr = df_ltr.drop(i, axis = 0)
		df_ltr.reset_index(drop=True)


df_erv=pd.DataFrame.from_dict(erv_samples,orient='index').transpose()
cols = list(df_erv.columns.values)
cols = sorted(cols, key=str.lower)
df_new = df_erv[cols]
df_erv = df_new
row_colors = pd.Series(map_idx_erv).map({1: 'gold', 0: 'white'})
clustermap = sns.clustermap(df_ltr, annot=False, row_colors=row_colors, cmap='coolwarm')
#clustermap.ax_col_dendrogram.set_visible(False)
plt.show()