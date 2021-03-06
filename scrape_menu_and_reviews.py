###################################################################################################
# STEP 1: GET ALL THE LINKS TO RESTAURANTS LISTED AS TAIWANESE
###################################################################################################
import time
import re
import pandas as pd
from selenium import webdriver

# RUN THIS THE FIRST TIME TO GET THE RIGHT DRIVERS
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument("user-data-dir=C://Users/gaoan/AppData/Local/Google/Chrome/User Data")

driver = webdriver.Chrome(options=chrome_options)

# JUST SCRAPE ONE MENU FOR NOW:
driver.get('https://www.foodpanda.com.tw/en/restaurant/z7jm/da-hao-niu-pai-gao-xiong-re-he-dian') #burgers cuisine = 177
time.sleep(8)  # Timeout

# GET RESTAURANT NAME
rest_title = driver.find_elements_by_tag_name('h1')[0].text

# GET RATING
rest_rating = driver.find_elements_by_class_name("rating-label")[0].text

# GET DEAL NAME
deal_name = driver.find_elements_by_class_name("deal-name")[0].text

# GET DEAL DESCRIPTION
deal_desc = driver.find_elements_by_class_name("deal-desc")[0].text

# GET CUISINES

details_cuis = driver.find_element_by_class_name("vendor-info-main-details-cuisines")
details_char_items = details_cuis.find_elements_by_class_name("characteristic-list-item")

# DOLLAR SIGNS
all_dollars_list = []
details_dollar_items = details_char_items[0].find_elements_by_tag_name('span')   # $$$

for dolla in details_dollar_items:
    all_dollars_list.append(dolla.text)

# CUISINE 1
details_char_items1 = details_char_items[1].find_element_by_tag_name('span')   # cuisines

cuisine_1 = []
cuisine_1.append(details_char_items1.text)

# CUISINE 2
cuisine_2 = []
if len(details_char_items)>2:

    details_char_items2 = details_char_items[2].find_element_by_tag_name('span')   # cuisines
    cuisine_2.append(details_char_items2.text)

else:    
    cuisine_2.append("NA")

# GET DISH CATEGORIES 
dish_cat_sections = driver.find_elements_by_class_name("dish-category-section")

dish_cats_list = []
full_menu_items_list = []
full_prices_list = []
full_discounts_list = []
full_pic_list = []
full_info_list = []
full_ratings_list = []

for elem in dish_cat_sections:
    button_count = elem.find_elements_by_tag_name('button')                                                 # (keep all with more than one button)
    if len(button_count) > 1:
        dish_cats_list.append(elem.find_elements_by_class_name("dish-category-title")[0].text)


        # get all menu items
        dish_info = elem.find_elements_by_class_name("dish-info")
        for dish in dish_info:
            temp_menu_items = dish.find_elements_by_tag_name('span')
        
            for item in temp_menu_items:
                full_menu_items_list.append(item.text)

        # get all original prices
        price_info = elem.find_elements_by_class_name("price-tags-container")
        for price in price_info:
            temp_prices = price.find_elements_by_class_name('p-price')

            for item in temp_prices:
                full_prices_list.append(item.text)

        # get all discount prices
        for price in price_info:
            temp_discs = price.find_elements_by_class_name('price-discount')

            for item in temp_discs:
                full_discounts_list.append(item.text)

        # haz picture?
        dish_info = elem.find_elements_by_class_name("dish-info-container")
        for dish in dish_info:
            temp_pic = dish.find_elements_by_tag_name('picture')

            if len(temp_pic) > 0:
                full_pic_list.append("1")
            else:
                full_pic_list.append("0")

# GET REVIEWS

time.sleep(5)  # Timeout

driver.find_element(By.XPATH, '//*[@class="vendor-info-main-details"]').click()

time.sleep(5)  # Timeout
driver.find_element(By.XPATH, '//*[@data-title="Reviews"]').click()

# driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
# driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
# driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)

time.sleep(5)  # Timeout

review_info = driver.find_element(By.XPATH, '//*[@id="reviews-panel"]')

rev_content = review_info.find_elements_by_tag_name('p')

for info in rev_content:
    full_info_list.append(info.text)


review_ratings = review_info.find_elements_by_class_name("rating-label")
for rat in review_ratings:
    full_ratings_list.append(rat.text)


time.sleep(5)  # Timeout

print(rest_title)

print(rest_rating)

print(deal_name)

print(deal_desc)

print(cuisine_1)

print(cuisine_2)

print(all_dollars_list)


# print(dish_cats_list)
print(full_menu_items_list)
print(len(full_menu_items_list))
print(full_prices_list)
print(len(full_prices_list))
print(full_discounts_list)
print(len(full_discounts_list))
print(full_pic_list)
print(len(full_pic_list))
print(full_info_list)
print(len(full_info_list))
print(full_ratings_list)
print(len(full_ratings_list))

# temp_list = []

# for i in range(len(full_menu_items_list)):
#     temp_list.append(full_menu_items_list[i])
#     temp_list.append(full_prices_list[i])
#     temp_list.append(full_discounts_list[i])
#     temp_list.append(full_info_list[i])
#     temp_list.append(full_prices_list[i])


# df = pd.DataFrame({'name': rest_title,
#                     'overall_rating': rest_rating,
#                     'deal_name': deal_name,
#                     'deal_description': deal_desc,
#                     'cuisine_1': cuisine_1,
#                     'cuisine_2': cuisine_2,
#                     'dollars': ''.join(all_dollars_list),
#                     'full_menu_items_list': ''.join(all_dollars_list),
#                     'full_menu_items_list': elem_list,
#                     'links': elem_list,
#                     'links': elem_list,
#                     'links': elem_list,

#                                         })

# df.to_csv("burger_links.csv", index=False)


# string_to_check = elements[0].text
# number_found = re.findall(r'^[0-9]*', str(string_to_check))
# number_found = int(number_found[0])

# print(number_found)

# how_many = []

# while len(how_many)<number_found:                                                          #the number quoted at the top of the page isn't right sometimes
#     # Scroll down to bottom
# #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
        
#         # driver.execute_script("window.scrollTo(0, document.body.scrollHeight, {behavior: 'smooth'});")
        
#         # time.sleep(2) 

#         driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
#         driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
#         driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
#         # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
#         # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)

#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)

#         how_many = driver.find_elements_by_class_name("vendor-picture")

#         print(len(how_many))

#         # Calculate new scroll height and compare with last scroll height
#         # new_height = driver.execute_script("return document.body.scrollHeight")
#         # if new_height == last_height:
#         #         break
#         # last_height = new_height


# # ONCE SCROLLED ALL THE WAY TO THE BOTTOM GET ALL LINKS ON PAGE

# href_elems = driver.find_elements_by_xpath("//a[@href]")

# elem_list = []

# for elem in href_elems:
#         target_string = elem.get_attribute("href")

#         if "/restaurant/" in str(target_string):
#                 elem_list.append(re.findall(r'(?<=restaurant\/)(.*)', str(target_string))[0])


# # WRITE TO FILE (REMEMBER TO CHANGE FILENAME BELOW)

# print(len(elem_list))

# df = pd.DataFrame({'links': elem_list})

# df.to_csv("burger_links.csv", index=False)

'''
listings = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/main/div[3]/section")

href_elems = listings[0].find_elements_by_xpath("//a[@href]")

elem_list = []

for elem in href_elems:
        target_string = elem.get_attribute("href")

        if "/restaurant/" in str(target_string):
                elem_list.append(re.findall(r'(?<=restaurant\/)(.*)', str(target_string))[0])

print(elem_list)

df = pd.DataFrame({'links': elem_list})

df.to_csv("tW_links.csv", index=False)



time.sleep(5)  # Timeout

# Start the stopwatch
# start = time.time()






# # CLOSE BROWSER
driver.quit()

'''
# start_num = 6230

