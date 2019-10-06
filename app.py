'''
app.py
The back-end code that provides the logic for the Clarity application.

Author: Gerald Cordova <gerald.cordova@alumni.uncg.edu>
'''

#MODULES
from flask import Flask, render_template, request
import requests, re
from threading import Thread
from queue import Queue

#APPLICATION
appObj = Flask(__name__)

#CONSTANTS
API_KEY = "PRIVATE - This must be kept private so people cannot impersonate me to access Riot's API"
VERSION_NUM = "9.19.1"
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


#ERROR-HANDLING FUNCTIONS
@appObj.errorhandler(400)
@appObj.errorhandler(413)
@appObj.errorhandler(414)
@appObj.errorhandler(500)
def error_handler(e):
    return render_template('error.html', problem="Error - Likely a programming error. Please notify the site owner if possible."), e.code

@appObj.errorhandler(403)
def forbidden_handler(e):
    return render_template('error.html', problem="Error - a 403 Forbidden response was received. Please notify the site owner."), 403

@appObj.errorhandler(404)
@appObj.errorhandler(410)
def page_missing_handler(e):
    return render_template('error.html', problem="Error - You went to a page that doesn't exist"), e.code

@appObj.errorhandler(408)
@appObj.errorhandler(429)
def timeout_handler(e):
    return render_template('error.html', problem="Error - A request timed out or too many are being sent. Please wait and try again."), e.code



#URL-HANDLING FUNCTIONS
@appObj.route("/")
def index():

    #We return an empty lookup page if either parameter is empty/missing
    if empty_params(['region','name_input']):
        return render_template('lookup.html')

    #We return an error message if our region argument is not acceptable
    elif request.args.get('region') != "none" and request.args.get('region') not in REGION_DICT.keys():
        return render_template('error.html')

    #If our name_input parameter has an invalid character in it, we cannot call the API
    elif invalid_character_check():
        return render_template('error.html')

    #If the "Search all regions" option is selected...
    elif request.args.get('region') == "none":
        return search_all_servers( request.args.get('name_input') )

    #If we get here, we must have a region selected and a summoner name containing valid characters
    else:
        return see_summoner( (request.args.get('region'), REGION_DICT[request.args.get('region')]) , request.args.get('name_input'))



#DATA-PROCESSING FUNCTIONS

#Function to check a URL for empty parameters
def empty_params(param_list):

    for param in param_list:
        if request.args.get(param) is None or not request.args.get(param):
            return True
    return False



#Function to seek out invalid characters in the summoner's name
def invalid_character_check():

    #Spaces, \w (Unicode letters including numbers and underscore), and period (.) are allowed
    regex_string = r'^[ \w\.]+$'

    #If None is returned, we didn't find an acceptable name
    return re.search(regex_string, request.args.get('name_input'), flags=re.IGNORECASE) is None



#Function to search Riot's API for a player and render a page with that information
def see_summoner(region_info, summoner_name):

    #Create a URL to access the API, and request the player's information
    summoner_url = "https://"+region_info[0]+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    summoner = requests.get(summoner_url)

    #If we receive a 403 response, either the API is being incorrectly accessed or the API key stored here is expired
    if summoner.status_code == 403:
        return forbidden_handler(summoner.status_code)

    #If we receive a 404 response, it means there is no player, so if it ISN'T a 404 response, we do have a player
    if not summoner.status_code == 404:
        summoner = summoner.json()

        #Now we need the summoner's champions...
        summoner_champ_url = "https://"+region_info[0]+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+summoner["id"]+"?api_key="+API_KEY
        summoner_champ_pool = requests.get(summoner_champ_url).json()

        #Our last request has a lot of extra information in it; now we can slim it down to what we need, just the champion ID's

        #First, we make a list of the player's champions missing a hex chest
        champs_missing_chest = [entry["championId"] for entry in summoner_champ_pool if not entry["chestGranted"]]
        #The champions that a summoner has never played are not included in the previous list, so we have to collect them next
        champs_never_played = [int(x) for x in CHAMPION_DICT if int(x) not in [entry["championId"] for entry in summoner_champ_pool]]
        #By extending this list, we now have a list of all the champions a summoner can earn a hex chest on, in order of mastery points
        champs_missing_chest.extend(champs_never_played)

        #Now we convert the list of champion IDs into a list of champion names
        champ_names_missing_chest = [CHAMPION_DICT[str(key)] for key in champs_missing_chest]

        #Getting the URL of the profile icon of the summoner - it'll be used to help identify the account that's shown on the page
        summoner_icon_url = "http://ddragon.leagueoflegends.com/cdn/"+VERSION_NUM+"/img/profileicon/"+str(summoner["profileIconId"])+".png"

        #Now we're missing the overall mastery progress of every champion on the summoner's account

        #I'm going to want a list of lists. Each list will contain champions fitting within a specific mastery level for the summoner
        champ_level_list = [[] for _ in range(8)] #8 lists because there are 8 levels --> 0 through 7

        #We have all the champions at level 0 mastery in a previous list, so we'll use that
        #Also, I'm using a dictionary within the list because I have specific information I want at each mastery level
        champ_level_list[0] = [{"name":CHAMPION_DICT[str(x)]} for x in champs_never_played]
        #Iterate through the remaining 7 lists adding general information; when we render the html template, we can specify which information is relevant to display
        for i in range(1, len(champ_level_list)):
            champ_level_list[i] = [     { "name":CHAMPION_DICT[str(x["championId"])],
                                          "xp":x["championPointsSinceLastLevel"], 
                                          "xpLeft":x["championPointsUntilNextLevel"], 
                                          "tokens":x["tokensEarned"]                 } for x in summoner_champ_pool if x["championLevel"] == i]

        #Condensing relevant information into a list to send to html template in the return statement
        summoner_info = [summoner["name"], summoner["summonerLevel"], region_info[1]]

        #Finally done processing information; render the webpage
        return render_template('summoner.html',
                                lookup=True,
                                summoner=summoner_info,
                                icon_url=summoner_icon_url,
                                chest_option_list=champ_names_missing_chest,
                                champ_list_by_mastery=champ_level_list,
                                VERSION=VERSION_NUM)

    #This is our return for the case in which a 404 response is received
    return render_template('error.html', problem='Summoner by that name does not exist on that server, please try a different name or server')


