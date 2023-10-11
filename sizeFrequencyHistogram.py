import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


%matplotlib inline
min_size = '200'
max_size = '1000'
species = "horse"
data_dir = "../sv_analysis/data/"
sv_info_file = data_dir+species+'/'+species+'_info_265.txt'


df = pd.read_csv(sv_info_file, sep='\t', lineterminator='\n')
df.columns = ['chrom','start','end','length','seq','species']

df['length'].value_counts()
df = df[df['length']!='.']

#### if you get NaN error run this first line and then delete whatever index is causing the error
#print(df[df['length'].isnull()])
#df = df.drop(73676)
####

df['length'] = df['length'].astype(int)
df['length'].value_counts()
t_rows = df.query('length >= ' + min_size)
t_rows = t_rows.query('length <=  ' + max_size)
t = t_rows['length'].value_counts()

### Use this to print the top N frequencies (helps when trying to narrow down a range)
#print(t[0:20])
#mean = t.sum()
#print(mean)
###

plt.hist(t_rows['length'], density=False, bins=len(t))
#plt.yscale('log')
plt.ylabel('log(Frequency)')
plt.xlabel('Insertion Size (bp)')