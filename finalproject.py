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



class Movie(object):
	def __init__(self, movie_diction):
		self.id = movie_diction["imdbID"]
		self.title = movie_diction["Title"]
		self.director = movie_diction["Director"]
		self.rating = movie_diction["imdbRating"]
		self.actors = movie_diction["Actors"] 
		self.languages = movie_diction["Language"] 

	def lst_actors(self):
		return self.actors.split(",")
	def num_languages(self):
		return len(self.languages.split(","))
	def num_one_actor(self):
		return self.lst_actors()[0]

	def tuple_generate(self): ##Remember the order used here, make sure it's correct with what the database table row order is
		tup = (self.id, self.title, self.director, self.rating, self.num_one_actor(), self.num_languages())
		return tup


## Define a class called "Tweet" which should accept a list of tweet dictionaries and a string represented as the movie title of the tweet list. It should generate a tuple for later use in the Tweets database

class Tweet(object):
	
	def __init__(self, tweet_list, movie_titles):
		self.search = []
		self.text = []
		self.id = []
		self.user = []
		self.favorites = []
		self.retweets = []
		for tweet in tweet_list:
			for movie in movie_titles:
				if movie in tweet["text"]:
					self.search.append(movie)
			self.text.append(tweet["text"])
			self.id.append(tweet["id"])
			self.user.append(tweet["user"]["screen_name"])
			self.favorites.append(tweet["favorite_count"])
			self.retweets.append(tweet["retweet_count"])

	def zip_lists(self):
		m = zip(self.search, self.text, self.id, self.user, self.favorites, self.retweets)
		w = list(m)
		return w



# testing = get_tweets("Hidden Figures")
# test = Tweet(tweet_list = testing, movie_title = "Hidden Figures")
# print(test.zip_lists())



## Define a class "Tweet_User" which should accept [INSERT] and generate a tule for later use in the Users database

class Tweet_User(object):
	def __init__(self, user_diction):
		pass
##~~~~~~ I am still very confused as to what the project instructions are calling for when they get data on all the users in the neighborhod of a tweet. So which tweets should I be getting these users from? The get_tweets() function? Then grabbing the users from that and inputting those into the get_user_tweets() function? Thanks!! ~~~~~~~~~~




## Make a list of tweet dictionaries using the get_tweets function and assign it to a unique variable


tweet_dictionaries = []
for movie in movie_titles:
	tweet_dictionaries.append(get_tweets(movie))


## Create a list of instances of the Tweet class for each of the dictionaries in the tweet_dictionaries list

tweet_instances=[]
for diction in tweet_dictionaries:
	tweet_instances.append(Tweet(tweet_list=diction, movie_titles = movie_titles))

# for inst in tweet_instances:
# 	m = inst.zip_lists()
# 	print(m)
## Write an invocation to the function for a user timeline and save the result in a unique variable:

user_tweets_dictionaries = []

##~~~~~~~ Need help with understanding what is needs of Tweet_User class first ~~~~~~~~~~~~

## Create a list of instances of the Tweet_User class for each of the dictionaries in the tuser_tweets_dictionaries list

user_instances = []

##~~~~~~~ Need help with understanding what is needs of Tweet_User class first ~~~~~~~~~~~~

## Create a list of dictionaries calling on the OMDB function for each of the movie titles in the movie_titles list

movie_dictionaries = []

for item in movie_titles:
	movie_dictionaries.append(get_OMDBdata(item))

## Create a list of instances of the Movie class for each of the dictionaries in the movie_dictionaries list

movie_instances = []

for diction in movie_dictionaries:
	movie_instances.append(Movie(diction))




## Begin setup for Movie database

conn = sqlite3.connect("finalproject.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Movies")
table_spec1 = "CREATE TABLE IF NOT EXISTS Movies (movie_ID TEXT PRIMARY KEY, title TEXT, director TEXT, IMDB_rating TEXT, top_actor TEXT, num_of_languages INTEGER)"
cur.execute(table_spec1)

