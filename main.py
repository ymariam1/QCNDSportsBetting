# Imports
import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper import *
import time

driver1 = webdriver.Chrome()
# driver2 = webdriver.Chrome()
pinnacle_data = []
# Scrape True Value Odds
driver1.get("https://www.pinnacle.com/en/basketball/matchups/")
# Click button to view bets on first NBA game
viewPropBtn = WebDriverWait(driver1, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "style_btn__3I6l1"))
)
viewPropBtn.click()
#Clicks on button to view only player props
player_props_btn = WebDriverWait(driver1,10).until(
    EC.element_to_be_clickable((By.ID,"player-props"))
)
player_props_btn.click()


#Looks at all the props and stores them in div_elements
main_cont = driver1.find_element("xpath",'/html/body/div[2]/div[1]/div[2]/main/div[3]')
div_elements = main_cont.find_elements("xpath",'.//div[@data-test-id="Collapse"]')
for div_element in div_elements:
    # Extract player name and prop from the span element
    player_prop = div_element.find_element("xpath",'.//span').text
    player, prop = player_prop.split('(')
    
    # Extract the buttons for Over and Under
    over_button = div_element.find_element("xpath",'.//button[contains(@title, "Over")]')
    under_button = div_element.find_element("xpath",'.//button[contains(@title, "Under")]')
    
    # Extract line, over, and under values from buttons
    line = over_button.get_attribute('title').split()[1]
    over = over_button.find_element("xpath",'.//span[@class="style_price__3Haa9"]').text
    under = under_button.find_element("xpath",'.//span[@class="style_price__3Haa9"]').text

    [tOver,tUnder] = devig(over, under)

    
    # Append the extracted information to the DataFrame
    pinnacle_data.append({'Player': player.strip(), 'Prop': prop[:-1].strip(), 'Line': line, 'Over': over, 'Under': under, 'True Over': tOver, 'True Under': tUnder})
df = pd.DataFrame(pinnacle_data)
# Print the DataFrame
print(df)

time.sleep(5)




# Scrape all odds
"""
driver2.get("https://unabated.com/nba/props")
driver2.implicitly_wait(1)
prop_names = driver2.find_element(by=By.CLASS_NAME, value="btn-sm btn-falcon-primary dropdown-toggle btn btn-secondary")
prop_names.click()
print("Complete")
"""