# HERE YOU CAN CHOOSE WHAT RANGE OF GAMES YOU WANT TO SCRAPE DATA FOR
# gamez = gamez_df.loc[start_num:start_num+50, "app_id"].tolist()

# OPEN A LOGFILE TO TRACK ANY GAMES THAT DIDN'T GET SCRAPED
# logf = open("step1_failed_scrapes.txt", "a")

# counter = start_num

# fail_count =0

##### CREATE BLANK DATAFRAME SINCE IN THE LOOP YOU ARE APPENDING THE DATA WITHOUT HEADERS

# df = pd.DataFrame(columns = ['app_id_scrap',                                                #ONLY NEED TO DO THIS THE VERY FIRST TIME
#                                     'old_usrscore_scrap', 
#                                     'metascore_scrap',
#                                     'genres_scrap',
#                                     'followers_scrap',
#                                     'playtime_scrap',
#                                     'youtube_scrap',
#                                     'ccu_scrap',
#                                     'developer_scrap',
#                                     'publisher_scrap',

#                                     'lang_1_scrap',
#                                     'lang_2_scrap',
#                                     'lang_3_scrap',
#                                     'lang_4_scrap',
#                                     'lang_5_scrap',
#                                     'lang_6_scrap',
#                                     'lang_7_scrap',
#                                     'lang_8_scrap',
#                                     'lang_9_scrap',
#                                     'lang_10_scrap',
#                                     'lang_11_scrap',
#                                     'lang_12_scrap',
#                                     'lang_13_scrap',
#                                     'lang_14_scrap',
#                                     'lang_15_scrap',
#                                     'lang_16_scrap',
#                                     'lang_17_scrap',
#                                     'lang_18_scrap',
#                                     'lang_19_scrap',
#                                     'lang_20_scrap',

#                                     'tag_1_scrap', 'tag_1_count',
#                                     'tag_2_scrap', 'tag_2_count',
#                                     'tag_3_scrap', 'tag_3_count',
#                                     'tag_4_scrap', 'tag_4_count',
#                                     'tag_5_scrap', 'tag_5_count',
#                                     'tag_6_scrap', 'tag_6_count',
#                                     'tag_7_scrap', 'tag_7_count',
#                                     'tag_8_scrap', 'tag_8_count',
#                                     'tag_9_scrap', 'tag_9_count',
#                                     'tag_10_scrap', 'tag_10_count',
#                                     'tag_11_scrap', 'tag_11_count',
#                                     'tag_12_scrap', 'tag_12_count',
#                                     'tag_13_scrap', 'tag_13_count',
#                                     'tag_14_scrap', 'tag_14_count',
#                                     'tag_15_scrap', 'tag_15_count',
#                                     'tag_16_scrap', 'tag_16_count',
#                                     'tag_17_scrap', 'tag_17_count',
#                                     'tag_18_scrap', 'tag_18_count',
#                                     'tag_19_scrap', 'tag_19_count',
#                                     'tag_20_scrap', 'tag_20_count',
#                                     'description',
#                                     'full_text'])

# df.to_csv("step1_steamspy_scraped_data.csv", index=False)

# ITERATE THROUGH THE LIST AND GET DOWNLOAD THE CSV TO THE DOWNLOADS FOLDER
# for current_app_id in gamez:

#     print(f"trying game #{counter}")
#     counter+=1
#     try:
#         first_game_url = f"https://steamspy.com/app/{int(current_app_id)}#tab-tagstime"
#         driver.get(first_game_url)
#         time.sleep(10)

#         driver.find_element(By.XPATH, '//*[@id="amch-tagstime"]/div/div[2]/ul/li/a').click()
#         time.sleep(1)

