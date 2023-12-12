from Bio import Align
import sys

def reverse_complement(dna_sequence):
    # Define a dictionary to map nucleotides to their complements
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    # Reverse the DNA sequence using slicing
    reversed_sequence = dna_sequence[::-1]

    # Use a list comprehension to replace each nucleotide with its complement
    complement_sequence = [complement_dict[n] for n in reversed_sequence]

    # Join the list of complemented nucleotides into a string
    return ''.join(complement_sequence)



#ERE1='GACCAGTGTGGGGGGGCTGGCCCCGTGGCCGAGTGGTTAAGTTCGCGCGCTCTGCTGCAGGCGGCCCAGTGTTTCGTTGGTTCGAATCCTGGGCGCGGACATGGCACTGCTCATCAAAACCAGGCTGAGGCGGCGTCCCACATACCACAACTAGAAGAATCCACAACGAAGAATATACAACTATGTACCGGGGGGCTTTGGGGAGAAAAAGGAAATAATAAAATCTTTAAAAAAAAAAAAAAAAAAAAAGACCAGTGTG'
aligner = Align.PairwiseAligner()
alignments = aligner.align(sys.argv[1], sys.argv[2])
rev_alignments = aligner.align(sys.argv[1], reverse_complement(sys.argv[2]))
print(alignments.score, rev_alignments.score)
