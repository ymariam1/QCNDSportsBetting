from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def devig(over, under):
    # Assumes decimal Odds
    over = float(over)
    under = float(under)
    # Finds implied odds for over/under
    if (over != 0 and under != 0):
        impO = (100/over)
        impU = (100/under)
    else:
        return [0,0]
    # Normalizes odds by removing vig
    true_over = impO/(impO+impU) 
    true_under = impU/(impO+impU)
    return [true_over, true_under]

def findPercent(over, under):
    over = float(over)
    under = float(under)
    # Finds implied odds for over/under
    if (over != 0 and under != 0):
        impO = (100/over) / 100
        impU = (100/under) / 100
    else:
        return [0,0]
    return [impO, impU]

    

def store_data(team, player, prop, line, over, under, true_over, true_under):
    # Append the data to the list as a dictionary
    return {
        'Team': team,
        'Player': player,
        'Prop': prop,
        'Line': line,
        'Over': over,
        'Under': under,
        'tOver': true_over,
        'tUnder': true_under
    }
def team_shorten(team):
    # Shorten team name to match with unabated team names
    team_name_map = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Charlotte Hornets": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Brooklyn Nets": "BKN",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHO",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTH",
        "Washington Wizards": "WAS"
    }
    return team_name_map.get(team, "Unknown")

def find_button_with_text(driver, text):
    return WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
    )

def propToMarket(prop):
    player_prop_map = {'3 Point FG': "player_threes",
     'Assists': "player_assists",
     'Points': "player_points",
     'Pts+Rebs+Asts': "player_points_rebounds_assists",
     'Rebounds': "player_rebounds",
    'Double+Double': "player_double_double",
    'Triple+Double': "player_triple_double"
    }
    return player_prop_map.get(prop, "Unknown")

def simplify_props(prop):
    player_prop_map = {
        'player_assists': "assists",
        'player_points': 'points',
        'player_threes': 'threes',
        "player_rebounds": "rebounds",
        "player_points_rebounds_assists": "P+A+R",
        "player_double_double": "Double double",
        "player_triple_double": "Triple double"
    }
    return player_prop_map.get(prop, "Unkown")

def findEv(row):
    win_multiplier = otm(row['price'])
    
    true_prob = row['tOver'] if row['direction'] == 'Over' else row['tUnder']
    
    ev = (true_prob * (win_multiplier - 1)) - (1 - true_prob)
    return ev
    
def calcKelly(row):
    decimal_odds = otm(row['price'])
    b = decimal_odds - 1
    p = row['tOver'] if row['direction'] == 'Over' else row['tUnder']
    q = 1 - p
    
    f = (b * p - q) / b if b != 0 else 0
    
    f = max(min(f, 1), 0)
    return f

def americanOdds(odds):
    if odds != 100:
        prob = ((-1*odds)/((-1*(odds))+100))
    else:
        return 0.5
    return prob

def dta(odds):
    if odds == 1:
        return None
    elif odds >= 2:
        aodds = (odds-1)*100
    else:
        aodds = (-100)/(odds-1)
    return aodds

def otm(odds):
    if odds > 0:
        return odds / 100 + 1
    else:
        return 100 / abs(odds) + 1
    