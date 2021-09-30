import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

df = pd.read_csv("step5_result_2018.csv",index_col=False)           #### USE THIS TO TEST CALCULATING MEASURES FOR NOW
# df = pd.read_csv("step5_result.csv",index_col=False)

# print(df.columns[1:40])

# print(len(df))
# genrez1 = df['genre_1'].tolist()
# genrez1 = list(set(genrez1))
# print(genrez1)

df = df.loc[(df.genre_1 != 'Animation & Modeling')
            & (df.genre_1 != 'Audio Production') 
            & (df.genre_1 != 'Video Production')
            & (df.genre_1 != 'Education')
            & (df.genre_1 != 'Free to Play') , :]

# print(len(df))
# genrez1 = df['genre_1'].tolist()
# genrez1 = list(set(genrez1))
# print(genrez1)
# print(df.columns[37:463])

#df = df.replace(np.nan,0)
df = df.replace(999999,np.nan)

# print(len(df))
df = df.loc[df.genre_1 == 'Action']
# print(len(df))

#COUNT THE NUMBER OF GENRES AS A SIMPLE SPANNING MEASURE
df['num_of_genres'] = df.iloc[:,31:36].apply(lambda x: x.notnull().sum(), axis='columns')   # THIS IS WEIRD YOU ONLY WANT COLUMNS 31-35 but you need to write 31:36
new_df = df.iloc[0:5,[31,32,33,34,35,890]]   #THIS NEEDS TO BE CHANGED BECAUSE YOU ADDED 5 EXTRA GENRE COLUMNS (TOTAL OF 10 NOW) IN STEP 4
# print(new_df)


##############################################################################################################################################################
#CALCULATE PROTOTYPE FOR ACTION GAMES USING TAGS 
# USE A DICHOTOMOUS MEASURE AT t0

#HOW MANY ACTION GAMES AT t0 APPLIED THE 'ACTION' TAG (#19)?
# print(df.tag_492.notnull().sum())

# Make a new dataset of only the t0 tags and 1 or 0 in each column

columns = [2,31] + list(np.arange(37,463))

t0_tags_df = df.iloc[:,columns]

# Change all null cells to 0 and all positive cells to 1
#t0_tags_df.iloc[:,2:len(t0_tags_df.columns)] = t0_tags_df.mask(t0_tags_df.iloc[:,2:len(t0_tags_df.columns)]>=1, 1)
# print(t0_tags_df.iloc[0:6,0:6])

t0_tags_df = t0_tags_df.loc[t0_tags_df.genre_1=="Action"]

how_many_action_games = len(t0_tags_df)

# print(f"{how_many_action_games} action games")
 
t0_tags_df = t0_tags_df.iloc[:,2:len(t0_tags_df.columns)-1]  

# print(t0_tags_df.iloc[1:10,0:6])



action_prototype_df = action_prototype_df / how_many_action_games
# print(list_of_counts.head())
# print(len(list_of_counts))

action_prototype_list = action_prototype_df.tolist()
# print(action_tags_prototype)

action_prototype_df = pd.DataFrame({"code" : action_prototype_df.index, "count" : action_prototype_df})

# print(action_prototype_df.head)
# print(action_prototype_df.columns)

# APPLY TAG NAMES AND CHECK OUt THE WEIGHTS OF THE PROTOTYPE

tag_codes_df = pd.read_csv("tag_codes.csv")

# print(tag_codes_df.head)

for i in range(len(tag_codes_df)):
    tag_codes_df.code[i] = f"tag_{tag_codes_df.code[i]}"

#print(tag_codes_df.head)

prototype_mgd_df = pd.merge(action_prototype_df,tag_codes_df, on='code')
prototype_mgd_df = prototype_mgd_df.sort_values(by=['count'], ascending=False)
#print(prototype_mgd_df.iloc[0:10])

# CHECK OUT THE NAMES OF THE TAGS FOR THE FIRST GAME

example_game = t0_tags_df.iloc[3,:]

