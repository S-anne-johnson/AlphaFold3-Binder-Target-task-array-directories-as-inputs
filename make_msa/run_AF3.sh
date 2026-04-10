#!/bin/bash
#SBATCH -J af3
#SBATCH --partition=gpu-a4000
#SBATCH -c 16
#SBATCH --gpus=1
#SBATCH --mem=16g
#SBATCH -t 8:00:00

# Create an array of JSON files in your directory
json_files=(/scratch/snorlax/saj027/saj027_projects/250616_mmpl3_AF-A0QP27/make_msa/Prep/jsons/*.json)

# Get the JSON file corresponding to the current task index
json_file=${json_files[$SLURM_ARRAY_TASK_ID]}

echo "Processing ${json_file}"

eval "$(/home/nbethel/Software/ls/bin/conda shell.bash hook)"

#Load python environment
conda activate /home/nbethel/Software/ls/envs/af3

ALPHAFOLD3DIR="/software/alphafold3"

HMMER3_BINDIR="/software/hmmer/bin"

DB_DIR="/home/nbethel/public_databases"

MODEL_DIR="/software/alphafold3/models"

python /software/alphafold3/run_alphafold.py \
        --jackhmmer_binary_path="${HMMER3_BINDIR}/jackhmmer" \
        --nhmmer_binary_path="${HMMER3_BINDIR}/nhmmer" \
        --hmmalign_binary_path="${HMMER3_BINDIR}/hmmalign" \
        --hmmsearch_binary_path="${HMMER3_BINDIR}/hmmsearch" \
        --hmmbuild_binary_path="${HMMER3_BINDIR}/hmmbuild" \
        --db_dir="${DB_DIR}" \
        --model_dir="${MODEL_DIR}" \
        --json_path="${json_file}" \
        --output_dir="AF3_outputs" \
        --buckets="256,512,768,1024,1280,1536,2048,2560,3072,3584,4096,4608,5120"

