  
'''
constants.py
This file stores all constants needed for app.py and player.py

Author: Gerald Cordova <gerald.cordova@alumni.uncg.edu>
'''

import requests

API_KEY = "PRIVATE - This must be kept private so people cannot impersonate me to access Riot's API"
VERSION_NUM = "9.20.1"
REGION_DICT = {     "br1":"Brazil",
                    "eun1":"EU Nordic & East",
                    "euw1":"EU West",
                    "jp1":"Japan",
                    "kr":"Korea",
                    "la1":"Latin America North",
                    "la2":"Latin America South",
                    "na1":"North America",
                    "oc1":"Oceania",
                    "tr1":"Turkey",
                    "ru":"Russia"}

#A summoner's champions are identified with a numeric ID. We need a way to translate those ID's to string names...
CHAMPION_DATA = "http://ddragon.leagueoflegends.com/cdn/"+VERSION_NUM+"/data/en_US/champion.json"
CHAMPION_DICT = {value['key']:key for key, value in requests.get(CHAMPION_DATA).json()["data"].items()}
#Now we have the game's champion information held as a dictionary of {ID:Name} entries