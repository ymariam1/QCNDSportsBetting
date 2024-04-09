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

api_data = pd.read_csv("apiData.csv")
pinnacle_data = pd.read_csv("pinnacle_data.csv")
pinnacle_data = pinnacle_data.drop(columns=['Team'])

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
            if len(pinnacle_line) > 0:
                row['Prop'] = simplify_props(row['Prop'])
                comp_data.append(row)
        comp_data = pd.DataFrame(comp_data)
        if not comp_data.empty:
            comparison = comp_data[(comp_data['tOver'] > comp_data['impOver']) | (comp_data['tUnder'] > comp_data['impUnder'])]
            if not comparison.empty:
                if (comparison['tOver'] > comparison['impOver']).any():
                    print("Over")
                    comparison.loc[:, 'ev'] = findEv(comparison['Under_api'], comparison['tOver'], 100)
                    comparison.loc[:,'kelly'] = calcKcrit(comparison['tOver'], comparison['tUnder'], comparison['Over_api'])
                elif (comparison['tUnder'] > comparison['impUnder']).any():
                    print("Under")
                    comparison.loc[:,'ev'] = findEv(comparison['Under_api'], comparison['tOver'], 100)
                    comparison.loc[:,'kelly'] = calcKcrit(comparison['tOver'], comparison['tUnder'], comparison['Under_api'])
                if (comparison['ev'] > 100).any():
                    print(comparison)
                

            

