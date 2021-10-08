###################################################################################################
# STEP 1: GET ALL THE LINKS TO RESTAURANTS
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
# driver.get('https://www.foodpanda.com.tw/restaurants/new?lat=22.6548347&lng=120.2880371&vertical=restaurants&cuisines=248') #taiwanese cuisine = 248
# driver.get('https://www.foodpanda.com.tw/restaurants/new?lat=22.6548347&lng=120.2880371&vertical=restaurants&cuisines=179') #american cuisine = 179
driver.get('https://www.foodpanda.com.tw/restaurants/new?lat=22.6548347&lng=120.2880371&vertical=restaurants&cuisines=179') #burgers cuisine = 177
# ADD MORE CUISINE LINKS HERE





time.sleep(2)  # Timeout

#SCROLL TO THE BOTTOM TO LOAD ALL THE LINKS

SCROLL_PAUSE_TIME = 2

elements = driver.find_elements_by_tag_name('p')
string_to_check = elements[0].text
number_found = re.findall(r'^[0-9]*', str(string_to_check))
number_found = int(number_found[0])

print(number_found)

how_many = []

while len(how_many)<number_found:                                                          #the number quoted at the top of the page isn't right sometimes
    # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.5);")
        
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight, {behavior: 'smooth'});")
        
        # time.sleep(2) 

        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        how_many = driver.find_elements_by_class_name("vendor-picture")

        print(len(how_many))

        # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #         break
        # last_height = new_height


# ONCE SCROLLED ALL THE WAY TO THE BOTTOM GET ALL LINKS ON PAGE

href_elems = driver.find_elements_by_xpath("//a[@href]")

elem_list = []

for elem in href_elems:
        target_string = elem.get_attribute("href")

        if "/restaurant/" in str(target_string):
                elem_list.append(re.findall(r'(?<=restaurant\/)(.*)', str(target_string))[0])


# WRITE TO FILE (REMEMBER TO CHANGE FILENAME BELOW)

print(len(elem_list))

df = pd.DataFrame({'links': elem_list})

df.to_csv("burger_links.csv", index=False)
