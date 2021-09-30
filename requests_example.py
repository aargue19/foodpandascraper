import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# "steamdb_tag_codes_raw.txt" is the raw source from the page "view-source:https://steamdb.info/tags/"

# HERE I PARSE THE HTML TO GET THE TAG NAME, TAG CODE AND COUNT

with open('steamdb_tag_codes_raw.txt') as f:
    read_data = f.read()
    page_content = BeautifulSoup(read_data, "html.parser")

list_of_links = page_content.find_all("a", {"class": "label-link"}, href=True)

list_of_codes = []

for lnk in list_of_links:
    list_of_codes.append(re.findall("(?<=tag/)(.*)(?=/ )", str(lnk))[0])

list_of_counts = page_content.find_all("span", {"class": "label-count"})

list_of_counts_clean = []

for cnt in list_of_counts:
    list_of_counts_clean.append(re.findall('(?<=\<span class="label-count flex-grow muted">)(.*)(?= products)', str(cnt))[0])

all_rows=[]

for i in range(len(list_of_links)):
    current_row = [list_of_codes[i], list_of_links[i].text, list_of_counts_clean[i]]
    all_rows.append(current_row)

df = pd.DataFrame(all_rows, columns = ['tag_code', 'tag_name', 'tag_count'])
    
df.to_csv("tag_names_codes_counts.csv", index=False)