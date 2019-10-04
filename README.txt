Clarity

The web app that makes your options clearer!

----------

Table of Contents

0. Introduction
I. Relevant Terminology
II. Why this application was built
III. How to access the application
IV. How to use the application
V. Installing files locally

----------

INTRODUCTION

Clarity is a web application for League of Legends players that is powered using
the Python language and the Flask web framework. "Clarity" is also the name of an
old spell in League of Legends. The word "Clarity" can be defined as
"transparency", which is what this application provides.

This README explains in further depth what the application accomplishes, provides
an example of how the application would be used, and installation instructions in
case someone would like to run the program on their private machine.

----------

RELEVANT TERMINOLOGY

League of Legends - The name of the popular online game that this app is built around

Riot Games (or "Riot") - The name of the company that developed, and continues to
develop/support the game.

Summoner - This is synonymous with "player". A long time ago, Riot used the word
"summoner" to refer to entities that could control champions. You, as a player, were
also a summoner.

Champion - The character that a player/summoner will be using for the duration of a
match, which generally spans 15-30 minutes. League of Legends has approximately
140+ champions available to play.

Hextech Chest - A type of reward that a player can earn by performing well on a
champion. A player has the ability to earn one chest per week, and can only use
a particular champion for earning that chest once per year. So as an example, if I earn
a chest using Alistar this week, I will not be able to use Alistar to earn another
chest until next year. But I will be able to use a different champion to earn another
chest next week.

Champion Mastery - This is a system in the game to help reflect a player's experience
and/or expertise using a champion. There are cosmetic rewards players can earn as
they progress in champion mastery levels.

----------

WHY THE APPLICATION WAS BUILT

If you want to know more about League of Legends, Google is your friend. All you need
to know about the game is that before starting any match, you will choose a character
to play as. In the game, this is referred to as your "champion".

Players have plenty of reasons to choose a specific champion. Two reasons that I've
encountered in recent years are "I want to try and earn a hextech chest," and "I want
to earn more champion mastery levels." But those particular reward and progression
systems are specific to each individual player's account. For example, I might be able
to earn a hextech chest by playing Master Yi, but many other players aren't able to
right now. The real problem is that the information I need to answer those questions
is not available during the champion selection process. So I have to memorize it, or
write it down somewhere and refer to it during champion selection.

But the good news is that Riot, the company who develops League of Legends, have set
up an API that provides that information, and more. My application makes use of that
API and presents the information for a particular player in an easily digestible fashion.

----------

HOW TO ACCESS THE APPLICATION

Visit https://gcor.io/league

----------

HOW TO USE THE APPLICATION

All you really need to use the application is to know a player's summoner name. This is
the player's name that is displayed during a match. If you happen to know the server or
region that the player belongs to, that will expedite your usage of the application.

The application was built to be straight-forward, but here's some diagrams to walk
one through the application anyway.

[Base diagram]

[Diagram of search functionality]

[Diagram of summoner return]

[Diagram of expanded hex chest availability (or gif?)]

[Diagram of expanded champion mastery info (or gif?)]

----------

INSTALLING FILES LOCALLY

This section will not be perfect, because I did the initial development environment setup
a while ago, and don't exactly recall all the steps I took.

1. Install python in whatever environment you need to use. If you have to choose between
python 2 and python 3, choose 3.

2. Set up and activate a virtual environment as described in:
https://flask.palletsprojects.com/en/1.1.x/installation/#installation

3. Once you've done that, you can install the necessary libraries for the application to work.
Those libraries and their installation commands are:
~ Flask (pip install Flask) -- You might've already done this in step 2
~ requests (pip install requests)

4. You will need a valid API key in order to run the code. The API key will need to be inserted
into app.py at line 11 in place of the entire "PRIVATE - This must be..." message. So, you'll
leave the quotations alone and just replace the message within the quotes with the API key. The
next few steps will explain how to get an API key.

a. First, you can go to Riot's Developer Portal at https://developer.riotgames.com/

b. If you play League of Legends, you will use your normal account to generate an API key. There's
a login button in the corner you can use to sign in.

   If you do not play League of Legends, you will need to sign up for an account to be able to
access the developer portal. Sign up is fairly straightforward, you only need an email address.

c. Once you've accessed the developer portal, you can very quickly see a "development API key"
a little ways down the screen. If it is an expired key, you can 'regenerate' a new API key at
the bottom of the page.

d. Copy and paste the development API key to that "API_KEY" variable I pointed out at the
beginning of step 4. Keep the quotation marks, only change the message within the quotation.
Save the modification. (Please note that your development API key expires every 24 hours)

5. You should be all set up now! Within your terminal, you should be able to run "py app.py",
which will start the application locally and allow you to visit http://127.0.0.1:5000/