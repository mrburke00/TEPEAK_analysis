import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#FIGURE 3 AND SUPP 1

#####REQUIRED VARIABLES######
min_size = '200' # determines minimum and maximum bp range for histogram THEY ARE STRINGS FOR A REASON
max_size = '2000'
species = "horse"  # takes in overall VCF pop info file for each species
############################################################



sv_info_file = species+'_info.txt'

df = pd.read_csv(sv_info_file, sep='\t', lineterminator='\n')
df.columns = ['chrom','start','end','length','seq','species']

df['length'].value_counts()
df = df[df['length']!='.']

#### if you get NaN error run this first line and then delete whatever index is causing the error
print(df[df['length'].isnull()])
df = df.drop(73676)
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
#plt.ylabel('log(Frequency)')

plt.ylabel('Frequency')
plt.xlabel('Insertion Size (bp)')

plt.show()