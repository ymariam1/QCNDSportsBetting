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
import os

api_data = pd.read_csv("apiData.csv")
pinnacle_data = pd.read_csv("pinnacle_data.csv")

players = api_data['Player'].unique()
props = api_data['Prop'].unique()
arb_opps = []
merged_data = pd.merge(api_data,pinnacle_data, on=['Player', 'Prop'], suffixes=('_api', '_pinnacle'))
merged_data = merged_data.drop_duplicates()
for player in players:
    for prop in props:
        comp_data = []
        subset_df = merged_data[(merged_data['Player'] == player) & (merged_data['Prop'] == prop)]
        for index, row in subset_df.iterrows():
    # Extract the API line and pinnacle line for the current row
            api_line = row['Line_api']
            pinnacle_line = pinnacle_data.loc[(pinnacle_data['Player'] == row['Player']) & (pinnacle_data['Prop'] == row['Prop']), 'Line'].values
            # Check if the API line matches the pinnacle line
            if len(pinnacle_line) > 0:
                comp_data.append(row)
        comp_data = pd.DataFrame(comp_data)
        if not comp_data.empty:
            print(comp_data)