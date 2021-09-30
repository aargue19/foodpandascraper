import requests
import json
import pandas as pd
import time
import datetime
import numpy as np

query_games_df = pd.read_csv('step3_earliest_tags.csv')

all_app_ids = query_games_df['app_id'].tolist()

list_of_app_ids_to_check = all_app_ids

# create blank dataframe and reorder columns

all_df = pd.DataFrame(columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
                                             'avg_pt_2weeks','initial_price','current_price','ccu',
                                             'lang_1','lang_2','lang_3','lang_4','lang_5',
                                             'lang_6','lang_7','lang_8','lang_9','lang_10',
                                             'genre_1','genre_2','genre_3','genre_4','genre_5'])

# logf = open("failed_games.txt", "w")

for i in range(len(list_of_app_ids_to_check)):

    print(f"checking #{i}: {int(list_of_app_ids_to_check[i])}")
    try:
        

        response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={int(list_of_app_ids_to_check[i])}').text

        response_info = json.loads(response)

        app_id = response_info['appid']

        pos_rev_num = response_info['positive']
        neg_rev_num = response_info['negative']
        usr_score = response_info['userscore']

        avg_pt_forever = response_info['average_forever']
        avg_pt_2weeks = response_info['average_2weeks']
        initial_price = response_info['initialprice']
        current_price = response_info['price']
        ccu = response_info['ccu']

        # split the string into two
        owners_string = response_info['owners']

        owners_vals = owners_string.split(" .. ")

        clean_owners_vals = []

        for string in owners_vals:
            new_string = string.replace(",", "")
            clean_owners_vals.append(new_string)

        if len(clean_owners_vals) > 0:
            owners_min = int(clean_owners_vals[0])
            owners_max = int(clean_owners_vals[1])
        if len(clean_owners_vals) == 0:
            owners_min = 999999
            owners_max = 999999 

        genre_list = response_info['genre'].split(", ")

        if len(genre_list) < 11:
            number_of_nas_to_append = 10 - len(genre_list)

            for j in range(number_of_nas_to_append):
                genre_list.append("NA")    
        
        else:
            # logf.write(f"{app_id}\n")
            print(f"more than 10 game #{app_id}")

        lang_list = response_info['languages'].split(", ")

        if len(lang_list) < 11:
            number_of_nas_to_append = 10 - len(lang_list)

            for j in range(number_of_nas_to_append):
                lang_list.append("NA")  

        row_to_add = {'app_id':[app_id],
                    'pos_rev_num':[pos_rev_num],
                    'neg_rev_num':[neg_rev_num],
                    'usr_score':[usr_score],
                    'avg_pt_forever':[avg_pt_forever],
                    'avg_pt_2weeks':[avg_pt_2weeks],
                    'initial_price':[initial_price],
                    'current_price':[current_price],
                    'ccu':[ccu],

                    'lang_1':[lang_list[0]],
                    'lang_2':[lang_list[1]],
                    'lang_3':[lang_list[2]],
                    'lang_4':[lang_list[3]],
                    'lang_5':[lang_list[4]],
                    'lang_6':[lang_list[5]],
                    'lang_7':[lang_list[6]],
                    'lang_8':[lang_list[7]],
                    'lang_9':[lang_list[8]],
                    'lang_10':[lang_list[9]],

                    'genre_1':[genre_list[0]],
                    'genre_2':[genre_list[1]],
                    'genre_3':[genre_list[2]],
                    'genre_4':[genre_list[3]],
                    'genre_5':[genre_list[4]],
                    'genre_6':[genre_list[5]],
                    'genre_7':[genre_list[6]],
                    'genre_8':[genre_list[7]],
                    'genre_9':[genre_list[8]],
                    'genre_10':[genre_list[9]]}

        df = pd.DataFrame(row_to_add, columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
                                                'avg_pt_2weeks','initial_price','current_price','ccu',
                                                'lang_1','lang_2','lang_3','lang_4','lang_5',
                                                'lang_6','lang_7','lang_8','lang_9','lang_10',
                                                'genre_1','genre_2','genre_3','genre_4','genre_5',
                                                'genre_6','genre_7','genre_8','genre_9','genre_10'])   

        all_df = pd.concat([all_df,df])

        #print(all_df)

        time.sleep(5)

    except Exception as e:
        print(f"Game #{i} failed -- ID# {list_of_app_ids_to_check[i]} failed")
        #print(e)
#########################################
# CHECK HERE TO SEE WHICH OF THE 476 GAMES FAILED

all_df.to_csv('step4_steam_api_data.csv', index=False)

###################################################################
# WHEN YOU HAVE THE DATA FOR ALL 476 GAMES THEN merge with previous file

all_df = pd.read_csv('step4_steam_api_data.csv', index_col=False)