#         driver.find_element(By.XPATH, '//*[@id="amch-tagstime"]/div/div[2]/ul/li/ul/li[2]/a/span').click()
#         time.sleep(1)

#         driver.find_element(By.XPATH, '//*[@id="amch-tagstime"]/div/div[2]/ul/li/ul/li[2]/ul/li[1]/a').click()
        
        
        # THIS MAY BE NECESSARY IF THE SAVE FILE DIALOG BOX COMES UP
        # time.sleep(10)
        # import keyboard
        # keyboard.press_and_release('enter')
        
        

        # time.sleep(1)

        ###############################################################################################################
        # GET ADDITIONAL DATA FROM PAGE   ##### LATER THIS DATA CAN BE MERGED INTO THE DATASET USING THE APPID

        # GET DIV
        # /html/body/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/p[1]
        # info_div = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/p[1]")

        # href_elems = info_div.find_elements_by_xpath("//a[@href]")

        # for elem in href_elems:
        #     print(elem)
        #     print(elem.get_attribute("href"))

        # current_href_list = []
        # for elem in href_elems:
        #     current_href_list.append(elem.get_attribute("href"))

        # all_devs_list=[]

        # only_devs_list=[]
        # for href in current_href_list:
        #     if "/dev/" in str(href):
        #         only_devs_list.append(re.findall(r'(?<=dev\/)(.*)', str(href))[0])

        #FOR SOME REASON THERE ARE THE SAME N DEVS AT THE START SO GOTTA GET RID OF THEM
        # only_devs_list = only_devs_list[-2:]
        # all_devs_list.append(only_devs_list)

        #LANGUAGES

        # all_langs_list = []
        # only_lang_list=[]
        # for href in current_href_list:
        #     if "/language/" in str(href):
        #         only_lang_list.append(re.findall(r'(?<=language\/)(.*)', str(href))[0])

        #print(only_lang_list)

        # final_lang_list = ['','','','','','','','','','','','','','','','','','','',''] # 20 LANGUAGES SHOULD BE ENOUGH
        
        #FOR SOME REASON THERE ARE THE SAME 18 LANGUAGES AT THE START SO GOTTA GET RID OF THEM
        # count = 0
        # for i in range(18,len(only_lang_list)):
        #     if only_lang_list[i] is not None:
        #         final_lang_list[count] = only_lang_list[i]
        #         count+=1

        # all_langs_list.append(final_lang_list)
        #print(final_lang_list)

        #TAGS
        #MAKE A LIST OF ALL THE TEXT ASSOCIATED WITH LINKS TO MATCH UP THE COUNTS (WRITTEN AS TEXT) WITH THE TAG LABELS (AS LINKS) 

        # only_tags_list=[]
        # all_tags_list = []


        # for href in current_href_list:
        #     if "/tag/" in str(href):
        #         only_tags_list.append(re.findall(r'(?<=tag\/)(.*)', str(href)))

        # final_tags_list = ['','','','','','','','','','','','','','','','','','','',''] # 20 TAGS MAX


        # #FOR SOME REASON THERE ARE THE SAME 23 tags AT THE START SO GOTTA GET RID OF THEM
        # count = 0
        # for i in range(23,len(only_tags_list)):
        #     if only_tags_list[i] is not None:
        #         final_tags_list[count] = only_tags_list[i][0]
        #         count+=1

        # all_tags_list.append(final_tags_list)

        # print(only_tags_list)
        # print(final_tags_list)

        # GET COUNTS FOR TAGS

        # all_tags_and_counts = []
        # tag_counts_list = []
        # p_text = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/p[1]")

        # tag_counts_list = re.findall(r'(?<=\()\d*(?=\))', p_text.text)

        # tags_and_counts = [['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0],
        #                     ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0], ['',0]]

        # tag_counter = 0
        # for i in range(len(final_tags_list)):
        #     if len(final_tags_list[i]) > 0:
        #         tags_and_counts[tag_counter] = [final_tags_list[i], int(str(tag_counts_list[i]))]
        #         tag_counter+=1

        # all_tags_and_counts.append(tags_and_counts)

        # print(tags_and_counts)

        #GET FULL TEXT JUST IN CASE

