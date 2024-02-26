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

driver = webdriver.Chrome()
pinnacle_data = []
# Scrape True Value Odds
driver.get("https://www.pinnacle.com/en/basketball/nba/matchups/#period:0")
upcoming_games = driver.find_elements(By.XPATH, '//div[@class="style_dateBar__1adEH"]/following-sibling::div[@class="style_row__yBzX8 style_row__12oAB"]')
urls = []

for game in upcoming_games:
    # Extract game information
    link_element = game.find_element(By.CLASS_NAME, 'style_btn__3I6l1')
    # Stores upcoming game links inside an array
    url = link_element.get_attribute('href')
    urls.append(url)
for url in urls:
    driver.get(url)
    player_props_btn = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID,"player-props"))
)
    player_props_btn.click()
    main_cont = driver.find_element("xpath",'/html/body/div[2]/div[1]/div[2]/main/div[3]')
    div_elements = main_cont.find_elements("xpath",'.//div[@data-test-id="Collapse"]')
    for div_element in div_elements:
        # Extract player name and prop from the span element
        player_prop = div_element.find_element("xpath",'.//span').text
        player, prop = player_prop.split('(')
        prop = prop[:-1]

        # Extract the buttons for Over and Under
        over_button = div_element.find_element("xpath",'.//button[contains(@title, "Over")]')
        under_button = div_element.find_element("xpath",'.//button[contains(@title, "Under")]')

        # Extract line, over, and under values from buttons
        line = over_button.get_attribute('title').split()[1]
        over = over_button.find_element("xpath",'.//span[@class="style_price__3Haa9"]').text
        under = under_button.find_element("xpath",'.//span[@class="style_price__3Haa9"]').text

        [tOver,tUnder] = devig(over, under)
        pinnacle_data.append(store_data(player, prop, line, over, under, tOver, tUnder))
true_vals = pd.DataFrame(pinnacle_data)
print(true_vals)


driver.get("https://unabated.com/nba/props")
