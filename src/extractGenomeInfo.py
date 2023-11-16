import pandas as pd
import re
import random
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns 


meta_data_file = 'horse/horse_sra_simple2.csv'

gcf_annotated_file = 'data/horse/ltr_gcf_merged.txt'
loci_annotated_file = 'data/horse/ltr_loci_merged.bed'
vcf_file = 'data/horse/ltr_merged_pop_loci_final.bed' 

intersection_type = 'exon' #exon, gene, CDS

breed_samples_count = {'QUARTER HORSE': 27, 'THOROUGHBRED': 26, 'ARABIAN': 26, \
					   'MONGOLIAN': 26, 'TIBETAN': 21, 'STANDARDBRED': 15, \
					   'JEJU HORSE': 14, 'FREIBERGER': 13,  \
					   'AKHAL-TEKE': 11, 'FRIESIAN': 9, 'HANOVERIAN': 10}


sra_info_file = 'data/horse/horse_sra_simple2.csv'
meta_data = pd.read_csv(sra_info_file)
meta_data=meta_data.dropna(axis=1, how='all')
meta_data=meta_data.dropna(axis=0, how='all')

if len(meta_data.columns) > 2:
	meta_data = meta_data.drop(meta_data.columns[2:len(meta_data.columns)], axis=1)
meta_data.columns = ['sra','breed']

df = pd.read_csv(loci_annotated_file, sep='\t', comment='t', header=None)

header = ['chrom', 'chromStart', 'chromEnd','sname', 'gene_id', 'gene_name', 'type']
df.columns = header[:len(df.columns)]
breed_names = []
idx_to_remove = []
for idx, row in df.iterrows():
	breed_name = meta_data.loc[meta_data['sra'] == row['sname']]['breed'].values
	if len(breed_name) > 0:
		breed_names.append(breed_name[0])
	else:
		idx_to_remove.append(idx)
df = df.drop(idx_to_remove)        
df['breed_name'] = breed_names

df_type = df.drop_duplicates(subset=['chrom', 'chromStart', 'chromEnd','sname','gene_id','type'])


df_type = df_no_duplicates[df_no_duplicates['type'] == intersection_type]

print(*df_type['gene_id'].value_counts().head(1000).index.tolist(), sep = ' ')
grouped_df = df_type.groupby(['breed_name', 'gene_id']).size().reset_index(name='count')
grouped_df = grouped_df.sort_values(by=['breed_name','count'], ascending=False)


grouped_df = df_type.groupby(['breed_name', 'gene_id']).size().reset_index(name='count')
# Step 1: Calculate Gene Occurrences Per Breed
gene_occurrences_per_breed = grouped_df.groupby(['breed_name', 'gene_id'])['count'].sum().reset_index()

# Step 2: Calculate Total Occurrences for Each Gene
total_occurrences_per_gene = gene_occurrences_per_breed.groupby('gene_id')['count'].sum().reset_index()

# Step 3: Merge DataFrames to Calculate Proportion
merged_df = pd.merge(gene_occurrences_per_breed, total_occurrences_per_gene, on='gene_id', suffixes=('_breed', '_total'))

# Step 4: Calculate Proportion of Occurrences in Each Breed
merged_df['Proportion'] = merged_df['count_breed'] / merged_df['count_total']

# Step 5: Rank Genes by Proportion
gene_ranks = merged_df.sort_values(by=['gene_id','breed_name'], ascending=[False,False])
#gene_ranks = gene_ranks.groupby('breed_name').head(1)

# Displaying the result
print(gene_ranks)
#valid_genes = gene_ranks[gene_ranks['count_total'] >= 15]['gene_id']
#print(valid_genes)
#df_filtered = gene_ranks[gene_ranks['gene_id'].isin(valid_genes)]
df_filtered.to_csv("ere1_intron.csv", index=False)