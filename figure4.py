import string
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

overall_entries = [[],[],[],[]]
overall_loci = [[],[],[],[]]
lengths = []

cluster_files = ['1-100000.csv','100000-200000.csv',\
                '200000-300000.csv', '300000-400000.csv',\
                '400000-500000.csv', '400000-500000.csv', \
                '500000-526675.csv'] 
sra_info_file = 'horse_sra_simple2.csv'

breed_samples_count = {'QUARTER HORSE': 27, 'THOROUGHBRED': 26, 'ARABIAN': 26, \
                       'MONGOLIAN': 26, 'TIBETAN': 21, 'STANDARDBRED': 15, \
                       'JEJU HORSE': 14, 'FREIBERGER': 13,  \
                       'AKHAL-TEKE': 11, 'FRIESIAN': 9, 'HANOVERIAN': 10}
                       
#cluster_files = ['data/horse/1-10000.csv']
for ere1_cluster in cluster_files:
    with open(ere1_cluster) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            #print("lenlines",i, len(lines))
            ere_entries = lines[i].split('","')
            entries = []
            loci = []
            #print(len(ere_entries))
            for line in ere_entries:

                t = line.split()
                #print(t[1])

                t[0] = t[0].replace('"', '')
                t[0] = t[0].replace("'", '')
                x = t[0].replace('(', '')

                x = x.split(',')
                entry = x[0]+","+x[1]+","+x[2]


                t = line.split()

                t[1] = t[1].replace("'", '')
                y = t[1].replace(",", '')

                if entry not in loci:
                    loci.append(entry)
                entries.append((entry,y))
            #print(len(loci))
            #print(len(entries))
            overall_entries[i].extend(entries)
            overall_loci[i].extend(loci)
        print('newfile')
print(len(overall_loci[0]))
print(len(overall_entries[0]))
meta_data = pd.read_csv(sra_info_file)
meta_data=meta_data.dropna(axis=1, how='all')
meta_data=meta_data.dropna(axis=0, how='all')

if len(meta_data.columns) > 2:
    meta_data = meta_data.drop(meta_data.columns[2:len(meta_data.columns)], axis=1)
meta_data.columns = ['sra','breed']
#print(meta_data['breed'].value_counts())

overall_samples=[]
for j,entry in enumerate(overall_entries):
    samples={}
    loci = overall_loci[j]
    for i,(coord, sample_name) in enumerate(entry):
        if sample_name in meta_data['sra'].values:
            breed_name = meta_data.loc[meta_data['sra'] == sample_name]['breed'].values[0]
            if breed_name not in samples.keys():
                samples[breed_name] = np.zeros(len(loci))
            if coord.split(',')[0] not in ['X', 'Y']: # check which SV in reference to TE loci 
                idx = loci.index(coord)
                samples[breed_name][idx] += 1
    overall_samples.append(samples)


df_ere1=pd.DataFrame.from_dict(overall_samples[0],orient='index').transpose()
df_ere2=pd.DataFrame.from_dict(overall_samples[1],orient='index').transpose()
df_ere3=pd.DataFrame.from_dict(overall_samples[2],orient='index').transpose()
df_ere4=pd.DataFrame.from_dict(overall_samples[3],orient='index').transpose()
#print(df_ere1)
for df in [df_ere1,df_ere2,df_ere3,df_ere4]:
    for i, row in df.iterrows():
        for breed_name in list(row.index):
            t = row[breed_name]/breed_samples_count[breed_name]
            if t > 1:
                t = 1
            row[breed_name] = t

fig, ax = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(9,9))
#print(df_final.columns.tolist())
breeds = ['QUARTER HORSE', 'THOROUGHBRED', 'MONGOLIAN', 'AKHAL-TEKE', \
         'FREIBERGER', 'JEJU HORSE', 'TIBETAN', 'ARABIAN', 'STANDARDBRED']
#print(n_cols)
#del n_cols[4]
#del n_cols[3]
for i in range(3):
    for j in range(3):
        breed = breeds[i*3+j]
        ax1=ax[i,j]
        ax1.boxplot([[i for i in df_ere1[breed].values.tolist() if i  > 0.1], \
             [i for i in df_ere2[breed].values.tolist() if i > 0.1], \
             [i for i in df_ere3[breed].values.tolist() if i > 0.05], \
             [i for i in df_ere4[breed].values.tolist() if i > 0.05], \
            ], labels=['ERE-1', 'ERE-2', 'ERE-3', 'ERE-4'])
        
        ax1.set_ylim(0,0.75)
        ax1.set_title(breed, fontsize=10, loc='center', y=1.0)
        ax1.tick_params(axis='x', labelsize=12)
plt.show()