step3_df = pd.read_csv('step3_earliest_tags.csv', index_col=False)

step_4_df = pd.merge(step3_df, all_df, on="app_id")


# REORDER COLUMNS

# for i in range(len(step_4_df.columns)):
#     print(i)
#     print(step_4_df.columns[i])

cols = step_4_df.columns.tolist()

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")

myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
myorder = myorder + list(np.arange(441,469,1)) + list(np.arange(14,440,1))
mylist = [cols[i] for i in myorder]
step_4_df = step_4_df[mylist]

# cols = step_4_df.columns.tolist()
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))


step_4_df.to_csv("step4_result_earliest_tags.csv", index=False)



###############################################################################
# UNUSED CODE

# #query the steamspy api for the 108 games in test2222.csv and get the current tags at present
# import requests
# import json
# import pandas as pd
# import time
# import datetime
# import numpy as np

# query_games_df = pd.read_csv('step3_result.csv')

# #list_of_app_ids_to_check = query_games_df['app_id'].tolist()
# all_app_ids = query_games_df['app_id'].tolist()
# #list_of_app_ids_to_check = all_app_ids[0:2]
# #list_of_app_ids_to_check = [706560]

# list_of_app_ids_to_check = all_app_ids

# # create blank dataframe and reorder columns
# all_df = pd.DataFrame(columns = query_games_df.columns)

# count = 0

# for current_app_id in list_of_app_ids_to_check:

#     count +=1

#     print(f"checking #{count}: {current_app_id}")

#     time.sleep(10)

#     response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={current_app_id}').text

#     response_info = json.loads(response)

#     tags_info = []

#     for tag in response_info['tags']:
#         tags_info.append([tag, response_info['tags'][tag]])

#     df = pd.DataFrame(tags_info, columns = ['tag_name','tag_count'])

#     #the tag data from the api is labeled using the names so match it with tag ids from tag_codes.csv

#     tag_codes_df = pd.read_csv('tag_names_codes_counts.csv')

#     df['app_name'] =  response_info['name']
#     df['app_id'] = current_app_id
#     df['new_tag_code'] = 999999

#     for i in range(len(df)):
#         try:
#             name_to_code = str(df.tag_name[i])
#             code_to_use = tag_codes_df.code.loc[tag_codes_df.tag == name_to_code].item()
#             # print(name_to_code)
#             # print(code_to_use)
#             df.new_tag_code.iloc[i] = code_to_use
#         except Exception as e:
#             print(e)
#     #print(df)

#     #CREATE A DATAFRAME WITH THE GAME DETAILS AND ALL 445 TAG COLUMNS AS BLANK

#     temp_present_tags_df = pd.DataFrame(columns=query_games_df.columns)

#     # append the data from test2222.csv to the first 15 columns and leave the rest blank

#     to_append = query_games_df.loc[query_games_df.app_id == current_app_id].values.tolist()

#     #print(f"to append is :")
#     #print(to_append)

#     a_series = pd.Series(to_append[0], index = temp_present_tags_df.columns)

#     temp_present_tags_df = temp_present_tags_df.append(a_series, ignore_index=True)

#     temp_present_tags_df.iloc[0,14:444] = ""

#     #put the current tags data in the same format as the original tags data
#     today = datetime.date.today()
#     d1 = today.strftime("%m/%d/%Y")
#     temp_present_tags_df.tag_date = pd.to_datetime(d1)
#     temp_present_tags_df.tag_before_release = 0

#     #iterate through the tag_#### columns and add the counts from the current game if they exist

#     tags_in_current_game = df['new_tag_code'].tolist()

#     #print(tags_in_current_game)

#     for i in range(len(tags_in_current_game)):

#         for j in range(len(temp_present_tags_df.columns)):
            
#             tag_to_check = f'tag_{tags_in_current_game[i]}'

#             if temp_present_tags_df.columns[j] == tag_to_check:
#                 #print(f"{tag_to_check} is the {j}th column")

#                 temp_present_tags_df.iloc[0,j] = df.tag_count.loc[df.new_tag_code == tags_in_current_game[i]]

#     all_df = all_df.append(temp_present_tags_df)

#     all_df.to_csv('step4_result.csv')


#combine the data for original tags and the present day tags


# temp_present_tags_df.index
# temp_present_tags_df.app_num
# temp_present_tags_df.app_name
# temp_present_tags_df.app_id
# temp_present_tags_df.release_date
# temp_present_tags_df.price
# temp_present_tags_df.price_decimal
# temp_present_tags_df.user_score_meta_score
# temp_present_tags_df.owners
# temp_present_tags_df.playtime_median
# temp_present_tags_df.developer
# temp_present_tags_df.developer2
# temp_present_tags_df.publisher
# temp_present_tags_df.publisher2