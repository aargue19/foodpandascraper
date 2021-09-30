import pandas as pd

#MERGE THE COLUMNS FROM THE TWO DATASETS WITH EARLIEST AND 6 MO TAGS
pd.set_option('display.max_rows', 100)

df1 = pd.read_csv("step4_result_earliest_tags.csv")
df2 = pd.read_csv("step3_tags_after_6_mo.csv")

# CHANGE THE NAMES OF THE COLUMNS IN THE 6 MONTH DF STARTING AFTER WITH 14


for colnum in range(13,len(df2.columns)):       #because 0 indexed to start at 14th column use 13
    
    orig_col_name = df2.columns[colnum]
    new_col_name = f"t6_{orig_col_name}"
    df2.rename(columns = {orig_col_name : new_col_name}, inplace = True)

print(len(df1.columns))
print(len(df2.columns))

mgd_df = pd.merge(df1, df2, on="app_id")

print(len(mgd_df.columns))

mgd_df.drop(mgd_df.filter(regex='_y').columns, axis=1, inplace=True)
# mgd_df = mgd_df.loc[:,~mgd_df.columns.str.endswith('_y')]

print(len(mgd_df.columns))

## SOME TAGS ARE MISSPELT OR DONT EXIST ANYMORE SO REMOVE THEM ### YOU DON"T NEED TO DO THIS ANYMORE B/C YOU DID IT IN STEP 2
#mgd_df = mgd_df.drop('tag_999999', 1)
#mgd_df = mgd_df.drop('t6_tag_999999', 1)
#mgd_df = mgd_df.drop('tag_5144', 1)
#mgd_df = mgd_df.drop('t6_tag_5144', 1)
#mgd_df = mgd_df.drop('tag_1694', 1)
#mgd_df = mgd_df.drop('t6_tag_1694', 1)
#mgd_df = mgd_df.drop('tag_134316', 1)
#mgd_df = mgd_df.drop('t6_tag_134316', 1)

# mgd_df.drop(mgd_df.filter(regex='999999').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='5144').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='1694').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='134316').columns, axis=1, inplace=True)

mgd_df.to_csv("step5_result.csv", index=False)