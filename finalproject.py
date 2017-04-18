import tweepy
import twitter_info
import unittest
import json
import sqlite3
import re
import collections
import itertools
from itertools import chain
import requests
import csv
import webbrowser
from pprint import pprint
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer) 
##to deal with emojies and other languages

##Tweepy setup

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


## Insert 3 movie titles into movie list

movie_titles = ["Hidden Figures", "Rogue One", "Lazer Team"]

## Create initial cache setup

CACHE_FNAME = "finalproject.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
	
except:
	CACHE_DICTION = {}


# Define your function get_user_tweets to fetch and cache tweets based on a Twitter screen name:

def get_user_tweets(username):
	twitter_phrase = "twitter_"+str(username)
	tweets = []

	if twitter_phrase in CACHE_DICTION:
		print('using cache')
		response_text = CACHE_DICTION[twitter_phrase]
		for tweet in response_text:
			tweets.append(tweet)
	else:
		print('fetching')
		public_tweets = api.user_timeline(id=username)
		CACHE_DICTION[twitter_phrase] = public_tweets
		response_text = public_tweets

		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

		for tweet in response_text:
			tweets.append(tweet)
	return tweets

## Define your functino get_tweets to fetch and cache tweets based on a Twitter phrase (in this case, movie titles):

def get_tweets(phrase):
	twitter_phrase = "twitter_"+str(phrase)
	tweets = []

	if twitter_phrase in CACHE_DICTION:
		print('using cache')
		response_text = CACHE_DICTION[twitter_phrase]

	else:
		print('fetching')
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		public_tweets = api.search(q=phrase)
		CACHE_DICTION[twitter_phrase] = public_tweets
		response_text = public_tweets

		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	# return response_text

	tweeter = response_text["statuses"]
	for tweet in tweeter:
		tweets.append(tweet)
	return tweets


## Define your function get_OMDBdata to fetch and cache movie data based on a movie title:


def get_OMDBdata(name):
	baseurl = "http://www.omdbapi.com/?"
	omdb_phrase = "omdbsearch_"+str(name)

	if omdb_phrase in CACHE_DICTION:
		print('using cache')
		response_text = CACHE_DICTION[omdb_phrase]

	else:
		print('fetching')
		omdb = requests.get(baseurl, params = {"t":name, "type":"movie"}).text
		omdb_return = json.loads(omdb)
		CACHE_DICTION[omdb_phrase] = omdb_return
		response_text = omdb_return
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	return response_text



## Define a class called "Movie" which should accept a dictionary that represents movie data from OMDB
##It should have at least 3 instance variables and at least 2 methods besides the constructor



