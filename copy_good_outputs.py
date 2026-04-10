import os
import shutil
import pandas as pd

pae = r"250619_AF3_binder-smeg_mmpL3_on_tb_designs.csv"

#Choose an input folder to find hits in! (folder shoud contain Alphafold_outputs[] folders)
cwd = r"/scratch/snorlax/saj027/saj027_projects/250619_mmpl3_AF-A0QP27"

#Choose a destination folder!
dest = r"/scratch/snorlax/saj027/saj027_projects/250619_mmpl3_AF-A0QP27/Hits"  

df = pd.read_csv(pae)

hits = []

for i in df.index:
  pae_int = df.iloc[i,1]  #Note that the min PAE of interaction must be in the second column!
  if pae_int < 3.05:    #Edit according to the threshhold of PAE you want the designs to have.
    design = df.iloc[i,0]
    hits.append(design)


directory = os.listdir(cwd)
for folder in directory:
    if "AF3_outputs" in folder:
        outputs_path = os.path.join(cwd,folder)
        outputs = os.listdir(outputs_path)
        for output in outputs:
            for hit in hits:
                if output == hit:
                    start = os.path.join(outputs_path,output)
                    end = os.path.join(dest,hit)
                    shutil.copytree(start,end)





#updated 250625 SJ
