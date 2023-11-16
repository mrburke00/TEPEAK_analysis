import numpy as np
import matplotlib.pyplot as plt
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_ac', type=int, default=0)
    parser.add_argument('--breed_file', type=str, required=True)
    parser.add_argument('--bed_files', type=str, nargs='+', required=True)
    parser.add_argument('--titles', type=str, nargs='+', required=True)
    parser.add_argument('--height', type=int, default=8)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--out_file', type=str, required=True)
    return parser.parse_args()

def get_sr_to_breed(file):
    sr_to_breed = {} 
    with open(file, mode='r', encoding='utf-8-sig') as lines:
        for line in lines:
            A = line.rstrip().split(',')
            if len(A) == 2:
                sr_to_breed[A[0]] = A[1]
    return sr_to_breed


def main():
    args = get_args()

    sr_to_breed = get_sr_to_breed(args.breed_file)

    breeds = sorted(list(set(sr_to_breed.values())))

    breed_count = {}

    fig, axs = plt.subplots(len(args.bed_files),1, figsize=(8,8))

    ax_i = 0
    for bed_file in args.bed_files:
        with open(bed_file) as lines:
            af = {}

            for line in lines:
                A = line.rstrip().split()

                loci = (A[0], A[1], A[2])
                sr = A[3]

                breed = sr_to_breed[sr]
                if breed not in breed_count:
                    breed_count[breed] = {}
                if sr not in breed_count[breed]:
                    breed_count[breed][sr] = 0
                breed_count[breed][sr] = breed_count[breed][sr] + 1

                if breed not in af:
                    af[breed] = {}
                if loci not in af[breed]:
                    af[breed][loci] = 0

                af[breed][loci] = af[breed][loci] + 1

            D = []
            for breed in breeds:
                d = []
                for loci in af[breed]:
                    if af[breed][loci] >= args.min_ac:
                        d.append(af[breed][loci] / len(breed_count[breed]))
                D.append(d)

            axs[ax_i].boxplot(D)
            axs[ax_i].set_title(args.titles[ax_i],
                                loc='left')
            axs[ax_i].set_xticklabels([])
            axs[ax_i].set_ylabel('')

            ax_i += 1

    axs[ax_i - 1].set_xticklabels(breeds)
    plt.setp(axs[ax_i - 1].get_xticklabels(),
             rotation=30,
             va='top',
             ha='right')

    max_y = max(ax.get_ylim()[1] for ax in axs)

    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim((0, max_y))


    fig.tight_layout()
    fig.savefig(args.out_file)

if __name__ == '__main__':
    main()
