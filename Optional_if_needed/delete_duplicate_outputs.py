#delete duplicate output folders from repeated AlphaFold 3 jobs

import os
import shutil

path = "AF3_outputs"

for folder in os.listdir(path):
    if len(folder) > 40:
        # print(f"{folder} len: {len(folder)}")
        shutil.rmtree(path + "/" + folder)
