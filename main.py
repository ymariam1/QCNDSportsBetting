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
import time

driver1 = webdriver.Chrome()
# driver2 = webdriver.Chrome()

# Scrape True Value Odds
driver1.get("https://www.pinnacle.com/en/basketball/nba/matchups/#period:0")
viewPropBtn = WebDriverWait(driver1, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "style_btn__3I6l1"))
)
# Click the first instance of the button
viewPropBtn.click()
div_elements = WebDriverWait(driver1, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@data-collapsed="true" and @data-test-id="Collapse" and contains(@class, "style_marketGroup")]'))
)

player_props_html = []
player_props = []
criteria = [
    "(Points)","(Pts+Reb+Asts)","(Rebounds)", "(3 Point FG)","(Assists)","(Double+Double)"
    ]

for div_element in div_elements:
    # Find the nested span element
    span_element = div_element.find_element(By.XPATH, '//div/span')
    # Get the text content of the span element
    # Check if the text content meets the criteria
    player_props_html.append(div_element)
for player_prop in player_props_html:
    span_element = player_prop.find_element(By.XPATH, './div/span[1]')
    span_text = span_element.text
    if any(substring.lower() in span_text.lower() for substring in criteria):
        player_props.append(span_text)
print(player_props)




# Scrape all odds
"""
driver2.get("https://unabated.com/nba/props")
driver2.implicitly_wait(1)
prop_names = driver2.find_element(by=By.CLASS_NAME, value="btn-sm btn-falcon-primary dropdown-toggle btn btn-secondary")
prop_names.click()
print("Complete")
"""