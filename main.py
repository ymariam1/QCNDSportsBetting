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
driver1.get("https://www.pinnacle.com/en/basketball/nba/matchups/#period:0")
upcoming_games = driver1.find_elements(By.XPATH, '//div[@class="style_dateBar__1adEH"]/following-sibling::div[@class="style_row__yBzX8 style_row__12oAB"]')
urls = []

for game in upcoming_games:
    # Extract game information
    link_element = game.find_element(By.CLASS_NAME, 'style_btn__3I6l1')
    # Extract the href attribute value and append it to the urls list
    url = link_element.get_attribute('href')
    urls.append(url)
    teams = game.find_elements(By.XPATH, './/span[@class="ellipsis event-row-participant style_participant__2BBhy"]')
    team1 = teams[0].text
    team2 = teams[1].text
for url in urls:
    driver1.get(url)
    player_props_btn = WebDriverWait(driver1,10).until(
    EC.element_to_be_clickable((By.ID,"player-props"))
)
    player_props_btn.click()
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
        pinnacle_data.append(store_data(team1, team2, player_prop, line, over, under, tOver, tUnder))
df = pd.DataFrame(pinnacle_data)
print(df)

# Click button to view bets on first NBA game
# viewPropBtn = WebDriverWait(driver1, 10).until(
#     EC.element_to_be_clickable((By.CLASS_NAME, "style_btn__3I6l1"))
# )
# viewPropBtn.click()
#Clicks on button to view only player props



#Looks at all the props and stores them in div_elements

    # Append the extracted information to the DataFrame
    #pinnacle_data.append({'Player': player.strip(), 'Prop': prop[:-1].strip(), 'Line': line, 'Over': over, 'Under': under, 'True Over': tOver, 'True Under': tUnder})

# Print the DataFrame

# Scrape all odds
"""
driver2.get("https://unabated.com/nba/props")
driver2.implicitly_wait(1)
prop_names = driver2.find_element(by=By.CLASS_NAME, value="btn-sm btn-falcon-primary dropdown-toggle btn btn-secondary")
prop_names.click()
print("Complete")
"""