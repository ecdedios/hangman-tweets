#hangman-tweets
#hangman.py

import json
import os
import random
import re
import sys
import tweepy


def clear():
	os.system("cls" if os.name == "nt" else "clear")


def get_trends():

	# Tweepy Oauth Implementation

    CONSUMER_KEY = 'xxx'
    CONSUMER_SECRET = 'xxx'
    ACCESS_TOKEN = 'xxx'
    ACCESS_TOKEN_SECRET = 'xxx'
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth)

	# The Yahoo! Where On Earth ID for the entire world is 1.
	# http://developer.yahoo.com/geo/geoplanet/
    # U.S.=23424977 and SATX=2487796
    WOEID = 2487796

    trends = api.trends_place(WOEID)

    trends_set = set(
        [trend['name']
        for trend in trends[0]['trends']]
        )

    trends_list = []

    for item in trends_set:
        trends_list.append(re.sub('[^A-Za-z0-9]+', '', item))

    return trends_list


def draw(misses, hits, word):
    clear()

    print("\nSuccesful Hits: ",end="")
    
    for letter in hits:
        print(letter,end=" ")

    print("\nLetter/Number Strikes: ", end="")

    for letter in misses:
        print(letter, end=" ")
    
    print("\n\n")

    print("Strikes: {}/{}".format(len(misses),MAX_MISSES))

    print("\n")
    
    for letter in word:
        if letter in hits:
            print(letter, end=" ")
        else:
            print("_ ", end=" ")

    print("\n\n")

    
def get_guess(misses, hits):
    while True:
        guess = input("Guess a letter or number: ").upper()
    
        if len(guess) != 1:
            print("You can only guess a single letter or number!")
        elif guess in misses or guess in hits:
            print("You've already guessed that!")
        else:
            return guess


def play(done):
    clear()
    word = random.choice(trends).upper()
    misses = []
    hits = []
    
    while True:
        draw(misses, hits, word)
        guess = get_guess(misses, hits)
        
        if guess in word:
            hits.append(guess)
            found = True
            for letter in word:
                if letter not in hits:
                    found = False
            if found:
                print("\n\nYou win!")
                done = True
        else:
            misses.append(guess)
            if len(misses) == MAX_MISSES:
                draw(misses, hits, word)
                print("\n\nYou lost!")
                print("The secret word was {}".format(word))
                done = True
        
        if done:
            play_again = input("Play again? Y/N ").upper()
            if play_again != "N":
                return play(done=False)
            else:
                sys.exit()


def welcome():
    
    start = input("Press any key to start or Q to quit ").upper()
    if start == "Q":
        print("Good Bye!")
        sys.exit()
    else:
        return True



MAX_MISSES = 10
trends = get_trends()
done = False

while True:
    clear()
    print(trends)
    print("""\n
==================================================
# HANGMAN TWEETS
==================================================

This game is a hangman clone that makes the player
guess one of the trending Twitter topics in San
Antonio.

It's written in python and uses tweepy, "an easy-
to-use Python library for accessing the Twitter
API.

# JUST TINKERING AROUND PYTHON !

""")
    welcome()
    play(done)