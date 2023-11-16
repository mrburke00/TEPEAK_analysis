#FIGURE 3 AND SUPP 1

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_size', type=int, default=200)
    parser.add_argument('--max_size', type=int, default=2000)
    parser.add_argument('--width', type=int, default=3)
    parser.add_argument('--height', type=int, default=3)
    parser.add_argument('--sv_info_file', type=str, required=True)
    parser.add_argument('--out', type=str, required=True)
    parser.add_argument('--log', default=False, action='store_true')
    return parser.parse_args()

def main():
    args = get_args()

    lengths = []

    with open(args.sv_info_file) as lines:
        for line in lines:
            fields = line.rstrip().split()
            if len(fields) >= 4:
                try:
                    length = int(fields[3])
                    if length >= args.min_size and length <= args.max_size:
                        lengths.append(length)
                except ValueError:
                    continue

    fig, ax = plt.subplots(figsize=(args.width, args.height))
    #ax.hist(t_rows['length'], density=False, bins=len(t))
    ax.hist(lengths, density=False, bins=len(set(lengths)))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Insertion Size (bp)')

    if args.log:
        ax.set_yscale('log')
        ax.set_ylabel('log(Frequency)')

    fig.tight_layout()
    fig.savefig(args.out)

if __name__ == '__main__':
    main()
