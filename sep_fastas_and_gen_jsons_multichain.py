from glob import glob
import argparse
import json
import os
import numpy as np
import pyrosetta
from pyrosetta import Pose

pyrosetta.init()

argparser = argparse.ArgumentParser()  # Added parser initialization

argparser.add_argument("--proteinmpnn_directory", type=str, help="Path to a folder with .fa files")

argparser.add_argument("--output_directory", type=str, help="Path where to save .jsonl dictionary of parsed pdbs")

argparser.add_argument("--num_seqs", type=str, help="Number of sequences")

args = argparser.parse_args()

nseqs = int(args.num_seqs)
cnt = 0

for fa in glob(args.proteinmpnn_directory + '/*fa'): # HAS TO BE THE FA FILES
    fin = open(fa, 'r')
    lline = fin.readline()
    lline = fin.readline()

    for i in range(nseqs):
        #out_ind = np.floor(cnt / 1000)
        # print(cnt/1000)
        # print(out_ind)

        if not os.path.exists(args.output_directory + '/fastas/'):
            os.makedirs(args.output_directory + '/fastas/')

        lline = fin.readline()
        lline = fin.readline()
        pname = fa.split('/')[-1][:-3]
        # LS
        # takes bottom:
        # /content/drive/MyDrive/GoogleColab_Tests/tests_for_ColabFold_gentasks.py/inputs/talen1_3.32_34.30_25_71_aligned_13.fa
        # converts to
        # talen1_3.32_34.30_25_71_aligned_13

        fout = open(args.output_directory + '/fastas/' + pname + '_%d.fasta' % i, 'w')
        fout.write('>' + pname + '_%d\n' % i)

        out_str=''

        #replace / delimiters in fasta with :, colabfold syntax
        for j in lline.split('/'):
            out_str=out_str+j+':'

        fout.write(out_str[:-1])
        fout.close()

        cnt += 1

        print(f"Fasta Wrote: {args.output_directory + '/fastas/' + pname + '_%d.fasta' % i} successfully")


#-----------------------------Code added by SJ start

msa_AF = r"has_AF-A0QP27_msa_data.json"     #SJ --- the path to the file outputted by Alphafold that has your desired msa
chain = "B"    #replace with the chain that contains the MSA you want to copy and paste!!!
unpairedMsa = ""

print("I got here")


with open(msa_AF,"r") as file:
    llines = file.readlines()
    for line in llines:
        if '"id": "' + chain + '"' in line:
            print("found id")
            index_to_msa = llines.index(line) + 3
            if "unpairedMsa" in llines[index_to_msa]:
                print("found unpairedMsa")
                start = llines[index_to_msa].find(": ") + 2
                unpairedMsa = llines[index_to_msa][start:].replace('"','').encode('utf-8').decode('unicode_escape')


#--------------------------------Code added by SJ en

for fasta in glob(args.output_directory + '/fastas/*fasta'):
    fasta_name = fasta.split('/')[-1][:-6]  # gets name and removes .fasta
    #break_name = fasta_name.split('_')   # creates a list by splitting each element by "_" (ex: talen1_3.32_34.30_38_210_aligned_17_Bdna_centered_0)
    #dna_name = '_'.join(break_name[7:9]) # creates a new string "dna_name" by adding underscores from indices 7 to 9 of the fasta name (ex: Bdna_centered_0)
    with open(fasta, "r") as file:
        llines = file.readlines()
        fasta = llines[1].strip() # Removes extra spaces from the second line, and is equal to the fasta variable
    #dna_directory = glob(args.dna_directory + '/*.pdb') # Searches the DNA directory for pdbs
    #for dna in dna_directory:
        #dna_filename = os.path.basename(dna).replace(".pdb", "") # Removes the .pdb file extension from the DNA filename
        #if dna_name == dna_filename:
            #ppose = pyrosetta.pose_from_pdb(dna) # Creates a pose (molecular representation) of the DNA
            #dna_sequence = ppose.sequence().upper()
    if not os.path.exists(args.output_directory + '/jsons'):
        os.makedirs(args.output_directory + '/jsons')

    data_to_write = {
        "name": fasta_name,
        "modelSeeds": [13],
        "sequences": [ 
            {
                "protein": {
                    "id": ["A"],
                    "sequence": fasta.split(":")[0], # EYSA Change
                    "unpairedMsa": ">query\n" + fasta.split(":")[0],
                    "pairedMsa": "",
                    #"unpaired_msa_path": " "      250507 commented out by SJ
                }
            },
             {
               "protein": {
                   "id": ["B"],
                 "sequence": "MFAWWGRTVYQFRYIVIGVMVALCLGGGVYGISLGNHVTQSGFYDEGSQSVAASLIGDEVYGRDRTSHVVAILTPPDDKKVTDKAWQKKVTEELDQVVKDHEDQIVGWVGWLKAPDTTDPTVSAMKTQDLRHTFISIPLQGDDDDEILKNYQVVEPELQQVNGGDIRLAGLNPLASELTGTIGEDQKRAEVAAIPLVAVVLFFVFGTVIAAALPAIIGGLAIAGALGIMRLVAEFTPVHFFAQPVVTLIGLGIAIDYGLFIVSRFREEIAEGYDTEAAVRRTVMTSGRTVVFSAVIIVASSVPLLLFPQGFLKSITYAIIASVMLAAILSITVLAAALAILGPRVDALGVTTLLKIPFLANWQFSRRIIDWFAEKTQKTKTREEVERGFWGRLVNVVMKRPIAFAAPILVVMVLLIIPLGQLSLGGISEKYLPPDNAVRQSQEQFDKLFPGFRTEPLTLVMKREDGEPITDAQIADMRAKALTVSGFTDPDNDPEKMWKERPANDSGSKDPSVRVIQNGLENRNDAAKKIDELRALQPPHGIEVFVGGTPALEQDSIHSLFDKLPLMALILIVTTTVLMFLAFGSVVLPIKAALMSALTLGSTMGILTWMFVDGHGSGLMNYTPQPLMAPMIGLIIAVIWGLSTDYEVFLVSRMVEARERGMSTAEAIRIGTATTGRLITGAALILAVVAGAFVFSDLVMMKYLAFGLLIALLLDATIIRMFLVPAVMKLLGDDCWWAPRWMKRVQEKLGL",
                 "unpairedMsa": unpairedMsa[:-3] + "\n",  #SJ 250507 gets rid of super annoying extra \n,
                 "pairedMsa": "",
                #"unpaired_msa_path": '/scratch/snorlax/enarambulo/AF3/NGF_MSAs/NGF_MSA_rd1rd2'
                }
             }
        ],
        # "bondedAtomPairs": [
        #   [["A", 1, "CA"], ["G", 1, "CHA"]],
        #   [["I", 1, "O6"], ["I", 2, "C1"]]
        # ],
        # "userCCD": ...,
        "dialect": "alphafold3",
        "version": 3
    }

    with open(args.output_directory + '/jsons/' + fasta_name + '.json', 'w') as fout_json:
        json.dump(data_to_write, fout_json, indent=2) 
        print(f"JSON Wrote: {args.output_directory + '/jsons/' + fasta_name + '.json'} successfully")

