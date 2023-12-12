import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


import argparse
import seaborn as sns 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--breed_file', type=str, required=True)
    parser.add_argument('--bed_file', type=str, required=True)
    parser.add_argument('--height', type=int, default=8)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--out_file', type=str, required=True)
    return parser.parse_args()

def get_sr_to_breed(file):
    sr_to_breed = {} 
    header = None
    with open(file, mode='r', encoding='utf-8-sig') as lines:
        for line in lines:
            if header is None:
                header = line
                continue
            if line[0] == '#': continue
            A = line.rstrip().split(',')
            if len(A) == 2 and len(A[0]) > 0 and len(A[1]) > 0:
                sr_to_breed[A[0]] = A[1]
    return sr_to_breed

def get_breed_locus_af(file, sr_to_breed):
    breed_count = {}
    
    loci = {}

    ac = {}
    with open(file) as lines:
        for line in lines:
            A = line.rstrip().split()

            locus = (A[0], A[1], A[2])

            if locus not in loci:
                loci[locus] = 1

            sr = A[4]

            if sr not in sr_to_breed: continue

            breed = sr_to_breed[sr]
            if breed not in breed_count:
                breed_count[breed] = {}
            if sr not in breed_count[breed]:
                breed_count[breed][sr] = 0
            breed_count[breed][sr] = breed_count[breed][sr] + 1

            if breed not in ac:
                ac[breed] = {}
            if locus not in ac[breed]:
                ac[breed][locus] = {}
            if sr not in ac[breed][locus]:
                ac[breed][locus][sr] = 0

            ac[breed][locus][sr] = ac[breed][locus][sr] + 1

    # convert from allele count to allele freq
    af = {}
    for breed in ac:
        af[breed] = {}
        for locus in ac[breed]:
            if len(ac[breed][locus]) == 0 : print (breed, locus)
            af[breed][locus] = len(ac[breed][locus]) / len(breed_count[breed])

    return af
 
def main():
    args = get_args()

    sr_to_breed = get_sr_to_breed(args.breed_file)

    breeds = sorted(list(set(sr_to_breed.values())))

    af = get_breed_locus_af(args.bed_file, sr_to_breed)

    fig = plt.figure(layout="constrained", figsize=(args.width,args.height))
    gs = GridSpec(4, 6, figure=fig)

    gs_order = [gs[0,0:2], gs[0,2:4], gs[0,4:6],
                gs[1,0:2], gs[1,2:4], gs[1,4:6],
                gs[2,0:2], gs[2,2:4], gs[2,4:6],
                gs[3,1:3], gs[3,3:5]]

    ax_i = 0
    for breed in breeds:
        D = []
        for locus in af[breed]:
            D.append(af[breed][locus])
        ax = fig.add_subplot(gs_order[ax_i])
        ax.hist(D, bins=20, width=0.05, color='#0080FF')
        ax.set_title(breed, loc='left')
        ax.set_xlim((0,1))
        ax.set_yscale('log')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_ylabel('Freq.')
        ax.set_xlabel('ERE-1 allele freq.')

        ax_i += 1

    fig.tight_layout()
    plt.savefig(args.out_file)

if __name__ == '__main__':
    main()
