from glob import glob
import os

for file in glob("*json*/*.json*"):
    filename = file.split("/")[-1]
    os.rename(file, "jsons/"+filename)
