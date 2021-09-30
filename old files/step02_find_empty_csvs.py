import pandas as pd
import numpy as np
import os
import datetime
from os import listdir
from os import getcwd

#GET A LIST OF ALL THE CSV FILES WITH TAGS OVER TIME DATA DOWNLOADED FROM STEAMSPY AND CLEAN UP

rootdir = getcwd()

#filepath = rootdir + os.sep + "csvs" + os.sep
filepath = "C:" + os.sep + "Users" + os.sep + "gaoan" + os.sep + "Downloads" + os.sep
fail_folder_destination = "C:" + os.sep + "Users" + os.sep + "gaoan" + os.sep + "Desktop" + os.sep + "fail_folder" + os.sep

list_of_gamez = []
list_of_file_names = []

with os.scandir(filepath) as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        list_of_file_names.append(entry)
        list_of_gamez.append(entry.name.replace("_",":").replace(".csv",""))

for i in range(1,len(list_of_gamez)):

    try:
        #print(f"trying {list_of_gamez[i]}")

        data = pd.read_csv(list_of_file_names[i])

        column_name_list = data.columns.tolist()

        # print(column_name_list)
        # print(len(column_name_list))

        # if len(column_name_list) < 2 :
        #     print(f"{list_of_gamez[i]}: {len(column_name_list)}") 
    except Exception as e:
        print(f"{list_of_gamez[i]} is empty")

        current_filename = filepath + list_of_file_names[i].name
        current_destination_filename = fail_folder_destination + list_of_file_names[i].name
        print(f"moving file from here: {current_filename}, to here {current_destination_filename}")

        os.rename(current_filename, current_destination_filename)

        ##ADD CODE HERE TO DELETE THESE FILES FROM ORIGINAL DIRECTORY?