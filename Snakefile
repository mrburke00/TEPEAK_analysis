exts = ['png', 'pdf']
sra_to_breed_file='data/horse_sra_final.csv'

rule all:
    input:
      expand('doc/horse_size_freq_hist_log.{ext}', ext = exts),
      expand('doc/horse_size_freq_hist_log.{ext}', ext = exts),
      expand('doc/horse_size_freq_hist.{ext}', ext = exts),
      expand('doc/breed_loci_af_heatmap.{ext}', ext = exts),
      expand('doc/breed_af_histo.{ext}', ext = exts),
      expand('doc/breed_loci_af_heatmap.{ext}', ext = exts),
      expand('doc/pairwise_shared_loci_heatmap.{ext}', ext = exts),
      expand('doc/ere_breed_af.{ext}', ext = exts)

rule size_freq_hist:
    input:
      'data/horse_info.txt'
    output:
      linear = 'doc/horse_size_freq_hist_log.{ext}',
      log = 'doc/horse_size_freq_hist.{ext}'
    params:
      max_size = 1500,
      log_max_size = 8000,
      min_size = 100,
      width = 5,
      height = 4
    shell:
        """
        python src/size_histo.py \
            --sv_info_file {input} \
            --out {output.log} \
            --max_size {params.log_max_size} \
            --min_size {params.min_size} \
            --width {params.width} \
            --height {params.height} \
            --log

        python src/size_histo.py \
            --sv_info_file {input} \
            --out {output.linear} \
            --max_size {params.max_size} \
            --min_size {params.min_size} \
            --width {params.width} \
            --height {params.height} 
        """

rule af_box_plots:
    input:
        breed_file = sra_to_breed_file,
        bed_files = expand('data/ere{i}.bed', i=[1,2,3,4]),
    output:
        'doc/ere_breed_af.{ext}'
    params:
        titles = 'ERE-1 ERE-2 ERE-3 ERE-4',
        min_ac = 0
    shell:
        """
            python src/af_box_plots.py \
                --breed_file {input.breed_file} \
                --bed_files {input.bed_files} \
                --titles {params.titles} \
                --min_ac {params.min_ac} \
                --out_file {output}
        """

rule breed_af_histo:
    input:
        breed_file = sra_to_breed_file,
        ere1_file = 'data/ere1_merged_pop_vcf.bed'
    output:
        'doc/breed_af_histo.{ext}'
    params:
        width = 10,
        height = 6
    shell:
        """
            python src/breed_af_histo.py \
                --breed_file {input.breed_file} \
                --bed_file {input.ere1_file} \
                --out_file {output} \
                --width {params.width} \
                --height {params.height}
        """

rule breed_loci_af_heatmap:
    input:
        breed_file = sra_to_breed_file,
        ere1_file = 'data/ere1_merged_pop_vcf.bed'
    output:
        'doc/breed_loci_af_heatmap.{ext}'
    params:
        width = 2,
        height = 2,
        min_af = 0.75
    shell:
        """
            python src/breed_loci_af_heatmap.py \
                --breed_file {input.breed_file} \
                --bed_file {input.ere1_file} \
                --min_af {params.min_af} \
                --out_file {output} \
                --width {params.width} \
                --height {params.height}
        """


rule pairwise_shared_loci_heatmap:
    input:
        breed_file = sra_to_breed_file,
        ere1_file = 'data/ere1_merged_pop_vcf.bed'
    output:
        'doc/pairwise_shared_loci_heatmap.{ext}'
    params:
        width = 10,
        height = 10,
        min_af = 0.75
    shell:
        """
            python src/pairwise_shared_loci_heatmap.py \
                --breed_file {input.breed_file} \
                --bed_file {input.ere1_file} \
                --min_af {params.min_af} \
                --out_file {output} \
                --width {params.width} \
                --height {params.height}
        """


