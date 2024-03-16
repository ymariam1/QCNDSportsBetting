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
import os

# Get API key from enviornment
API_KEY = os.getenv('API_KEY')
true_vals =pd.read_csv("pinnacle_data.csv")

# Collect player, away team, and prop names in two seperate dfs
players = true_vals["Player"].unique()
players = [player.strip() for player in players]
props = true_vals['Prop'].unique()
away_teams = true_vals["Team"].unique().tolist()
# Things needed for the api call
MARKETS = []

for prop in props:
    MARKETS.append(prop)

SPORT = 'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'
# Checks if api has already been stored as an API
if os.path.exists('api_response.json'):
    with open('api_response.json', 'r') as f:
        api_response = json.load(f)
else:
    # Collect Game ids
    gameInfo = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events?apiKey={API_KEY}')
    if gameInfo.status_code == 200:
        event_ids = []
        for event in gameInfo.json():
            if event["away_team"] in away_teams:
                event_ids.append(event['id'])
        api_response = []
        # Gets info for every game
    for EVENT_ID in event_ids:
        for MARKET in MARKETS:
            response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/events/{EVENT_ID}/odds?apiKey={API_KEY}&regions={REGIONS}&markets={MARKET}&dateFormat={DATE_FORMAT}&oddsFormat={ODDS_FORMAT}')
            api_response.append(response.json())
        # Stores in a json file
    with open('api_response.json', 'w') as f:
        json.dump(api_response, f)

filtered_response = []
# Clean data, ensure there are both over and under prices for each player
for event in api_response:
    for bookmaker in event['bookmakers']:

        bookmaker_title = bookmaker['title']
        for market in bookmaker['markets']:
            if market['key'] in MARKETS:
                market_last_update = market['last_update']
                filtered_outcomes = []
                for outcome in market['outcomes']:
                    player = outcome["description"]   
                    if 'price' in outcome and 'point' in outcome:
                        if player in players:
                            filtered_outcomes.append(outcome)
                
                # Append only if both 'price' and 'point' are present in at least one outcome
                if filtered_outcomes:
                    market['outcomes'] = filtered_outcomes
                    filtered_response.append(event)

api_data_list = []

for event in filtered_response:
    for bookmaker in event['bookmakers']:
        bookmaker_title = bookmaker['title']
        for market in bookmaker['markets']:
            if market['key'] in MARKETS:
                for outcome in market['outcomes']:
                    player = outcome['description']
                    player_prop = market["key"]
                    prop = outcome['name']
                    price = outcome['price']
                    if 'Over' in prop:
                        over_price = price
                    elif 'Under' in prop:
                        under_price = price
                    line_value = outcome["point"]
                
                # Print the formatted output
                true_over,true_under = devig(over_price, under_price)
                api_data_list.append({
                            'Book Maker': bookmaker_title,
                            'Player': player,
                            'Prop': player_prop,
                            'Line': line_value,
                            'Over': over_price,
                            'Under': under_price,
                            'tOver': true_over,
                            'tUnder': true_under
                })
api_data = pd.DataFrame(api_data_list)
csv_file = "apiData.csv"
api_data.to_csv(csv_file, index=False)