#         full_text = [p_text.text]

#         #GET DESCRIPTION

#         description = re.findall(r'(.*)(?=\n)', p_text.text)

#         #GET SCORES
#         # old_userscore_list = []

#         old_userscore =  re.findall(r'(?<=Old userscore:)(.*)(?=Metascore)', p_text.text)
#         if len(old_userscore) == 0:
#             old_userscore = ['XXXXXX']
#         # if len(old_userscore) > 0:
#         #     old_userscore_list.append(old_userscore)
#         # else:
#         #     old_userscore_list.append([''])

#         # metascore_list = []

#         metascore =  re.findall(r'(?<=Metascore:)(.*)', p_text.text)
#         if len(metascore) == 0:
#             metascore = ['XXXXXX']
#         # if len(metascore) > 0:
#         #     metascore_list.append(metascore)
#         # else:
#         #     metascore_list.append([''])

#         #GET GENRES
#         # genres_list = []

#         genres =  re.findall(r'(?<=Category:)(.*)', p_text.text)
#         if len(genres) == 0:
#             genres = ['XXXXXX']
#         # genres_list.append(genres)

#         # GET FOLLOWERS
#         # followers_list = []

#         followers =  re.findall(r'(?<=Followers: )(.*)', p_text.text)
#         if len(followers) == 0:
#             followers = ['XXXXXX']
#         followers[0] = followers[0].replace(",","")

#         # followers_list.append(followers)

#         # GET PLAYTIME
#         # playtime_list=[]


#         playtime = re.findall(r'(?<=Playtime total: )(.*)', p_text.text)
#         if len(playtime) == 0:
#             playtime = ['XXXXXX']

#         # playtime_list.append(playtime)

#         # GET YOUTUBE STATS
#         # yt_list=[]

#         yt_stats = re.findall(r'(?<=YouTube stats: )(.*)', p_text.text)
#         if len(yt_stats) == 0:
#             yt_stats = ['XXXXXX']
#         # yt_list.append(yt_stats)

#         # GET CCU STATS
#         # ccu_list = []

#         ccu_stats = re.findall(r'(?<=Peak concurrent players yesterday: )(.*)', p_text.text)
#         if len(ccu_stats) == 0:
#             ccu_stats = ['XXXXXX']
#         # ccu_list.append(ccu_stats)

#         # PREPARE ROWS FOR DF
#         all_rows=[]


#         current_row = [int(current_app_id), 
#                         old_userscore[0], 
#                         metascore[0],
#                         genres[0],
#                         followers[0], 
#                         playtime[0], #
#                         yt_stats[0], #
#                         ccu_stats[0], #

#                         only_devs_list[0],
#                         only_devs_list[1],

#                         final_lang_list[0],
#                         final_lang_list[1],
#                         final_lang_list[2],
#                         final_lang_list[3],
#                         final_lang_list[4],
#                         final_lang_list[5],
#                         final_lang_list[6],
#                         final_lang_list[7],
#                         final_lang_list[8],
#                         final_lang_list[9],
#                         final_lang_list[10],
#                         final_lang_list[11],
#                         final_lang_list[12],
#                         final_lang_list[13],
#                         final_lang_list[14],
#                         final_lang_list[15],
#                         final_lang_list[16],
#                         final_lang_list[17],
#                         final_lang_list[18],
#                         final_lang_list[19],

