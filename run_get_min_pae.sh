#!/bin/bash
#SBATCH -J processing
#SBATCH --partition=cpu
#SBATCH -c 1
#SBATCH --mem=16g

#Add python executable to path
eval "$(/home/saj027/miniforge3/bin/conda shell.bash hook)"

#Load python environment
conda activate /home/saj027/miniforge3/envs/Everything

python Get_min_pae_script.py 
