from Bio import Align
#
ERE1='GACCAGTGTGGGGGGGCTGGCCCCGTGGCCGAGTGGTTAAGTTCGCGCGCTCTGCTGCAGGCGGCCCAGTGTTTCGTTGGTTCGAATCCTGGGCGCGGACATGGCACTGCTCATCAAAACCAGGCTGAGGCGGCGTCCCACATACCACAACTAGAAGAATCCACAACGAAGAATATACAACTATGTACCGGGGGGCTTTGGGGAGAAAAAGGAAATAATAAAATCTTTAAAAAAAAAAAAAAAAAAAAAGACCAGTGTG'
#
aligner = Align.PairwiseAligner()
#
#i = 0
#with open('../data/horse_info.txt') as lines:
#    for line in lines:
#        A = line.rstrip().split()
#        alignments = aligner.align(ERE1, A[4])
#        print(alignments.score)
#        i+=1
#        if i == 1000: break
##
##for alignment in sorted(alignments):
##    print("Score = %.1f:" % alignment.score)
##    print(alignment)

#"('X,41867022,41867022', 'SRR19364619', 'AAATGTAA')","('X,41867022,41867022', 'SRR19364619', 'AAATGTAA')"

import csv
import io

cluster_files = ['../data/1-100000.csv',
                 '../data/100000-200000.csv',
                 '../data/200000-300000.csv',
                 '../data/300000-400000.csv',
                 '../data/400000-500000.csv',
                 '../data/500000-526675.csv']

out_file_names = ['../data/ere1.bed', '../data/ere2.bed', '../data/ere3.bed', '../data/ere4.bed']

out_files = [open(file, 'w') for file in out_file_names]

for cluster_file in cluster_files:
    print(cluster_file)
    with open(cluster_file) as lines:
        file_i = 0
        for line in lines:
            A = line.rstrip().split('","')
            for a in A:
                c,s,e,srr,seq = a.replace('"', '').replace("'", '').replace('(', '').replace(')', '').replace(' ','').split(',')
                out_files[file_i].write( '\t'.join([c, s, e, srr, seq]) + '\n')
            file_i += 1

for out_file in out_files:
    out_file.close()
