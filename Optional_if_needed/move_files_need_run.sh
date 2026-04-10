#!/bin/bash
#SBATCH -J move
#SBATCH --partition=cpu
#SBATCH -c 1
#SBATCH --mem=16g
#SBATCH -t 1:00:00

#Add python executable to path
eval "$(/home/saj027/miniforge3/bin/conda shell.bash hook)"

#Load python environment
conda activate /home/saj027/miniforge3/envs/SE3nv

python move_files_need_run.py
