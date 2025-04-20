"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: global_methods.py
Description: Contains functions used throughout my projects.
"""
import random
import string
import csv
import time
import datetime as dt
import pathlib
import os
import sys
import numpy
import math
import shutil, errno

from os import listdir

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

def write_list_of_list_to_csv(curr_list_of_list, outfile):
  create_folder_if_not_there(outfile)
  with open(outfile, "w") as f:
    writer = csv.writer(f)
    writer.writerows(curr_list_of_list)

def write_list_to_csv_line(line_list, outfile): 
  create_folder_if_not_there(outfile)
  curr_file = open(outfile, 'a',)
  csvfile_1 = csv.writer(curr_file)
  csvfile_1.writerow(line_list)
  curr_file.close()

def read_file_to_list(curr_file, header=False, strip_trail=True): 
  if not header: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        if strip_trail: 
          row = [i.strip() for i in row]
        analysis_list += [row]
    return analysis_list
  else: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        if strip_trail: 
          row = [i.strip() for i in row]
        analysis_list += [row]
    return analysis_list[0], analysis_list[1:]

def read_file_to_set(curr_file, col=0): 
  analysis_set = set()
  with open(curr_file) as f_analysis_file: 
    data_reader = csv.reader(f_analysis_file, delimiter=",")
    for count, row in enumerate(data_reader): 
      analysis_set.add(row[col])
  return analysis_set

def get_row_len(curr_file): 
  try: 
    analysis_set = set()
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        analysis_set.add(row[0])
    return len(analysis_set)
  except: 
    return False

def check_if_file_exists(curr_file): 
  try: 
    with open(curr_file) as f_analysis_file: pass
    return True
  except: 
    return False

def find_filenames(path_to_dir, suffix=".csv"):
  filenames = listdir(path_to_dir)
  return [ path_to_dir+"/"+filename 
           for filename in filenames if filename.endswith( suffix ) ]

def average(list_of_val): 
  return sum(list_of_val)/float(len(list_of_val))

def std(list_of_val): 
  std = numpy.std(list_of_val)
  return std

def copyanything(src, dst):
  try:
    shutil.copytree(src, dst)
  except OSError as exc: # python >2.5
    if exc.errno in (errno.ENOTDIR, errno.EINVAL):
      shutil.copy(src, dst)
    else: raise

if __name__ == '__main__':
  pass