example_game_df = pd.DataFrame({"code" : example_game.index, "tag_count" : example_game})

mgd_df = pd.merge(example_game_df,tag_codes_df, on='code')

# print(example_game_df.loc[example_game_df.tag_count == 1])

mgd_df = mgd_df.sort_values(by=['tag_count'], ascending=False)

print(mgd_df.iloc[0:20,:])


#############################################################################################
# CALCULATE THE COSINE SIMILARITY OF A COUPLE GAMES

# print(df.head)S

first_game = t0_tags_df.iloc[3,:].tolist()
second_game = t0_tags_df.iloc[99,:].tolist()

# print(len(first_game))
# print(first_game)

# print(len(second_game))
# print(second_game)

# print(len(action_tags_prototype))
# print(action_tags_prototype)

# first_game_df = t0_tags_df.iloc[0,:]
# first_game_df = first_game_df[first_game_df != 0]

#print(first_game_df)

result1 = 1 - spatial.distance.cosine(first_game, action_prototype_list)

print(f"similarity of first game and prototype: {result1}")

# print(len(second_game))
# print(len(action_tags_prototype))

# second_game_df = t0_tags_df.iloc[1,:]
# second_game_df = second_game_df[second_game_df != 0]

# print(second_game_df)

# result2 = 1 - spatial.distance.cosine(second_game, action_tags_prototype)

# print(f"similarity of second game and prototype: {result2}")


################################################################################################################################
################################################################################################################################


# CALCULATE ENTROPY OF DISTRIBUTIONS OF TAGS AT t6

# https://www.youtube.com/watch?v=IPkRVpXtbdY

# Entropy is a measure of disorder in a dataset
# Take the count for each tag divide it by the total # of tags 
# This will give you a vector of probabilities
# Use this vector to calculate entropy

# # CALCULATES ENTROPY BY KEEPING TAGS AS A SERIES
# ent_df = df.iloc[:,464:889]

# ent_df = ent_df.replace(np.nan,0)


# data = ent_df.iloc[0,:]                                #

# sum_total = data.sum()

# data = data / sum_total

# data_no_zeros = data[data!=0]

# # plot = data_no_zeros.plot(kind="bar")
# # fig = plot.get_figure()
# # fig.savefig("barplot222222.png")

# # print(data.tolist())
# # print(scipy.stats.entropy(data, base=2))

# # TRY ANOTHER DISTRIBUTION OF t6 tags
# data = ent_df.iloc[2,:]                                #

# sum_total = data.sum()

# data = data / sum_total

# data_no_zeros = data[data!=0]

# plot = data_no_zeros.plot(kind="bar")
# fig = plot.get_figure()
# fig.savefig("barplot222222.png")

# print(data.tolist())
# print(scipy.stats.entropy(data, base=2))

#######################################################################################
# CALCULATES ENTROPY BY CONVERTING TAGS TO A LIST

# game_1_t6_tags = df.iloc[0,:].tolist()

# count = 0

# for i in range(len(game_1_t6_tags)):
#     count += game_1_t6_tags[i]

# for j in range(len(game_1_t6_tags)):
#     game_1_t6_tags[j] = game_1_t6_tags[j]/count

# print(game_1_t6_tags)
# print(count)

# entropy = scipy.stats.entropy(game_1_t6_tags)
# print(f"game 1 entropy: {entropy}")

# game_2_t6_tags = df.iloc[1,:].tolist()

# count = 0

# for i in range(len(game_2_t6_tags)):
#     count += game_2_t6_tags[i]

# for j in range(len(game_2_t6_tags)):
#     game_2_t6_tags[j] = game_2_t6_tags[j]/count

# print(game_2_t6_tags)
# print(count)

# entropy = scipy.stats.entropy(game_2_t6_tags)
# print(f"game 2 entropy: {entropy}")

############################################################################################################################################################
############################################################################################################################################################
# CALCULATE A MEASURE OF CONFUSION 
# FIND OUT HOW MANY NEW TAGS WERE ADDED TO A GAME ON TOP OF PRODUCERS' TAGS AT T=0

