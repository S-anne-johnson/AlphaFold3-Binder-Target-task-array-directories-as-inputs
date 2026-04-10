import os
import sys

path = "/scratch/snorlax/saj027/saj027_projects/251125-251201_AF3_MD_tb/Prep_AF3/jsons"  


#Take jsons folder as input. split into smaller folders.
#for each folder, generate a .sh file that is the AF3 run file for that folder.
#have a .sh file called 'launch all' that launches the jobs dynamically according to if there are enough gpus.


files_per_array = 100

os.makedirs("Launch_AF3", exist_ok=True)

def distribute_files(path, exec_files, output_folder, files_per_array):
    check_dirs = os.listdir(path)
    exec_file_paths = []
    if len(check_dirs) > files_per_array:
        x = len(check_dirs) // files_per_array
        rem = len(check_dirs) % files_per_array
        new_folders_list = x * [files_per_array]
        if rem < 150:
            new_folders_list[-1] = new_folders_list[-1] + rem
        elif rem >= 150:
            new_folders_list.append(rem)
        i = 0
        folder_i = 1  #2  CHANGED
        print(new_folders_list)
        for n in new_folders_list:            #for n in new_folders_list[:-1]: CHANGED
            folder = path + str(folder_i)
            if os.path.exists(folder):
                print(f"Already existing folder: {folder}")
                sys.exit()
            os.makedirs(folder)
            for file in check_dirs[i:i+n]:
                start = path + "/" + file
                end = folder + "/" + file
                os.rename(start,end)
            exec_file_path = exec_files +  "/run_AF3_" + str(folder_i)
            exec_file_paths.append(exec_file_path)
            with open(exec_file_path,"w") as f:
                f.write(f'''#!/bin/bash
#SBATCH -J af3
#SBATCH --partition=gpu-a4000
#SBATCH --gpus=1
#SBATCH --mem=16g
#SBATCH --exclude=mew
#SBATCH --exclude=jigglypuff                        

eval "$(/home/nbethel/Software/ls/bin/conda shell.bash hook)"

#Load python environment
conda activate /home/nbethel/Software/ls/envs/af3

ALPHAFOLD3DIR="/software/alphafold3"

HMMER3_BINDIR="/software/hmmer/bin"

DB_DIR="/home/nbethel/public_databases"

MODEL_DIR="/software/alphafold3/models"

python /software/alphafold3/run_alphafold.py \
        --jackhmmer_binary_path="${{HMMER3_BINDIR}}/jackhmmer" \
        --nhmmer_binary_path="${{HMMER3_BINDIR}}/nhmmer" \
        --hmmalign_binary_path="${{HMMER3_BINDIR}}/hmmalign" \
        --hmmsearch_binary_path="${{HMMER3_BINDIR}}/hmmsearch" \
        --hmmbuild_binary_path="${{HMMER3_BINDIR}}/hmmbuild" \
        --db_dir="${{DB_DIR}}" \
        --model_dir="${{MODEL_DIR}}" \
        --input_dir="{folder}"\
        --output_dir="{output_folder}" \
        --buckets="256,512,768,1024,1280,1536,2048,2560,3072,3584,4096,4608,5120"''')


            i += n
            folder_i = folder_i + 1
    
    with open(exec_files +"/launch_all.sh","w") as f:
        f.write('''#!/bin/bash
#SBATCH -J launch_all
#SBATCH --partition=cpu
#SBATCH -c 1
#SBATCH --mem=8g 
                
''')
        for sh in  exec_file_paths:
            sh_name = sh.split("/")[-1]
            f.write(f'''until sbatch "{sh_name}"; do
        echo "Submission failed for {sh_name}. Retrying in 2 minutes..."
        sleep 120
    done
    
    ''')                    

distribute_files(path, "Launch_AF3", "/scratch/snorlax/saj027/saj027_projects/251125-251201_AF3_MD_tb/AF3_outputs", files_per_array)   











        



#260106 SJ