## Write code to insert Movie data into Movie database from the instances list

mov_statement = "INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)"

for inst in movie_instances:
	cur.execute(mov_statement, inst.tuple_generate())

conn.commit()

## Begin setup for Tweets database

cur.execute("DROP TABLE IF EXISTS Tweets")
table_spec2 = "CREATE TABLE IF NOT EXISTS Tweets (tweet_ID INTEGER PRIMARY KEY, tweet_text TEXT, user TEXT, movie_search TEXT, num_favorites INTEGER, num_retweets INTEGER)"
cur.execute(table_spec2)


## Write code to insert tweet data into Tweets database





## Begin setup for Users database
cur.execute("DROP TABLE IF EXISTS Users")
table_spec3 = "CREATE TABLE IF NOT EXISTS Users (user_ID INTEGER PRIMARY KEY, screen_name TEXT, num_favorites_all INTEGER)"
cur.execute(table_spec3)

## Write code to insert user data into User database

##~~~~~~~~ Again, ignore all this code. I need to understand Tweet_User class before I can do anything more with Users database ~~~~~~~~~~~~

# user_statement = "INSERT or IGNORE INTO Users VALUES (?,?,?,?)"

# user_ids = []
# for tweet in umich_tweets:
#     for user in tweet["entities"]["user_mentions"]:
#         user_ids.append(user["screen_name"])

# user_ids.insert(0, '@umich')

# for user in user_ids:
# 	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
#     user = api.get_user(user)
#     user_id = user["id"]
#     screen_name = user["screen_name"]
#     num_favs = user["favourites_count"]

#     total_tweet = (user_id, screen_name, num_favs)

#     cur.execute(user_statement, total_tweet)

## Begin processing the data from the database:
	## 1. Make queries to the database to grab intersections of data, and then use at least four of the processing mechanisms (INNER JOIN needs to be used between the databases -- SEE INSTRUCTIONS)
		## - Possibly use list comprehensions
		## - Look up different things you can do with the collections library!
	## 2. Write that data to a text file -- a sort of "summary stats" page with a clear title
		## - Focus on tweet stats since that's what I want my CSV file to be based on.
		## - <List your 3 movie titles> + Twitter summary, <current date>
				## - Tweet summary = Num of tweets, num of retweets, num of faves, length of tweets (?), etc.
	## 3. Make a CSV file? Analyse data to see which of the 3 movies are most popular on Twitter, and make pie charts comparing the three!


##~~~~~~ I will work on the queries and output stuff at a later time ~~~~~~~~



























# ##---------- TEST CASES ----------
# class CachingTests(unittest.TestCase):
# 	def test_caching(self):
# 		cache = open("finalproject.json","r")
# 		s = cache.read()
# 		cache.close()
# 		self.assertTrue("Twilight" in s, 'test to see that one of the movies titles I choose is in the cache')

# 	def test_caching_type(self):
# 		self.assertEqual(type(CACHE_DICTION), type({}))


# class MovieTests(unittest.TestCase):
# 	def test_movie1(self):
# 		m = Movie()
# 		self.assertEqual(type(m.title), type(""), 'Checking to make sure that the instance variable .title is a string')

# 	def test_movie2(self):
# 		m = Movie()
# 		self.assertEqual(type(m.imdb_rating), type(1), 'testing that the imdb_rating instance variable is an integer')

# class TweetTests(unittest.TestCase):
# 	def test_tweet1(self):
# 		t = Tweet()
# 		self.assertEqual(type(t.unique), type(""), "testing that the unique instance variable is a string type")

# class DatabaseTests(unittest.TestCase):
# 	def test_db1(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Users');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result[0])==3,"Testing that there are 3 columns in the Users database")
# 		conn.close()
# 	def test_db2(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Tweets');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Users database")
# 		conn.close()
# 	def test_db3(self):
# 		conn = sqlite3.connect('project3_tweets.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Movies');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Users database")
# 		conn.close()






# if __name__ == "__main__":
# 	unittest.main(verbosity=2)