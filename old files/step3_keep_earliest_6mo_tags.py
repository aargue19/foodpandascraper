import pandas as pd
import numpy as np

#EXCLUDE GAMES WHERE THE TAGS DATA CAME AFTER THE RELEASE DATE

df = pd.read_csv("step2_result.csv")

# convert the 'Date' column to datetime format
df['release_date']= pd.to_datetime(df['release_date'])
df['tag_date']= pd.to_datetime(df['tag_date'])

#print(df.loc[:,['app_name','release_date','tag_date']].dtypes)

list_of_ids = df['app_id'].tolist()
list_of_ids = set(list_of_ids)
list_of_ids = list(list_of_ids)

#CREATE A COLUMN TO INDICATE IF A ROW IS THE EARLIEST TAGS FOR EACH GAME

df['tag_before_release'] = np.where(df['release_date']>df['tag_date'], "yes", "no")

#CREATE A COLUMN TO INDICATE IF A ROW IS THE FIRST TAGS AFTER THE ONE YEAR MARK FOR EACH GAME

# df['tag_before_release'] = np.where(df['release_date']>df['tag_date'], "yes", "no")

#MAKE A SUBSET OF JUST THE EARIEST RECORD OF TAGS

games_with_producer_tags = []

for current_id in list_of_ids:
    if "yes" in set(df['tag_before_release'].loc[df.app_id == current_id]):
        games_with_producer_tags.append(current_id)

tags_before_release_df = df[df["app_id"].isin(games_with_producer_tags)]

#use just the first game in the list to set up the dataframe
current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == games_with_producer_tags[0]].idxmin()

full_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

#iterate through and append the rest of the games
for current_id in games_with_producer_tags[1:len(games_with_producer_tags)]:

    try:
        current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == current_id].idxmin()

        temp_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

        full_df = pd.concat([full_df, temp_df], ignore_index=True, sort=False)
    
    except Exception as e:
        print(current_id)
        break


#EXCLUDE COLUMN # 444 WHICH iS THE GAME_BEFORE_RELEASE COL

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")
# print("\n")

cols = full_df.columns.tolist()
myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,438]
myorder = myorder + list(np.arange(13,438,1)) + [439,440]
mylist = [cols[i] for i in myorder]
full_df = full_df[mylist]

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))



full_df.to_csv("step3_earliest_tags.csv",index=False)

###########################################################################################################
# GAMES WITH NO TAGS AFTER 6 MONTHS:
# GOOD GIRL (1 MO)

df1 = df

df2 = df1.drop(['tag_before_release'], axis=1)

# df2 = df1.loc[:, df1.columns != 'tag_before_release']

df2 = df2.loc[df2.app_id.isin(df1.app_id)]                          ####THIS IS NOT WORKING AND THE TAG_BEFORE_RELEASE DOESNT ACTUALLY GET REMOVED
                                                                    ####BUT YOU CHANGE THE CODE IN STEP4 TO REMOVE IT SO IT GETS DROPPED LATER
# convert the 'Date' column to datetime format
df2['release_date']= pd.to_datetime(df2['release_date'])
df2['tag_date']= pd.to_datetime(df2['tag_date'])

#CREATE A COLUMN TO INDICATE HOW MANY MONTHS BETWEEN RELEASE AND EACH TAG DATE

df2['nb_months'] = ((df2.tag_date - df2.release_date)/np.timedelta64(1, 'M'))
df2['nb_months'] = df2['nb_months'].astype(int)

# df2.to_csv("test2222.csv")

full_df2 = pd.DataFrame(columns=df2.columns)

ids_to_check = list(set(df2['app_id'].tolist()))

# ## ONE GAME DOESNT HAVE TAGS AT 6 MONTHS SO REMOVE IT FROM THE DF                     #### HOW DID YOU CHECK FOR THIS???????
# #875230
# I REMOVED THE GAME FROM THE CSVS FOLDER INSTEAD
# CAN USE THIS IF THERE ARE MULTIPLE GAMES THOUGH
# FOR SOME REASON ITS NOT WORKING FOR THE EARLIEST TAGS DF ABOVE
# ids_to_check.remove(875230)

counter = 0

for current_id in ids_to_check:

    counter += 1

    try:
        current_idx = df2['tag_date'].loc[(df2['app_id'] == current_id) & (df2['nb_months'] == 6)].idxmin()

        temp_df = df2.loc[df2.index == current_idx,:]

        full_df2 = pd.concat([full_df2, temp_df], ignore_index=True, sort=False)
    
    except Exception as e:
        print(current_id)

# REORDER THE COLUMNS OF THE 6MO DF SO ALL TAG CODES ARE AT THE END
# THIS IS SO RENAMING THEM IS EASIER

cols = full_df2.columns.tolist()

# print(len(cols))
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append(cols[cnum])
# print(xxxx)

## THE COLUMN WITH # OF MONTHS BETWEEN RELEASE DATE AND TAG DATE IS DROPPED
myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,438]
myorder = myorder + list(np.arange(13,438,1)) + [439,440]
mylist = [cols[i] for i in myorder]
full_df2 = full_df2[mylist]

# cols = full_df.columns.tolist()
# print(len(cols))
# yyyy = []
# for cnum in range(len(cols)):
#     yyyy.append(cols[cnum])
# print(yyyy)

# print(full_df.columns[1:15])
# print(full_df2.columns[1:15])

# print(len(full_df.columns))
# print(len(full_df2.columns))


full_df2.to_csv("step3_tags_after_6_mo.csv", index=False)





###########################################################################################################

## MERGE THE TWO DATAFRAMES OF EARLIEST AND 6MO TAGS ?????????
## SHOULD DROP ONE CASE B/C THERE WERE NO TAGS AFTER 6 MO







###########################################################################################################
# UNUSED CODE





# for i in range(1, len(games_with_producer_tags)):

#     current_idx = tags_before_release_df.loc[tags_before_release_df['app_id'] == games_with_producer_tags[i], ['tag_date']].idxmin()

#     temp_df = tags_before_release_df.iloc[current_idx,:]

#     #full_df.append(temp_df, ignore_index=True)
#     full_df = pd.concat([full_df, temp_df], ignore_index=True, sort=False)

# full_df.to_csv("test2222.csv")

# print(tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == games_with_producer_tags[0]].idxmin())

# full_df = tags_before_release_df.loc[(tags_before_release_df['app_id'] == games_with_producer_tags[0]) & 
#                                             (tags_before_release_df['tag_date'] < tags_before_release_df['release_date']), :]

# for i in range(1,len(games_with_producer_tags)):

#     temp_df = tags_before_release_df.loc[(tags_before_release_df['app_id'] == games_with_producer_tags[i]) & 
#                                                 (tags_before_release_df['tag_date'] < tags_before_release_df['release_date']), :]

#     full_df = full_df.append(temp_df, ignore_index=True)

# tags_before_release_df.to_csv("test2222.csv")





# print(len(set(tags_before_release_df["app_id"])))
# print(set(tags_before_release_df["app_id"]))

#print(df.loc[df.app_id == list_of_ids[0], ['app_name','release_date','tag_date','tag_before_release']])

#print(df['tag_before_release'].loc[df.app_id == list_of_ids[0]])

#print("yes" in set(df['tag_before_release'].loc[df.app_id == list_of_ids[0]]))





# print(len(games_with_producer_tags))
# print(games_with_producer_tags)