#League of Legends is an international game - players are separated by regions, so they have relatively close servers to communicate with for low-latency gameplay
#This function searches all of Riot's servers across the globe for summoners who match a particular name
def search_all_servers(summoner_name):

    #We'll populate this list with tuples of players that exist in different servers
    valid_results = []

    #Threads will be used to check each server so the search time is reasonable (not using threads means a search takes ~20 seconds)
    threads = [None] * len(REGION_DICT)
    q = Queue() #The queue is to have a thread-independent collection for results

    #Create and start each thread, using the function "region_check" to search for summoners
    for region, region_name in REGION_DICT.items():
        current_index = threads.index(None)
        threads[current_index] = Thread(target=region_check, args=(q, (region, region_name), summoner_name))
        threads[current_index].start()

    #Join all threads before proceeding
    for i in range(len(threads)):
        threads[i].join()

    #Empty the queue (full of valid summoner information from different servers) into our list that we defined at the beginning of this function
    while not q.empty():
        item = q.get()
        if item == 403: #If 403 is in the queue, something is wrong and we need to return an error stating such
            return forbidden_handler(403)
        valid_results.append( item )

    #Render the webpage, but sort results based on alphabetical order of the region name 
    #(Otherwise the displayed order of results is based on which thread finishes first, which is incconsistent)
    return render_template('search.html', search_results=sorted(valid_results, key=lambda x: x[0]), VERSION=VERSION_NUM)


#Our thread function - This function will check the region passed as an argument for a player, and if found, add it to the queue
def region_check(queue_obj, region_tuple, summoner_name):

    #Create a URL to access the API, and request the player's information
    summoner_url = "https://"+region_tuple[0]+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summoner_name+"?api_key="+API_KEY
    response = requests.get(summoner_url)

    #If a 403 response is received, add it to the queue, we'll render an error page after all threads are joined
    if response.status_code == 403:
        queue_obj.put(403)

    #If a 404 response is received, the player doesn't exist, so we don't need to do anything else in this thread
    #Otherwise, it is assumed we found a player with matching name in the region, so let's get their information
    elif not response.status_code == 404:

        enc_summ_id = response.json()["id"] #Need this information for the next URL being constructed

        #Calling the API here to get the player's rank information, which is an indicator of how skilled they are within the region's playerbase
        rank_url = "https://"+region_tuple[0]+".api.riotgames.com/lol/league/v4/entries/by-summoner/"+enc_summ_id+"?api_key="+API_KEY
        rank_response = requests.get(rank_url).json()

        #League of Legends has a few different ways that a player can be ranked, we're interested in a player's solo 5 vs 5 ranking
        #"rank_response" (from a few lines ago) is a LIST of ranked results for whatever ranked queues a summoner is in
        for x in rank_response:
            if x["queueType"] == "RANKED_SOLO_5x5":
                rank_and_tier = x["tier"] + " " + x["rank"]
                break
        else:
            rank_and_tier = "Player does not have a solo/duo rank!"

        #Same as the see_summoner function - now we need some champion mastery information, so we're calling the API here
        champ_url = "https://"+region_tuple[0]+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+enc_summ_id+"?api_key="+API_KEY
        champ_response = requests.get(champ_url).json()

        #It is possible that a player's account has no champion mastery experience, so we have to check for that
        if len(champ_response) >= 1:
            #Put together a list of the summoner's 6 most played champions; we only need their names
            most_played = [CHAMPION_DICT[str(champ["championId"])] for champ in champ_response[0:6]]
        else:
            most_played = "Player has not played any matches granting champion mastery!"

        #Add a tuple of the information we need to the queue, we'll pull it from the queue after joining all threads
        queue_obj.put( (region_tuple[1], response.json(), rank_and_tier, most_played, region_tuple[0]) )


if __name__ == "__main__":
    appObj.run()