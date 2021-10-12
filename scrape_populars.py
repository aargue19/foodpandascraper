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
# current_rest_link = "https://www.foodpanda.com.tw/en/restaurant/z7jm/da-hao-niu-pai-gao-xiong-re-he-dian"

# iterate through list of restaurant pages stored in "test_links.csv"
rest_links_list = pd.read_csv("test_links.csv")

for current_rest_link in rest_links_list['links']:
    
    print(f"trying: https://www.foodpanda.com.tw/en/restaurant/{current_rest_link}")
    
    link_to_scrape = str(f'https://www.foodpanda.com.tw/en/restaurant/{current_rest_link}')

    try:

        driver.get(link_to_scrape)
        
        
        print("loading..")
        time.sleep(4)  # Timeout


        print("getting info..")
        # GET RESTAURANT NAME
        rest_title = driver.find_elements_by_tag_name('h1')[0].text

        print(rest_title)

        # GET RATING
        rest_rating = driver.find_elements_by_class_name("rating-label")[0].text

        print(rest_rating)

        # GET DEAL NAME
        if len(driver.find_elements_by_class_name("deal-name")) > 0:
            deal_name = driver.find_elements_by_class_name("deal-name")[0].text
        else:
            deal_name = "NA"

        print(deal_name)

        # GET DEAL DESCRIPTION
        if len(driver.find_elements_by_class_name("deal-name")) > 0:
            deal_desc = driver.find_elements_by_class_name("deal-desc")[0].text
        else:
            deal_desc = "NA"

        print(deal_desc)

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

        print("getting menu..")
        
        # GET DISH CATEGORIES 
        dish_cat_sections = driver.find_elements_by_class_name("dish-category-section")

        dish_cats_list = []
        full_menu_items_list = []
        full_prices_list = []
        full_discounts_list = []
        full_pic_list = []
        full_info_list = []
        full_ratings_list = []


        # GET DISH CATEGORIES 
        dish_cat_sections = driver.find_elements_by_class_name("dish-category-section")

        dish_cats_list = []
        full_menu_items_list = []
        full_prices_list = []
        full_discounts_list = []
        full_pic_list = []
        full_info_list = []
        full_ratings_list = []

        elem = dish_cat_sections[0]

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

            # print(full_menu_items_list)
            # print(len(full_menu_items_list))
            # print(full_prices_list)
            # print(len(full_prices_list))
            # print(full_discounts_list)
            # print(len(full_discounts_list))
            # print(full_pic_list)
            # print(len(full_pic_list))

            if len(full_menu_items_list) < 6:
                diff_len = 6 - len(full_menu_items_list)
                for i in range(diff_len):
                    full_menu_items_list.append("NA") 
                    full_prices_list.append("NA") 
                    full_discounts_list.append("NA") 
                    full_pic_list.append("NA") 

            if len(full_discounts_list) == 0:
                full_discounts_list = ["NA","NA","NA","NA","NA","NA"]

        print(full_menu_items_list)
        print(full_prices_list)
        print(full_discounts_list)
        print(full_pic_list)

        print("writing to file..")
        
        #prepare rows for df

        all_rows = []

        for i in range(6):
            current_row = [current_rest_link, 
                            rest_title,
                            rest_rating,
                            deal_name,
                            deal_desc,
                            full_menu_items_list[i],
                            full_prices_list[i],
                            full_discounts_list[i],
                            full_pic_list[i]]

            print("current row")
            print(current_row)


            all_rows.append(current_row)

        print("all rows")
        print(all_rows)

        df = pd.DataFrame(all_rows, columns = ['current_rest_link', 
                                                    'rest_title', 
                                                    'rest_rating',
                                                    'deal_name',
                                                    'deal_desc',
                                                    'full_menu_items_list',
                                                    'full_prices_list',
                                                    'full_discounts_list',
                                                    'full_pic_list'])

        df.to_csv('existing.csv', mode='a', index=False, header=False, encoding="utf-8")
    
    except Exception as e:
        print(e)

driver.close()