#                         tags_and_counts[0][0], tags_and_counts[0][1],
#                         tags_and_counts[1][0], tags_and_counts[1][1],
#                         tags_and_counts[2][0], tags_and_counts[2][1],
#                         tags_and_counts[3][0], tags_and_counts[3][1],
#                         tags_and_counts[4][0], tags_and_counts[4][1],
#                         tags_and_counts[5][0], tags_and_counts[5][1],
#                         tags_and_counts[6][0], tags_and_counts[6][1],
#                         tags_and_counts[7][0], tags_and_counts[7][1],
#                         tags_and_counts[8][0], tags_and_counts[8][1],
#                         tags_and_counts[9][0], tags_and_counts[9][1],
#                         tags_and_counts[10][0], tags_and_counts[10][1],
#                         tags_and_counts[11][0], tags_and_counts[11][1],
#                         tags_and_counts[12][0], tags_and_counts[12][1],
#                         tags_and_counts[13][0], tags_and_counts[13][1],
#                         tags_and_counts[14][0], tags_and_counts[14][1],
#                         tags_and_counts[15][0], tags_and_counts[15][1],
#                         tags_and_counts[16][0], tags_and_counts[16][1],
#                         tags_and_counts[17][0], tags_and_counts[17][1],
#                         tags_and_counts[18][0], tags_and_counts[18][1],
#                         tags_and_counts[19][0], tags_and_counts[19][1],
#                         description[0],
#                         full_text[0]]

#         all_rows.append(current_row)

#         df = pd.DataFrame(all_rows, columns = ['app_id_scrap', 
#                                             'old_usrscore_scrap', 
#                                             'metascore_scrap',
#                                             'genres_scrap',
#                                             'followers_scrap',
#                                             'playtime_scrap',
#                                             'youtube_scrap',
#                                             'ccu_scrap',
#                                             'developer_scrap',
#                                             'publisher_scrap',

#                                             'lang_1_scrap',
#                                             'lang_2_scrap',
#                                             'lang_3_scrap',
#                                             'lang_4_scrap',
#                                             'lang_5_scrap',
#                                             'lang_6_scrap',
#                                             'lang_7_scrap',
#                                             'lang_8_scrap',
#                                             'lang_9_scrap',
#                                             'lang_10_scrap',
#                                             'lang_11_scrap',
#                                             'lang_12_scrap',
#                                             'lang_13_scrap',
#                                             'lang_14_scrap',
#                                             'lang_15_scrap',
#                                             'lang_16_scrap',
#                                             'lang_17_scrap',
#                                             'lang_18_scrap',
#                                             'lang_19_scrap',
#                                             'lang_20_scrap',

#                                             'tag_1_scrap', 'tag_1_count',
#                                             'tag_2_scrap', 'tag_2_count',
#                                             'tag_3_scrap', 'tag_3_count',
#                                             'tag_4_scrap', 'tag_4_count',
#                                             'tag_5_scrap', 'tag_5_count',
#                                             'tag_6_scrap', 'tag_6_count',
#                                             'tag_7_scrap', 'tag_7_count',
#                                             'tag_8_scrap', 'tag_8_count',
#                                             'tag_9_scrap', 'tag_9_count',
#                                             'tag_10_scrap', 'tag_10_count',
#                                             'tag_11_scrap', 'tag_11_count',
#                                             'tag_12_scrap', 'tag_12_count',
#                                             'tag_13_scrap', 'tag_13_count',
#                                             'tag_14_scrap', 'tag_14_count',
#                                             'tag_15_scrap', 'tag_15_count',
#                                             'tag_16_scrap', 'tag_16_count',
#                                             'tag_17_scrap', 'tag_17_count',
#                                             'tag_18_scrap', 'tag_18_count',
#                                             'tag_19_scrap', 'tag_19_count',
#                                             'tag_20_scrap', 'tag_20_count',
#                                             'description',
#                                             'full_text'])

#         df.to_csv("step1_steamspy_scraped_data.csv", mode='a', header=False, index=False)

#         print(f"game #{int(current_app_id)} was successful")
#         fail_count = 0

#     except Exception as e:
#         print(f"game #{int(current_app_id)} failed")
#         print(e)
#         logf.write(f"{int(current_app_id)}\n")

