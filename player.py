'''
player.py
This file defines the Player class and is where any needed calls
to Riot's API is located.

Author: Gerald Cordova <gerald.cordova@alumni.uncg.edu>
'''

import requests
from threading import Thread
from queue import Queue

import constants as CONST

class Player:

    #Init function -- Needs a region code and player name or we cannot do anything
    def __init__(self, region_code, name):
        self.region_code = region_code
        self.region_name = CONST.REGION_DICT[region_code]
        self.name = name
        self.is_real()

    #A function to see if the player exists, and set appropriate attributes to the Player object
    def is_real(self):
        http_response = requests.get("https://"+self.region_code+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+self.name+"?api_key="+CONST.API_KEY)
        if http_response.status_code != 403 and http_response.status_code != 404:
            self.exists = True
            self.find_data(http_response.json())
        else:
            self.exists = False
            self.error = http_response.status_code

    #This function is ran when we know a player exists, and it gathers a lot of information to be rendered with the HTML template
    def find_data(self, summoner): #Arg is named "summoner" because the arg is some identification info about the player, needed to use the API
        ''' self.name needs to be re-assigned here because searches are case insensitive.
            For example: input could be "steve" and the API will return "STeve" from one server and "STEVE" from a different server.
            That is an acceptable behavior, but I want to return the correct casing of the name, so it's being re-assigned here. '''
        self.name = summoner["name"]
        
        self.level = summoner["summonerLevel"]
        self.icon_id = summoner["profileIconId"]

        #Using a thread to speed up execution - 2 API calls are necessary, but doing one after the other is too slow
        q = Queue()
        thread = Thread(target=self.get_lists, args=(q, summoner))
        thread.start() #API call #1 during thread

        self.rank = self.get_rank(summoner) #API call #2

        thread.join()
        info_dict = q.get()
        self.chest_champs = info_dict["chestOptions"]
        self.mastery_lists = info_dict["masteryProgress"]
        self.most_played = info_dict["mostPlayed"]


    #A function to find the player's rank, which is an indicator of how skilled they are within the region's playerbase
    def get_rank(self, summoner):
        rank_url = "https://"+self.region_code+".api.riotgames.com/lol/league/v4/entries/by-summoner/"+summoner["id"]+"?api_key="+CONST.API_KEY
        rank_response = requests.get(rank_url).json()

        #League of Legends has a few different ways that a player can be ranked, we're interested in a player's solo 5 vs 5 ranking
        #"rank_response" is a LIST of ranked results for whatever ranked queues a summoner is in
        for x in rank_response:
            if x["queueType"] == "RANKED_SOLO_5x5":
                return x["tier"] + " " + x["rank"]
        return "Player does not have a solo/duo rank!"


    #A function to compile a few lists of champion-based information relating to the player/summoner
    def get_lists(self, queue, summoner):

        #First, we get the list of chest options..

        #Now we need the summoner's champions that he/she has played at least once...
        summoner_champ_url = "https://"+self.region_code+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summoner["id"]+"?api_key="+CONST.API_KEY
        summoner_champ_pool = requests.get(summoner_champ_url).json()

        #Next, we make a list of the player's champions that are eligible to earn a chest
        champs_missing_chest = [entry["championId"] for entry in summoner_champ_pool if not entry["chestGranted"]]
        #The champions that a summoner has never played are not included in the previous list, so we have to collect them next
        champs_never_played = [int(x) for x in CONST.CHAMPION_DICT if int(x) not in [entry["championId"] for entry in summoner_champ_pool]]
        #By extending this list, we now have a list of all the champions a summoner can earn a hex chest on, in order of mastery points
        champs_missing_chest.extend(champs_never_played)

        #Finally, we convert the list of champion IDs into a list of champion names
        chestOptions = [CONST.CHAMPION_DICT[str(key)] for key in champs_missing_chest]


        #Second, we get the list showing champion mastery progress..

        #I'm going to want a list of lists. Each list will contain champions fitting within a specific mastery level for the summoner
        champ_level_list = [[] for _ in range(8)] #8 lists because there are 8 levels --> 0 through 7

        #We have all the champions at level 0 mastery in a previous list, so we'll use that
        #Also, I'm using a dictionary within the list because I have specific information I want at each mastery level
        champ_level_list[0] = [{"name":CONST.CHAMPION_DICT[str(x)]} for x in champs_never_played]
        #Iterate through the remaining 7 lists adding general information; when we render the html template, we can specify which information is relevant to display
        for i in range(1, len(champ_level_list)):
            champ_level_list[i] = [     { "name":CONST.CHAMPION_DICT[str(x["championId"])],
                                          "xp":x["championPointsSinceLastLevel"], 
                                          "xpLeft":x["championPointsUntilNextLevel"], 
                                          "tokens":x["tokensEarned"]                 } for x in summoner_champ_pool if x["championLevel"] == i]

        #Finally, we need a small list of the player's most played champions
        top_champs = [CONST.CHAMPION_DICT[str(champion["championId"])] for champion in summoner_champ_pool[0:6] if champion["championLevel"] > 0]

        #Finally we return all of our lists, in the form of a dict
        queue.put({"chestOptions":chestOptions, "masteryProgress":champ_level_list, "mostPlayed":top_champs})