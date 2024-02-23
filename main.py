# Imports
import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://unabated.com/nba/props")
title = driver.title
driver.implicitly_wait(1)
prop_names = driver.find_element(by=By.CLASS_NAME, value="btn-sm btn-falcon-primary dropdown-toggle btn btn-secondary")
prop_names.click()
print("Complete")

