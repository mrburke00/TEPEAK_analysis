merged_loci_bed = "merged_ltr_erv_intersection_test.bed"
bed_loci = "ltr_erv_test.bed"
output_file = "test3.bed"

loci = []
with open(bed_loci) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		loci.append(line)
		
merged_loci = []
with open(merged_loci_bed) as f:
	lines = f.readlines()
	for line in lines:
		line = line.split()
		merged_loci.append((line[0],line[1],line[2]))
		

new_loci = []
for l in loci:
	for m in merged_loci:
		if l[0] == m[0]:
			if l[2] >= m[1] and l[1] <= m[2]:
				l[0] = m[0]
				l[1] = m[1]
				l[2] = m[2]
				
with open(output_file, 'w') as r:
	for l in loci:
		r.write(l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4] + '\n')
print('done')