#         if fail_count > 2:
#             break
#         else:
#             fail_count+=1

# # for i in range(2):
# #     beepy.beep(6)
# beepy.beep(6)
# # beepy.beep(1)
# # beepy.beep(1)
# # CLOSE BROWSER
# driver.quit()




# # LOG HOW LONG IT TOOK
# print('It took {0:0.1f} seconds'.format(time.time() - start))

# # DO SOMETHING HERE TO CHECK WHAT THE LAST SUCCESSFULLY SCRAPED GAME WAS
# # YOU NEED THE ID OF THE GAME WHERE YOU WANT TO START AGAIN FROM
# # YOU ALSO NEED A LIST OF ANY GAMES THAT WERE UNSUCCESSFUL












###################################################################################################
# UNUSED CODE

# import time
# import keyboard
# from selenium import webdriver 
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# options = webdriver.ChromeOptions() 
# options.add_argument("start-maximized")
# options.add_argument("user-data-dir=chrome-data")

# #chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

# start_url = "https://steamspy.com/login"
# driver.get(start_url)
# time.sleep(100)

# first_game_url = "https://steamspy.com/app/590380"
# driver.get(first_game_url)

# driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/ul/li[12]/a/span').click()
# time.sleep(10)
# driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[11]/div[2]/div/div[2]/ul/li/ul/li[2]/ul/li[1]/a/span').click()
# time.sleep(5)
# keyboard.press_and_release('enter')
# driver.quit()

#username
# //*[@id="login_form"]/div[1]/input
#pass
# //*[@id="login_form"]/div[2]/input
#captcha
# //*[@id="recaptcha-anchor"]
#print(driver.page_source.encode("utf-8"))
#login button
# /html/body/div[3]/div[2]/div/div[2]/div/div/div/div[1]/form/button
# username = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[1]/input')
# password = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[2]/input')
# captcha = driver.find_element(By.XPATH, '//span[@id="recaptcha-anchor"]')
# login_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[1]/form/button')
# username.send_keys("nsysu")
# time.sleep(5)
# password.send_keys("6d12380383ec")
# time.sleep(5)
# driver.find_element_by_name("captcha").click()
# time.sleep(5)
# driver.find_element_by_name("login_button").click()
# time.sleep(10)

#########################################################################


# for i in range(len(gamez)):
#     current_row = [int(gamez[i]), 
#                     old_userscore_list[i][0], 
#                     metascore_list[i][0],
#                     genres_list[i][0],
#                     followers_list[i][0], 
#                     playtime_list[i][0],
#                     yt_list[i][0], 
#                     ccu_list[i][0], 

#                     all_devs_list[i][0],
#                     all_devs_list[i][1],

#                     all_langs_list[i][0],
#                     all_langs_list[i][1],
#                     all_langs_list[i][2],
#                     all_langs_list[i][3],
#                     all_langs_list[i][4],
#                     all_langs_list[i][5],
#                     all_langs_list[i][6],
#                     all_langs_list[i][7],
#                     all_langs_list[i][8],
#                     all_langs_list[i][9],
#                     all_langs_list[i][10],
#                     all_langs_list[i][11],
#                     all_langs_list[i][12],
#                     all_langs_list[i][13],
#                     all_langs_list[i][14],
#                     all_langs_list[i][15],
#                     all_langs_list[i][16],
#                     all_langs_list[i][17],
#                     all_langs_list[i][18],
#                     all_langs_list[i][19],

