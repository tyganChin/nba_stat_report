## Name    : getInfo.py
## Author  : Tygan Chin
## Purpose : Creates list of nba players and saves it to players.json

from nba_api.stats.static import players
import os, json

def setHome():
    playerList = (players.get_players())
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'data', 'players.json')
    with open(file_path, "w") as file:
        json.dump(playerList, file, indent=4)
