from requests import get
from io import StringIO
import numpy as np
import pandas as pd

def getPlayers():
    df = pd.read_csv(StringIO(get('https://pastebin.com/raw/WEf5d2fm').text))
    return df[['Player','Division']]

def getMatches():
    games = pd.read_csv(StringIO(get('https://pastebin.com/raw/eTmbZM46').text))
    games_grouped = games.groupby(['MatchID','Division','Week','Match'])
    lm = lambda x:max(set(list(x)), key=list(x).count)
    matches = pd.merge(games_grouped.agg({'Winner':lm,'Loser':lm}), 
                       games_grouped.agg(lambda x: tuple(x)), 
                       left_index=True, right_index=True, suffixes=('','_list')).reset_index()
    #calculate penalties for mid-match forfeits
    lm = lambda x:sum(np.where(np.repeat(x[0], len(x[1])) == np.array(x[1]), np.isnan(x[2]), 0))
    w_penalty = [lm(x) * 2 for x in matches[['Loser','Winner_list','L Clears']].values]
    l_penalty = [(lm(x) in [1, 2]) * 2 for x in matches[['Loser','Loser_list','L Clears']].values]
    #calculate match point totals
    is_sweep = [~np.isin(x[0], x[1]) for x in matches[['Loser','Winner_list']].values]
    matches['W Pts'] = np.where(is_sweep, 4, 3) - w_penalty
    matches['L Pts'] = np.where(is_sweep, 0, 1) - l_penalty
    repl_df = pd.read_csv(StringIO(get('https://pastebin.com/raw/0kyaPRqX').text))
    replacements = repl_df.to_dict('records')
    for repl in replacements:
        matches['Winner'].str.replace(repl['Old'], repl['New'])
        matches['Loser'].str.replace(repl['Old'], repl['New'])
    return matches[['Winner','Loser','W Pts','L Pts']]
    
def adjustMatches(matches):
    df = pd.DataFrame(matches[['Winner','Loser','W Pts']].values.tolist() +
                      matches[['Loser','Winner','L Pts']].values.tolist(),
                      columns = ['Player','Opponent','Pts'])
    totalpts = df.groupby(['Player']).agg({'Pts':'sum','Opponent':'count'}).reset_index()
    totalpts = totalpts.rename(columns={'Pts':'Total Pts','Opponent':'Games Played'})
    opp_pts = totalpts.rename(columns={'Player':'Opponent','Total Pts':'Opponent Total Pts','Games Played':'Opponent Games Played'})
    merged = pd.merge(pd.merge(df, totalpts, on='Player'), opp_pts, on='Opponent')
    return merged[['Player','Opponent','Pts','Total Pts','Opponent Total Pts','Games Played']]
    
def getPointLog():
    games = pd.read_csv(StringIO(get('https://pastebin.com/raw/eTmbZM46').text))
    points = pd.DataFrame(games[['Winner','Loser','W Clears','W GmOv','W TB']].values.tolist() +
                          games[['Loser','Winner','L Clears','L GmOv','L TB']].values.tolist(), 
                          columns= ['Player','Opponent','Clears','GmOv','TB'])
    points = points[~np.isnan(points['Clears'])]
    points['Pts'] = points['Clears'] - points['GmOv']
    played = points.groupby(['Player']).agg({'Clears':'count'}).reset_index()
    played = played.rename(columns={'Clears':'Games Played'})
    merged = pd.merge(points, played, on='Player')
    return merged

def getUnplayed():
    matches = pd.read_csv(StringIO(get('https://pastebin.com/raw/rmb6A8uW').text))
    return matches[['Home','Away']]