columns = [2] + list(np.arange(37,463))

t0_tags_df = df.iloc[:,columns]

t6_tags_df = df.iloc[:,464:889]























# print(df.iloc[:,37])

# print(df.iloc[:,37].mean())

# action_prototype = df.iloc[:,37:463]

# mean_df = action_prototype['tags_mean'] = action_prototype.mean(axis=1)

# print(mean_df)



# slice_and_dice = df.iloc[:,37:463]               #THIS NEEDS TO BE CHANGED BECAUSE YOU ADDED 5 EXTRA GENRE COLUMNS (TOTAL OF 10 NOW) IN STEP 4

# # print(slice_and_dice.columns)

# slice_and_dice[slice_and_dice != 0] = 1

# # print(slice_and_dice.iloc[0,:].tolist())

# # print(len(slice_and_dice))

# what_does_it_mean = slice_and_dice.mean(axis=0)

# # print(what_does_it_mean[37:463].tolist())





# CALCULATE COSINE SIMILARITY BETWEEN A GAME AND THE VECTOR OF AVERAGES FOR EACH TAG COLUMN FOR ACTION GAMES
# from numpy import dot
# from numpy.linalg import norm

# game_1_tag_vec = df.iloc[0,37:463].tolist()     #THIS NEEDS TO BE CHANGED BECAUSE YOU ADDED 5 EXTRA GENRE COLUMNS IN STEP 4  (TOTAL OF 10 NOW)

# game_2_tag_vec = df.iloc[1,37:463].tolist()     #THIS NEEDS TO BE CHANGED BECAUSE YOU ADDED 5 EXTRA GENRE COLUMNS IN STEP 4  (TOTAL OF 10 NOW)

# cos_sim_game_1 = dot(game_1_tag_vec, what_does_it_mean)/(norm(game_1_tag_vec)*norm(what_does_it_mean))
# cos_sim_game_2 = dot(game_2_tag_vec, what_does_it_mean)/(norm(game_2_tag_vec)*norm(what_does_it_mean))

# print(cos_sim_game_1)
# print(cos_sim_game_2)





# CALCULATE ENTROPY

# game_1_t6_tag_vec = df.iloc[0,464:890].tolist()
# game_1_t6_tagz = []
# for i in range(len(game_1_t6_tag_vec)):
#     if game_1_t6_tag_vec[i] > 0:
#         #print(f"{i}: {game_1_t6_tag_vec[i]}")
#         game_1_t6_tagz.append(game_1_t6_tag_vec[i])

# fig = plt.hist(np.array(game_1_t6_tagz))

# plt.savefig("abc.png")

# data = game_1_t6_tagz
# pd_series = pd.Series(data)
# counts = pd_series.value_counts()
# entropy = scipy.stats.entropy(counts)
# print(f"game 1 entropy: {entropy}")

# game_2_t6_tag_vec = df.iloc[1,464:890].tolist()
# game_2_t6_tagz = []
# for i in range(len(game_2_t6_tag_vec)):
#     if game_2_t6_tag_vec[i] > 0:
#         print(f"{i}: {game_2_t6_tag_vec[i]}")
#         game_2_t6_tagz.append(game_2_t6_tag_vec[i])

# data = game_2_t6_tagz
# pd_series = pd.Series(data)
# counts = pd_series.value_counts()
# entropy = scipy.stats.entropy(counts)
# print(f"game 2 entropy: {entropy}")


# v1 = [1,1,1,1,1]
# v2 = [10,10,10,10,10]
# v3 = [1,1,1,1]
# v4 = [1,1]
# v5 = [0.5,0.5]


# data = v5
# pd_series = pd.Series(data)
# counts = pd_series.value_counts()
# entropy = scipy.stats.entropy(counts)
# print(f"entropy for: {data}: {entropy}")

# data = v4
# pd_series = pd.Series(data)
# counts = pd_series.value_counts()
# entropy = scipy.stats.entropy(counts)
# print(f"entropy for: {data}: {entropy}")
