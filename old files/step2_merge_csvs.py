import pandas as pd
import numpy as np
import os
import datetime
from os import listdir
from os import getcwd

# THE DATA FOR "tag_names_codes_counts.csv" COMES FROM "https://steamdb.info/tags/"
# I SAVED THE RAW SOURCE AS "steamdb_tag_codes_raw.txt"
# I used "step0_get_tag_codes.py" to make "tag_names_codes_counts.csv" which is a list of ALL CODES+totals FOR ALL TAGS

#MAKE A LIST OF ALL THE TAG CODES ON STEAM AND RENAME THEM TO "TAG_####"
tag_codes = pd.read_csv("tag_names_codes_counts.csv")

tag_code_list = tag_codes['tag_code'].tolist()

renamed_tag_code_list = []

for entry in tag_code_list:
    renamed_tag_code_list.append(f"tag_{entry}")

#GET A LIST OF ALL THE CSV FILES WITH TAGS OVER TIME DATA DOWNLOADED FROM STEAMSPY AND CLEAN UP

rootdir = getcwd()

filepath = rootdir + os.sep + "csvs" + os.sep

list_of_gamez = []
list_of_file_names = []

with os.scandir(filepath) as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        list_of_file_names.append(entry)
        list_of_gamez.append(entry.name.replace("_",":").replace(".csv",""))

#READ THE T.O.T. DATA FROM THE FIRST CSV FILE AND RENAME THE COLUMNS TO "TAG_####", REPLACE MISSING VALUES WITH "999999"

#print(list_of_file_names[0])

data = pd.read_csv(list_of_file_names[0])

column_name_list = data.columns.tolist()

new_column_name_list = []

for colname in column_name_list:
    new_column_name_list.append(f"tag_{colname}")

data.columns = new_column_name_list

data = data.replace(np.nan, 999999)

#data.to_csv("test_step_2.csv")

#CREATE A DATAFRAME WITH COLUMNS FOR ALL 425 THE TAGS AS COLUMNS AND FILL IN TAGS OVER TIME DATA FOR THE CURRENT GAME

df1 = pd.DataFrame(index=np.arange(len(data)), columns = renamed_tag_code_list)

for col_name in data.columns:

    df1[f'{col_name}'] = data[f'{col_name}'].values

df1["app_name"] = list_of_gamez[0]

#MATCH THE RECORDS BASED ON THE APP NAME TO OTHER GAME DETAILS FROM LIST OF ALL GAMES IN THAT YEAR AND APPEND DETAILS OF THE CURRENT GAME TO EACH LINE OF THE DATAFRAME

# df = pd.read_csv('steamspy_2018_games_clean.csv')                                 #THIS IS FOR THE 2018 GAMES
df = pd.read_csv('steamspy_2017_games_clean.csv')
#df = df.loc[~df.app_name.str.contains("<U+"),:]

#LOAD THE LIST OF EX EARLY ACCESS GAMES AND REMOVE THEM FROM THE DATAFRAME
ex_ea_games = pd.read_csv("ex_early_access_games.csv")
ex_ea_names_list = ex_ea_games['Game'].tolist()
df = df.loc[~df["app_name"].isin(ex_ea_names_list)]

line_for_merge = df.loc[df.app_name == list_of_gamez[0],:]

mgd_df = pd.merge(line_for_merge,df1, on="app_name")

#SINCE THIS IS THE FIRST FILE USE IT TO CREATE THE FINAL DF

final_df = mgd_df

#final_df.to_csv("test_2222.csv")

# #DO THE SAME FOR ALL OTHER FILES AND APPEND THEM TO THE FINAL DATAFRAME

for i in range(1,len(list_of_gamez)):

    print(f"trying {list_of_gamez[i]}")

    data = pd.read_csv(list_of_file_names[i])

    column_name_list = data.columns.tolist()

    new_column_name_list = []

    for colname in column_name_list:
        new_column_name_list.append(f"tag_{colname}")

    data.columns = new_column_name_list

    data = data.replace(np.nan, 999999)

    #CREATE A DATAFRAME WITH COLUMNS FOR ALL 425 THE TAGS AS COLUMNS AND FILL IN TAGS OVER TIME DATA FOR THE CURRENT GAME

    df1 = pd.DataFrame(index=np.arange(len(data)), columns = renamed_tag_code_list)

    for col_name in data.columns:

        df1[f'{col_name}'] = data[f'{col_name}'].values

    df1["app_name"] = list_of_gamez[i]

    #LOAD THE FILE WITH 2018 GAME DETAILS AND APPEND DETAILS OF THE CURRENT GAME TO EACH LINE OF THE DATAFRAME

    line_for_merge = df.loc[df.app_name == list_of_gamez[i],:]

    mgd_df = pd.merge(line_for_merge,df1, on="app_name")

    final_df = final_df.append(mgd_df, ignore_index=True)


# THERE ARE SOME WEIRD COLUMNS THAT YOU MAY NEED TO GET RID OF
#ORIGINALLY YOU DID THIS IN STEP 5 BUT YOU SHOULD DO IT HERE IF THEY COME UP

cols_to_drop = ['tag_999999','t6_tag_999999','tag_5144','t6_tag_5144','tag_1694','t6_tag_1694','tag_134316','t6_tag_134316']

for col_name in cols_to_drop:
    try:
        final_df = final_df.drop(f'{col_name}', 1)
    except Exception as e:
        print(e)


#WHEN FINISHED WRITE TO FILE

final_df.to_csv("step2_result.csv", index=False)