#                     all_tags_and_counts[i][0][0], all_tags_and_counts[i][0][1],
#                     all_tags_and_counts[i][1][0], all_tags_and_counts[i][1][1],
#                     all_tags_and_counts[i][2][0], all_tags_and_counts[i][2][1],
#                     all_tags_and_counts[i][3][0], all_tags_and_counts[i][3][1],
#                     all_tags_and_counts[i][4][0], all_tags_and_counts[i][4][1],
#                     all_tags_and_counts[i][5][0], all_tags_and_counts[i][5][1],
#                     all_tags_and_counts[i][6][0], all_tags_and_counts[i][6][1],
#                     all_tags_and_counts[i][7][0], all_tags_and_counts[i][7][1],
#                     all_tags_and_counts[i][8][0], all_tags_and_counts[i][8][1],
#                     all_tags_and_counts[i][9][0], all_tags_and_counts[i][9][1],
#                     all_tags_and_counts[i][10][0], all_tags_and_counts[i][10][1],
#                     all_tags_and_counts[i][11][0], all_tags_and_counts[i][11][1],
#                     all_tags_and_counts[i][12][0], all_tags_and_counts[i][12][1],
#                     all_tags_and_counts[i][13][0], all_tags_and_counts[i][13][1],
#                     all_tags_and_counts[i][14][0], all_tags_and_counts[i][14][1],
#                     all_tags_and_counts[i][15][0], all_tags_and_counts[i][15][1],
#                     all_tags_and_counts[i][16][0], all_tags_and_counts[i][16][1],
#                     all_tags_and_counts[i][17][0], all_tags_and_counts[i][17][1],
#                     all_tags_and_counts[i][18][0], all_tags_and_counts[i][18][1],
#                     all_tags_and_counts[i][19][0], all_tags_and_counts[i][19][1]]

#     all_rows.append(current_row)

# df = pd.DataFrame(all_rows, columns = ['app_id_scrap', 
#                                        'old_usrscore_scrap', 
#                                        'metascore_scrap',
#                                        'genres_scrap',
#                                        'followers_scrap',
#                                        'playtime_scrap',
#                                        'youtube_scrap',
#                                        'ccu_scrap',
#                                        'developer_scrap',
#                                        'publisher_scrap',

#                                        'lang_1_scrap',
#                                        'lang_2_scrap',
#                                        'lang_3_scrap',
#                                        'lang_4_scrap',
#                                        'lang_5_scrap',
#                                        'lang_6_scrap',
#                                        'lang_7_scrap',
#                                        'lang_8_scrap',
#                                        'lang_9_scrap',
#                                        'lang_10_scrap',
#                                        'lang_11_scrap',
#                                        'lang_12_scrap',
#                                        'lang_13_scrap',
#                                        'lang_14_scrap',
#                                        'lang_15_scrap',
#                                        'lang_16_scrap',
#                                        'lang_17_scrap',
#                                        'lang_18_scrap',
#                                        'lang_19_scrap',
#                                        'lang_20_scrap',

#                                        'tag_1_scrap', 'tag_1_count',
#                                        'tag_2_scrap', 'tag_2_count',
#                                        'tag_3_scrap', 'tag_3_count',
#                                        'tag_4_scrap', 'tag_4_count',
#                                        'tag_5_scrap', 'tag_5_count',
#                                        'tag_6_scrap', 'tag_6_count',
#                                        'tag_7_scrap', 'tag_7_count',
#                                        'tag_8_scrap', 'tag_8_count',
#                                        'tag_9_scrap', 'tag_9_count',
#                                        'tag_10_scrap', 'tag_10_count',
#                                        'tag_11_scrap', 'tag_11_count',
#                                        'tag_12_scrap', 'tag_12_count',
#                                        'tag_13_scrap', 'tag_13_count',
#                                        'tag_14_scrap', 'tag_14_count',
#                                        'tag_15_scrap', 'tag_15_count',
#                                        'tag_16_scrap', 'tag_16_count',
#                                        'tag_17_scrap', 'tag_17_count',
#                                        'tag_18_scrap', 'tag_18_count',
#                                        'tag_19_scrap', 'tag_19_count',
#                                        'tag_20_scrap', 'tag_20_count'])

# df.to_csv("test222222.csv", index=False)