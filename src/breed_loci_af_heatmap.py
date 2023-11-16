import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns 
import breed_af_histo
import pandas as pd

def get_common_loci(af, breeds, min_af):
    all_loci = []
    for breed in af:
        for locus in af[breed]:
            if locus not in all_loci:
                all_loci.append(locus)

    common_loci = []
    for locus in all_loci:
        for breed in breeds:
            if locus in af[breed] and af[breed][locus] >= min_af:
                common_loci.append(locus)

    return list(set(common_loci))

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

    common_loci = get_common_loci(af, breeds, args.min_af)

    datas = []
    for breed in breeds:
        data = []
        for locus in common_loci:
            if locus in af[breed]:
                data.append( af[breed][locus] ) 
            else:
                data.append( 0 )
        datas.append(data)

    df = pd.DataFrame(datas, index=breeds)
    clustermap = sns.clustermap(df,
                                cmap = 'coolwarm',
                                center=.5,
                                dendrogram_ratio=(.1, 0.0),
                                cbar_pos=(0.95, 0.88, .01, .1),
                                yticklabels=True,
                                figsize=(5,5))#,cmap = 'rocket')
    clustermap.ax_col_dendrogram.set_visible(False)
    plt.savefig(args.out_file)

if __name__ == '__main__':
    main()
