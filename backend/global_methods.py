"""
Modernized global_methods.py

Ported and adapted from og_global_methods.py to provide all utility functions required by the backend.
"""

import os
import sys
import csv
import shutil
import errno
import numpy
import math
import random
import string
import datetime as dt
from os import listdir

# ---------------------------
# File/Folder Utilities
# ---------------------------

def create_folder_if_not_there(curr_path):
    """
    Checks if a folder in the curr_path exists. If it does not exist, creates
    the folder. If curr_path is a file, operates on its containing folder.
    """
    outfolder_name = curr_path.split("/")
    if len(outfolder_name) != 1:
        if "." in outfolder_name[-1]:
            outfolder_name = outfolder_name[:-1]
        outfolder_name = "/".join(outfolder_name)
        if not os.path.exists(outfolder_name):
            os.makedirs(outfolder_name)
            return True
    return False

def check_if_file_exists(curr_file):
    """
    Checks if a file exists.
    """
    try:
        with open(curr_file) as f_analysis_file:
            pass
        return True
    except:
        return False

def find_filenames(path_to_dir, suffix=".csv"):
    """
    Given a directory, find all files that end with the provided suffix and
    return their paths.
    """
    filenames = listdir(path_to_dir)
    return [
        os.path.join(path_to_dir, filename)
        for filename in filenames
        if filename.endswith(suffix)
    ]

def copyanything(src, dst):
    """
    Copy everything in the src folder to dst folder.
    """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise

# ---------------------------
# CSV Helpers
# ---------------------------

def write_list_of_list_to_csv(curr_list_of_list, outfile):
    """
    Writes a list of lists to a CSV file.
    """
    create_folder_if_not_there(outfile)
    with open(outfile, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(curr_list_of_list)

def write_list_to_csv_line(line_list, outfile):
    """
    Appends a single line (list) to a CSV file.
    """
    create_folder_if_not_there(outfile)
    with open(outfile, "a", newline='') as curr_file:
        csvfile_1 = csv.writer(curr_file)
        csvfile_1.writerow(line_list)

def read_file_to_list(curr_file, header=False, strip_trail=True):
    """
    Reads a CSV file to a list of lists. If header=True, returns (header, rows).
    """
    with open(curr_file) as f_analysis_file:
        data_reader = csv.reader(f_analysis_file, delimiter=",")
        analysis_list = []
        for count, row in enumerate(data_reader):
            if strip_trail:
                row = [i.strip() for i in row]
            analysis_list.append(row)
    if header:
        return analysis_list[0], analysis_list[1:]
    else:
        return analysis_list

def read_file_to_set(curr_file, col=0):
    """
    Reads a single column of a CSV file to a set.
    """
    analysis_set = set()
    with open(curr_file) as f_analysis_file:
        data_reader = csv.reader(f_analysis_file, delimiter=",")
        for count, row in enumerate(data_reader):
            if len(row) > col:
                analysis_set.add(row[col])
    return analysis_set

def get_row_len(curr_file):
    """
    Get the number of rows in a CSV file.
    """
    try:
        with open(curr_file) as f_analysis_file:
            data_reader = csv.reader(f_analysis_file, delimiter=",")
            return sum(1 for _ in data_reader)
    except:
        return False

# ---------------------------
# Math/Stats
# ---------------------------

def average(list_of_val):
    """
    Finds the average of the numbers in a list.
    """
    return sum(list_of_val) / float(len(list_of_val)) if list_of_val else 0

def std(list_of_val):
    """
    Finds the standard deviation of the numbers in a list.
    """
    return numpy.std(list_of_val) if list_of_val else 0


# ---------------------------
# Miscellaneous
# ---------------------------
def write_json(data, outfile):
    create_folder_if_not_there(outfile)
    with open(outfile, "w") as f:
        import json

        json.dump(data, f, indent=2)


def read_json(infile):
    with open(infile, "r") as f:
        import json

        return json.load(f)


# Add any additional helpers as needed
