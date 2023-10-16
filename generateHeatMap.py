import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

# PANEL 5 A

# can also change the centering of the heatmap scale in the clustermap() call below
# NOTE the LTR heatmap (FIG 9) currently in the paper is not made in this script SEE LTRvsERV2.py
#####REQUIRED VARIABLES######
#cluster_file = 'ere1_merged_pop_vcf.bed'
cluster_file = 'ltr_merged_pop_vcf.bed'
af_threshold = 0.25 #determines the loci allele frequency threshold dropout for panel 1 this was set at 0.75
############################################################

sra_info_file = 'horse_sra_simple2.csv'


breed_samples_count = {'QUARTER HORSE': 27, 'THOROUGHBRED': 26, 'ARABIAN': 26, \
					   'MONGOLIAN': 26, 'TIBETAN': 21, 'STANDARDBRED': 15, \
					   'JEJU HORSE': 14, 'FREIBERGER': 13,  \
					   'AKHAL-TEKE': 11, 'FRIESIAN': 9, 'HANOVERIAN': 10}

entries = []
loci = []
lengths = []
with open(cluster_file) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		#if line[0] not in ['X','Y']:
		t = line[0]+","+line[1]+","+str(line[2])
		if t not in loci:
			loci.append(t)
		entries.append((t,line[-1]))
		
meta_data = pd.read_csv(sra_info_file)
meta_data=meta_data.dropna(axis=1, how='all')
meta_data=meta_data.dropna(axis=0, how='all')

if len(meta_data.columns) > 2:
	meta_data = meta_data.drop(meta_data.columns[2:len(meta_data.columns)], axis=1)
meta_data.columns = ['sra','breed']

samples={}
for i,(coord, sample_name) in enumerate(entries):
	if sample_name in meta_data['sra'].values:
		breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
		if breed_name not in samples.keys():
			samples[breed_name] = np.zeros(len(loci))
			#samples[breed_name] = [0]*len(loci)
		if coord.split(',')[0] not in ['X', 'Y']: # check which SV in reference to TE loci 
			idx = loci.index(coord)
			samples[breed_name][idx] += 1
df=pd.DataFrame.from_dict(samples,orient='index').transpose()
cols = list(df.columns.values)
cols = sorted(cols, key=str.lower)
df_new = df[cols]
df_final = df_new
for i,row in df_final.iterrows():
	for breed_name in list(row.index):
		t = (row[breed_name]/breed_samples_count[breed_name])       
		if t > 1:
			t = 1
		row[breed_name] = t
		

for i,row in df_final.iterrows():
	rare_allele = True
	for breed_name in list(row.index):
		if row[breed_name] > af_threshold:
			rare_allele = False
			break
	if rare_allele:
		df_final = df_final.drop(i, axis = 0)
		df_final.reset_index(drop=True)
		
clustermap = sns.clustermap(df_final.T, cmap = 'coolwarm',center=.50, yticklabels=True)#,cmap = 'rocket')
#sns.set(rc={'font.family': 'serif'})
cbar_ax = clustermap.ax_heatmap.figure.axes[-1]
cbar_ax.set_yticklabels(['0', '0.25', '0.50', '0.75', '1.0'])
clustermap.tick_params(axis='both', labelsize=14)
clustermap.ax_col_dendrogram.set_visible(False)
plt.show()