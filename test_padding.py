# # full_menu_items_list = ["A","B","C","D","E","F"]
# full_menu_items_list = ["A","B"]


# print(full_menu_items_list)
# print(len(full_menu_items_list))

# if len(full_menu_items_list) < 6:
#     diff_len = 6 - len(full_menu_items_list)
#     for i in range(diff_len):
#         full_menu_items_list.append("NA") 
#     print(full_menu_items_list)

# else:
#     print("haz 6")

import pandas as pd

rest_links_list = pd.read_csv("test_links.csv")

print(rest_links_list)