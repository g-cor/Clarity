# Clarity

The web app that helps you decide who you want to play!


## Table of Contents

1. Introduction
2. Relevant Terminology
3. Why this application was built
4. How to access the application
5. How to use the application
6. Installing files locally


## Introduction

Clarity is a web application for League of Legends players that is powered using
the Python language and the Flask web framework. "Clarity" is also the name of an
old spell in League of Legends. The word "Clarity" can be defined as
"transparency", which is what this application provides.

This README explains in further depth what the application accomplishes, provides
an example of how the application would be used, and installation instructions in
case someone would like to run the program on their private machine.


## Relevant Terminology

**League of Legends** - The name of the popular online game that this app is built around

**Riot Games (or "Riot")** - The name of the company that developed, and continues to
develop/support the game.

**Summoner** - This is synonymous with "player". A long time ago, Riot used the word
"summoner" to refer to entities that could control champions. You, as a player, were
also a summoner.

**Champion** - The character that a player/summoner will be using for the duration of a
match, which generally spans 15-30 minutes. League of Legends has approximately
140+ champions available to play.

**Hextech Chest** - A type of reward that a player can earn by performing well on a
champion. A player has the ability to earn one chest per week, and can only use
a particular champion for earning that chest once per year. So as an example, if I earn
a chest using Alistar this week, I will not be able to use Alistar to earn another
chest until next year. But I will be able to use a different champion to earn another
chest next week.

**Champion Mastery** - This is a system in the game to help reflect a player's experience
and/or expertise using a champion. There are cosmetic rewards players can earn as
they progress in champion mastery levels.


## Why the application was built

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


## How to access the application

Visit https://gcor.io/league


## How to use the application

All you really need to use the application is to know a player's summoner name. This is
the player's name that is displayed during a match. If you happen to know the server or
region that the player belongs to, that will expedite your usage of the application.

The application was built to be straight-forward, but here's some diagrams to walk
one through the application anyway.

- When you first arrive at the application, it'll look like the picture below:

![Application Homepage](https://gcor.io/images/step1.png)

- For this demo, I'm supplying my summoner name. Please notice I'm not selecting a region for this lookup request.

![Entering a summoner name](https://gcor.io/images/step2.png)

- If you don't select a region, you'll have a screen like this. Since you should have an idea of the person you're
searching for, you should be able to identify who the correct player is based on the information provided. If you
**did** select a region, skip this picture entirely.

![Results from searching all servers](https://gcor.io/images/step3.png)

- Once you've found the player from the correct server, you'll have a screen with some basic information about the
player like so:

![Basic summoner information](https://gcor.io/images/step4.png)

- Clicking the "Available Hextech Chests" button will provide information like the picture below:

![Champions that I can earn a hextech chest with are listed](https://gcor.io/images/step5.png)

- Clicking the "Mastery Progress" button will provide information about my mastery with every champion in the game,
separated by the mastery level each character is at.

![My champion mastery progress is listed by mastery level, from 7 to 0](https://gcor.io/images/step6.png)


## Installing files locally

This section is provided on the off-chance that you'd like to run this on your private machine. One important point of note is that this section will not be perfect. I did the initial development environment setup
a while ago, and don't recall every step I took. But I did what I could to re-trace my steps with Flask and the Riot API and outline that process as I best remember it.

1. Download or clone the repo using the big green button on the right side of the top of this page.

2. [Download and install Python, if you don't have it yet.](https://www.python.org/downloads/) You might run into problems if you try using a version older than 3.7.

3. Set up and activate a virtual environment as described in [this Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/installation/#installation)

4. Once you've done that, you can install the necessary libraries for the application to work.
Those libraries and their installation commands are:
   - Flask (pip install Flask) -- You might've already done this in step 3
   - requests (pip install requests)

5. You will need a valid API key in order to run the code. The steps to get one are as follows:

   - Go to [Riot's Developer Portal](https://developer.riotgames.com/)

   - **If you play League of Legends**, you will use your normal account to generate an API key. There's
a login button in the corner you can use to sign in.

   -  **If you do not play League of Legends**, you will need to sign up for an account to be able to
access the developer portal. Sign up is fairly straightforward, you only need an email address.

   - Once you've accessed the developer portal, you can very quickly see a "development API key"
a little ways down the screen. If it is an expired key, you can 'regenerate' a new API key at
the bottom of the page.

   ![API Key Location](https://gcor.io/images/API_KEY_loc.png)

   - Copy and paste the development API key to the "API_KEY" variable within constants.py (located around line 10). It should
   go from..
   ```python
   API_KEY = "PRIVATE - This must be kept private so people cannot impersonate me to access Riot's API"
   ```
   to something like..
   ```python
   API_KEY = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   ```
   - Save the modifications. Please note that your development API key expires every 24 hours.

6. You should be all set up now! Within your terminal, you should be able to run "py app.py",
which will start the application locally and allow you to visit http://127.0.0.1:5000/
