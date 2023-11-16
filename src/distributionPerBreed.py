import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

# FIGURE 5 C

## Note because of the odd number of breeds I ended up doing a 3x3 and then just adding the last two 
# in illustrator. You can use the del n_cols[] command after line 80 to cycle the remaining two breeds
# right now its only going to make figures for 9 out of the 11 breeds. 

####REQUIRED VARIABLES######
cluster_file = "ere1_merged_pop_vcf.bed"
#cluster_file = "ltr_merged_pop_vcf.bed"
####################################################

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
        t = row[breed_name]/breed_samples_count[breed_name]
        if t > 1.0:
            t = 1.0
        row[breed_name] = t
for i,row in df_final.iterrows():
    rare_allele = True
    for breed_name in list(row.index):
        if row[breed_name] > 0:
            rare_allele = False
            break
    if rare_allele:
        df_final = df_final.drop(i, axis = 0)
        df_final.reset_index(drop=True)


def normaliseCounts(widths,maxwidth):
    widths = np.array(widths)/float(maxwidth)
    return widths



fig, ax = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(12, 2.75))
n_cols = df_final.columns.tolist()

#del n_cols[4]
#del n_cols[3]


for i in range(3):
    for j in range(3):
        col_name = n_cols[i*3+j]
        print(col_name)
        vals = df_final[col_name].values.tolist()
        vals = [value for value in vals if value != 0]
        ax1=ax[i,j]
        ax1.hist(vals, bins = 15, width=0.05, color='#0080FF')#
        

        ax1.set_xlim(0, 1.0)
        ax1.set_ylim(0,2500)
        ax1.set_ylabel('')
        ax1.set_xticks([0,0.5,1])
        ax1.set_title(col_name, fontsize=9, loc='right', y=.75)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.tick_params(axis='y', labelsize=8)
        ax1.tick_params(axis='x', labelsize=8)

ax1 = ax[2,1]
ax1.set_xlabel('Allele Frequency', fontsize=14, labelpad=10)
ax1 = ax[1,0]
ax1.set_ylabel('Frequency', fontsize=14, labelpad=10)
plt.show()