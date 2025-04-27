import os
import json

def create_folder_if_not_there(curr_path):
    outfolder_name = curr_path.split("/")
    if len(outfolder_name) != 1:
        if "." in outfolder_name[-1]:
            outfolder_name = outfolder_name[:-1]
        outfolder_name = "/".join(outfolder_name)
        if not os.path.exists(outfolder_name):
            os.makedirs(outfolder_name)
            return True
    return False

def write_json(data, outfile):
    create_folder_if_not_there(outfile)
    with open(outfile, "w") as f:
        json.dump(data, f, indent=2)

def read_json(infile):
    with open(infile, "r") as f:
        return json.load(f)

def check_if_file_exists(curr_file):
    return os.path.exists(curr_file)
