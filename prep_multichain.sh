#!/bin/bash
#SBATCH -J AF3_prep
#SBATCH --partition=cpu
#SBATCH -c 1
#SBATCH --mem=8g

module load conda/pyrosetta/2025.23 

#Run parsing script
python sep_fastas_and_gen_jsons_multichain.py \
--proteinmpnn_directory /scratch/snorlax/saj027/saj027_projects/251125-251201_MPNN_MD_tb/MPNN_outputs/alignments \
--output_directory Prep_AF3/ \
--num_seqs 3


