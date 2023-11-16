import pandas as pd 
import re
import random
import numpy as np
import string
import matplotlib.pyplot as plt
import seaborn as sns 
import breed_af_histo
import breed_loci_af_heatmap
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_af', type=float, default=0.5)
    parser.add_argument('--breed_file', type=str, required=True)
    parser.add_argument('--bed_file', type=str, required=True)
    parser.add_argument('--height', type=int, default=8)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--out_file', type=str, required=True)
    return parser.parse_args()

def main():
    args = get_args()

    sr_to_breed = breed_af_histo.get_sr_to_breed(args.breed_file)

    breeds = sorted(list(set(sr_to_breed.values())))

    af = breed_af_histo.get_breed_locus_af(args.bed_file, sr_to_breed)

    common_loci = breed_loci_af_heatmap.get_common_loci(af,
                                                        breeds,
                                                        args.min_af)
    shared_loci = []

    for breed_a in breeds:
        sharing = [0] * len(breeds)
        for i, breed_b in enumerate(breeds):
            if breed_a == breed_b : sharing[i] = np.nan 
            for loci in common_loci:
                if  loci in af[breed_a] and \
                    loci in af[breed_b] and \
                    af[breed_a][loci] >= args.min_af and \
                    af[breed_b][loci] >= args.min_af:
                        sharing[i] += 1
        shared_loci.append(sharing)

    df = pd.DataFrame(shared_loci, index=breeds, columns=breeds)
    df.set_axis(breeds)

    plt.figure(figsize=(10, 8))
    g = clustermap = sns.heatmap(df, cmap='coolwarm')
    g.set_facecolor('black')
    plt.title(f'Number of Shared Loci for Each Breed Pair')
    plt.tight_layout()
    plt.savefig(args.out_file)

if __name__ == '__main__':
    main()
