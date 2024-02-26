def devig(over, under):
    # Assumes decimal Odds
    over = float(over)
    under = float(under)
    # Finds implied odds for over/under
    impO = (100/over)
    impU = (100/under)
    # Normalizes odds by removing vig
    true_over = impO/(impO+impU) 
    true_under = impU/(impO+impU)
    return [true_over, true_under]

def store_data(player, prop, line, over, under, true_over, true_under):
    # Append the data to the list as a dictionary
    return {
        'Player': player,
        'Prop': prop,
        'Line': line,
        'Over': over,
        'Under': under,
        'True Over': true_over,
        'True Under': true_under
    }
