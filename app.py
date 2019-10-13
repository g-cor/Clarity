'''
app.py
This file starts the application, instantiates Player objects using
information passed by the user, and decides which HTML template
should be getting rendered.

Author: Gerald Cordova <gerald.cordova@alumni.uncg.edu>
'''

#MODULES
from flask import Flask, render_template, request
import re
from threading import Thread
from queue import Queue

#OTHER PROJECT FILES
from player import Player

#APPLICATION
appObj = Flask(__name__)

#CONSTANTS
import constants as CONST

#ERROR-HANDLING FUNCTIONS
@appObj.errorhandler(400)
@appObj.errorhandler(413)
@appObj.errorhandler(414)
@appObj.errorhandler(500)
def error_handler(e):
    return render_template('error.html', problem="Error - Likely a programming error. Please notify the site owner if possible."), e.code

@appObj.errorhandler(403)
def forbidden_handler():
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
    elif request.args.get('region') != "none" and request.args.get('region') not in CONST.REGION_DICT.keys():
        return render_template('error.html')

    #If our name_input parameter has an invalid character in it, we cannot call the API
    elif invalid_character_check():
        return render_template('error.html')

    #If the "Search all regions" option is selected...
    elif request.args.get('region') == "none":
        return search_all_servers( request.args.get('name_input') )

    #If we get here, we must have a region selected and a summoner name containing valid characters
    else:
        return see_summoner( request.args.get('region'), request.args.get('name_input'))


#DATA-PROCESSING FUNCTIONS

#Function to check a URL for empty parameters
def empty_params(param_list):

    for param in param_list:
        if request.args.get(param) == None or not request.args.get(param):
            return True
    return False

#Function to seek out invalid characters in the summoner's name
def invalid_character_check():

    #Spaces, \w (Unicode letters including numbers and underscore), and period (.) are allowed
    regex_string = r'^[ \w\.]+$'

    #If re.search returns None, we didn't find an acceptable name
    return re.search(regex_string, request.args.get('name_input'), flags=re.IGNORECASE) == None



#Function invokes Player class to gather necessary information about the player
def see_summoner(region_info, summoner_name):

    player = Player(region_info, summoner_name)

    if player.exists:
        return render_template('summoner.html', player=player, VERSION=CONST.VERSION_NUM)
    else:
        if player.error == 403:
            return forbidden_handler()
    
    return render_template('error.html', problem='Summoner by that name does not exist on that server, please try a different name or server')


#League of Legends is an international game - players are separated by regions, so they have relatively close servers to communicate with for low-latency gameplay
#This function searches all of Riot's servers across the globe for summoners who match a particular name
def search_all_servers(summoner_name):

    #We'll populate this list with Player objects representing players that exist in different servers
    players = []

    #Threads will be used to check each server so the search time is reasonable (not using threads means a search takes ~20 seconds)
    threads = [None] * len(CONST.REGION_DICT)
    q = Queue() #The queue is to have a thread-independent collection for results

    #Create and start each thread, using the function "region_check" to search an individual server for a summoner
    for region in CONST.REGION_DICT.keys():
        current_index = threads.index(None)
        threads[current_index] = Thread(target=region_check, args=(q, region, summoner_name))
        threads[current_index].start()

    #Join all threads before proceeding
    for i in range(len(threads)):
        threads[i].join()

    #Empty the queue (full of valid summoner information from different servers) into our empty list 
    while not q.empty():
        player = q.get()
        if player == 403: #If 403 is in the queue, something is wrong and we need to return an error stating such
            return forbidden_handler(403)
        players.append( player )

    #Render the webpage, but sort results based on alphabetical order of the region name 
    #(Otherwise the displayed order of results is based on which thread finishes first, which is incconsistent)
    return render_template('search.html', player_list=sorted(players, key=lambda x: x.region_name), VERSION=CONST.VERSION_NUM)


#Our thread function - This function will try to construct a Player using the region passed to it. If it exists, it's added to the queue.
def region_check(queue_obj, region_code, summoner_name):

    player = Player(region_code, summoner_name)

    if player.exists:
        queue_obj.put(player)
    elif player.error == 403: #This 403 gets handled back in the search_all_servers function
        queue_obj.put(403)



if __name__ == "__main__":
    appObj.run(debug=True)