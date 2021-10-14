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
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")



chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('no-sandbox')
chrome_options.add_argument("user-data-dir=C://Users/gaoan/AppData/Local/Google/Chrome/User Data")

driver = webdriver.Chrome(options=chrome_options)

# iterate through list of restaurant pages stored in "test_links.csv"
# rest_links_list = pd.read_csv("test_links.csv")
# rest_links_list = pd.read_csv("./links/tw_links.csv")
rest_links_list = pd.read_csv("remaining_links.csv")
# rest_links_list = pd.DataFrame({'links': ['f5ek/liu-dian-zhong-yang-sheng-dun-tang']})


for current_rest_link in rest_links_list['links']:

    print(f"trying: https://www.foodpanda.com.tw/en/restaurant/{current_rest_link}")
    
    link_to_scrape = str(f'https://www.foodpanda.com.tw/en/restaurant/{current_rest_link}')

    try:

        full_comments_list = []
        full_dates_list = []
        full_ratings_list = []

        driver.get(link_to_scrape)
        
        print("loading..")
        time.sleep(4)  # Timeout

        driver.find_element(By.XPATH, '//*[@class="vendor-info-main-details"]').click()

        time.sleep(4)  # Timeout

        driver.find_element(By.XPATH, '//*[@data-title="Reviews"]').click()

        time.sleep(4)  # Timeout

        review_info = driver.find_element(By.XPATH, '//*[@id="reviews-panel"]')

        review_dates = review_info.find_elements_by_class_name("f-14")
        for dat in review_dates:
            full_dates_list.append(dat.text)

        review_comments = review_info.find_elements_by_class_name("mt-sm")
        for com in review_comments:
            full_comments_list.append(com.text)

        review_ratings = review_info.find_elements_by_class_name("rating-label")
        for rat in review_ratings:
            full_ratings_list.append(rat.text)

        all_rows = []

        for i in range(len(review_dates)):
            current_row = [current_rest_link, 
                            full_dates_list[i],
                            full_comments_list[i],
                            full_ratings_list[i]]

            print(current_row)

            all_rows.append(current_row)

        df = pd.DataFrame(all_rows, columns = ['current_rest_link', 
                                                            'review_date', 
                                                            'review_comment',
                                                            'review_rating'])

        df.to_csv('tw_menu_comments.csv', mode='a', index=False, header=False, encoding="utf-8")

    except Exception as e:
        print(e)

driver.close()