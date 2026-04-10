import os
import pandas as pd
import json

df = pd.DataFrame()

filename = []

aa = [] #pae for chain a with chain a
ax = [] #pae for chain a with chain x
xa = [] #pae for chain x with chain a
xx = [] #pae for chain x with chain x

min_pae = []  #the minimum a-x interaction pae (either ax or xa, whichever is lower). Binder is chain x, mmpL3 is chain a.

#name = "AF3_outputs"       #Can use this if you have folders with naming styled AF3_outputs0, AF3_outputs1, etc.
# folder_list = []
# for i in range(0,9):
#     folder_list.append(name+str(i))

#############################################################################  Edit these variables  #
save_as = "250804_AF3_mtb_random_array_PAE_all.csv"

folder_list = ["AF3_outputs"]

folderpath = r"/scratch/snorlax/saj027/saj027_projects/250627-250715_AF_mtb_random_array/"
#######################################################################################################

for parent_folder in folder_list:
    parent_folder_path = os.path.join(folderpath, parent_folder)
    for folder in os.listdir(parent_folder_path):
        path = os.path.join(parent_folder_path, folder)
        outputs = os.listdir(path)
        for output in outputs:
            if "summary_confidences.json" in output:
                output_path = os.path.join(path,output)
                f = open(output_path)
                data = json.load(f)
                pair_pae = data["chain_pair_pae_min"]
                filename.append(output[:output.find("_summary")])
                aa.append(pair_pae[0][0])
                ax.append(pair_pae[0][1])
                xa.append(pair_pae[1][0])
                xx.append(pair_pae[1][1])
                if pair_pae[0][1] <= pair_pae[1][0]:
                    min_pae.append(pair_pae[0][1])
                elif pair_pae[1][0] < pair_pae[0][1]:
                    min_pae.append(pair_pae[1][0])



df["Design"] = filename
df["Min_PAE_Interaction_chain_A-X"] = min_pae
df["Min_PAE_chain_A-chain_A"] = aa
df["Min_PAE_chain_A-chain_X"] = ax
df["Min_PAE_chain_X-chain_A"] = xa
df["Min_PAE_chain_X-chain_X"] = xx




df.to_csv(save_as,index=False)


