import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper import *

pdata = pd.read_csv("pinnacle_data.csv")
tbets = pd.read_csv("Tuesday_bets.csv")
pdata.drop('Team', axis=1, inplace=True)
tbets.drop('game_id', axis=1, inplace=True)
tbets.drop('home_team', axis=1, inplace=True)
tbets.drop('away_team', axis=1, inplace=True)
pdata.rename(columns={'Prop':'market'}, inplace=True)
pdata.rename(columns={'Player':'player'}, inplace=True)
tbets['prob'] = tbets['price'].apply(americanOdds)
pdata.drop('Over',axis=1,inplace=True)
pdata.drop('Under',axis=1,inplace=True)

for df in [pdata, tbets]:
    df['player'] = df['player'].str.lower().str.strip()
    df['market'] = df['market'].str.lower().str.strip()

combined_df = pd.merge(tbets, pdata, on=['player','market'], suffixes=('_m','_t'))
combined_df["EV"] = combined_df.apply(findEv, axis=1)
good_bets = combined_df[combined_df['EV']>0]
better_bets = good_bets[combined_df['Line'] == combined_df['value']]
better_bets['kelly'] = better_bets.apply(calcKelly, axis = 1)
better_bets.sort_values(by=['kelly'], ascending=False, inplace=True)
better_bets.to_excel("day_1_bets.xlsx")

