import os 
import shutil
from tqdm import tqdm

to_move = "/scratch/snorlax/saj027/saj027_projects/250627-250715_AF_mtb_random_array/Prep_AF3/jsons"
dest =  "/scratch/snorlax/saj027/saj027_projects/250627-250715_AF_mtb_random_array/Prep_AF3/jsons2"

current_outputs = "/scratch/snorlax/saj027/saj027_projects/250627-250715_AF_mtb_random_array/AF3_outputs"

#############################

move = []

os.makedirs(dest,exist_ok=True)


#Example name: 250627_random_array_run15_random__592_1 

to_move_list = os.listdir(to_move)
curr_out_list = os.listdir(current_outputs)
for file in tqdm(to_move_list):
    name = file[:file.find(".")]
    if name not in curr_out_list:
        move.append(file)
        start = to_move + "/" + file
        end = dest + "/" + file
        shutil.copy(start,end)
        
print(f"Copied {len(move)} out of {len(to_move_list)} files from {to_move} into {dest}")
