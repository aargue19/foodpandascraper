import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# "raw_steamspy_year_2017.txt" is the raw source from the page "view-source:https://steamspy.com/year/2017"
# I DID A FIND/REPLACE ON <td data-order=""> to GET RID OF ANY BLANK NAMES OF GAMES OR DEVS (CHANGED TO XXXXXX)    #### YOU SHOULD CODE THIS SO YOU DONT HAVE TO DO IT MANUALLY
## YOU SHOULD ALSO INCLUDE SOME CODE TO REMOVE THE RECORDS WHERE YOU REPLACED BLANK ENTRIES  ("XXXXXX") BEFORE WRITING TO FILE

## ALSO SHOULD DO A REPLACE "N/A" AND "Free" WITH ZEROS IN PRICE_DECIMAL COLUMN BEFORE WRITING TO FILE


with open('steamspy_year_2017_games_raw.txt', encoding="utf8") as f:
    read_data = f.read()
    page_content = BeautifulSoup(read_data, "html.parser")


# PARSE THE HTML TO GET THE GAME NAMES
list_of_names=[]

# test_string = '<td data-order="Dungeon's Barrage">'
# print(re.findall("(?<=data-order=")(.*)(?=")))")

list_of_tds = page_content.find_all("td")

for td in list_of_tds:
    list_of_names.append(re.findall('(?<=data-order=")(.*)(?="><a)', str(td)))

good_names = []

for name in list_of_names:
    if len(name) > 0:
        good_names.append(name)

#print(len(good_names))

# PARSE THE HTML TO GET THE APP ID
list_of_ids = []

# test_string = '/app/434460'
# print(re.findall("(?<=app\/)(.*)", test_string))

list_of_links = page_content.find_all("a", href=True)

for lnk in list_of_links:
    list_of_ids.append(re.findall("(?<=app\/)(.*)", str(lnk['href'])))

# print(list_of_ids)

good_ids =[]

for i in list_of_ids:
    if len(i) > 0:
        good_ids.append(i)


# GET RELEASE DATES

list_of_rel_tds = page_content.find_all("td", {"class":"treleasedate"})

list_of_dates = []

for td in list_of_rel_tds:
    list_of_dates.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))

#GET PRICES 

list_of_price_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices = []

for td in list_of_price_tds:
    list_of_prices.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))



#GET PRICES WITH DECIMALS AND $

list_of_price_dec_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices_dec = []

for td in list_of_price_dec_tds:
    
    list_of_prices_dec.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# GET user_score_meta_score
#<td class="tuserscore" data-order="0">N/A (N/A/62%)</td>

list_of_score_tds = page_content.find_all("td", {"class":"tuserscore"})

list_of_scores = []

for td in list_of_score_tds:
    
    list_of_scores.append(re.findall('(?<=">)(.*)(?=<)', str(td)))



# GET OWNERS

# BE CAREFUL B/C FOR SOME REASON THE </FONT> TAG DISAPPEARS

# test_string = '<td data-order="100,000">100,000&nbsp;..&nbsp;200,000</font></td>'
# print(re.findall('(?=td data-order=\"\d)(.*)(?=<)',test_string))

#<td data-order="200,000">200,000&nbsp;..&nbsp;500,000</font></td>
list_of_owners = []

list_of_no_class_tds = page_content.find_all("td",{'class': None})

for td in list_of_no_class_tds[2::5]:
    list_of_owners.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

# print(list_of_owners[0:20])
# print(len(list_of_owners))



# print(list_of_owners_clean[0:10])
# print(len(list_of_owners_clean))

# GET PLAYTIME

list_of_ptimes = []
list_of_ptime_tds = page_content.find_all("td",{"class": "tplaytime"})

for td in list_of_ptime_tds:
    
    list_of_ptimes.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# print(list_of_ptimes[0:10])
# print(len(list_of_ptimes))


# GET DEVELOPER 

list_of_blank_tds = []
list_of_tds = page_content.find_all("td",{"class": None})

d1=[]
d2=[]

for td in list_of_tds[3::5]:
    d1.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

for td in list_of_tds[4::5]:
    d2.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))


# CHECK LENGTHS 
# print(len(good_names))
# print(len(good_ids))
# print(len(list_of_dates))
# print(len(list_of_prices))
# print(len(list_of_prices_dec))
# print(len(list_of_owners)) #######
# print(len(list_of_scores))
# print(len(list_of_ptimes))
# print(len(d1))
# print(len(d2))




# PREPARE ROWS FOR DF
all_rows=[]

for i in range(len(good_ids)):
    current_row = [i, good_names[i][0], good_ids[i][0], list_of_dates[i][0], list_of_prices[i][0], list_of_prices_dec[i][0],
                   list_of_scores[i][0], list_of_owners[i][0], list_of_ptimes[i][0], d1[i][0], d1[i][0], d2[i][0], d2[i][0]]
    all_rows.append(current_row)

# CREATE DF AND WRITE TO FILE
# colnames: app_num,app_name,app_id,release_date,price,price_decimal,user_score_meta_score,owners,playtime_median,developer,developer2,publisher,publisher2

df = pd.DataFrame(all_rows, columns = ['app_num', 'app_name', 'app_id','release_date','price','price_decimal',
                                       'user_score_meta_score','owners','playtime_median','developer','developer2', 'publisher', 'publisher2'])
df.to_csv("steamspy_2017_games_clean.csv", index=False)



################# UNUSED CODE

# THIS WAS FOR THE NON_MEMBERS PAGE WHERE OWNERS DATA IS GIVEN IN A RANGE
# for td in list_of_no_class_tds:
#     list_of_owners.append(re.findall('(?<=data-order="\d)(.*)(?=td)', str(td)))

# print(list_of_owners[0:20])

# list_of_owners_clean = []

# for x in list_of_owners:
#     if len(x) >0:
#         list_of_owners_clean.append(x)

# print(list_of_owners_clean[0:20])

# list_of_owners_clean2 = []

# for x in list_of_owners_clean:
#     # print(x)
#     if ".." in x[0] and "," in x[0]:
#         list_of_owners_clean2.append(x)

# print(list_of_owners_clean2[0:20])