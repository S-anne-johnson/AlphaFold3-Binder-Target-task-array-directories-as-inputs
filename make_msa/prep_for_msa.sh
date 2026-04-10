#!/bin/bash
#SBATCH -J AF3_prep
#SBATCH --partition=cpu
#SBATCH -c 1
#SBATCH --mem=8g
#SBATCH -t 01:00:00

#Add python executable to path
eval "$(/home/nbethel/Software/ls/bin/conda shell.bash hook)"

#Load python environment
conda activate /home/nbethel/Software/ls/envs/pyrosetta

#Run parsing script
python /scratch/snorlax/saj027/saj027_projects/250616_mmpl3_AF-A0QP27/make_msa/make_msa_sep_fastas_and_gen_jsons_multichain.py \
--proteinmpnn_directory /scratch/snorlax/saj027/saj027_projects/250616_mmpl3_AF-A0QP27/make_msa \
--output_directory Prep/ \
--num_seqs 4


