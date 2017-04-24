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
##to deal with emojies and other non-English languages

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

CACHE_FNAME = "206_final_project_cache.json"
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
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		public_tweets = api.get_user(id=username)
		CACHE_DICTION[twitter_phrase] = public_tweets
		response_text = public_tweets

		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	# 	# for tweet in response_text:
	# 		tweets.append(tweet)
	# return tweets
	return response_text

# print(get_user_tweets("nerdofinfo"))

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
		self.tweet_list = tweet_list
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
		m = zip(self.id, self.text, self.user, self.search, self.favorites, self.retweets)
		w = list(m)
		return w

	def user_mentions(self):
		user_ids = []
		for tweet in self.tweet_list:
			for user in tweet["entities"]["user_mentions"]:
				user_ids.append(user["screen_name"])
		return user_ids



# ## Define a class "Tweet_User" which should accept [INSERT] and generate a tule for later use in the Users database

class Tweet_User(object):
	def __init__(self, user_tweets):
		self.user_tweets = user_tweets

		self.user_id = self.user_tweets["id"]
		self.screen_name = self.user_tweets["screen_name"]
		self.num_favs = self.user_tweets["favourites_count"]

	def user_tups(self):
		total_tweet = (self.user_id, self.screen_name, self.num_favs)
		return total_tweet





## Make a list of tweet dictionaries using the get_tweets function and assign it to a unique variable


tweet_dictionaries = []
for movie in movie_titles:
	tweet_dictionaries.append(get_tweets(movie))


## Create a list of instances of the Tweet class for each of the dictionaries in the tweet_dictionaries list

tweet_instances=[]
for diction in tweet_dictionaries:
	tweet_instances.append(Tweet(tweet_list=diction, movie_titles = movie_titles))




## Create a list of tweet dictionaries of the of the get_user_tweets() function for the users mentioned in the tweets in the Tweets class

user_dictionaries = []
for inst in tweet_instances:
	for user in inst.user_mentions():
		user_dictionaries.append(get_user_tweets(user))

## Create a list of tweet dictionaries of the get_user_tweets function for the users who posted tweets in the Tweets class

user_dictionaries2 = []
for inst in tweet_instances:
	for name in inst.user:
		user_dictionaries2.append(get_user_tweets(name))

## Create a list of instances of the User class for each of the dicitonaries

user_instances = []
for diction in user_dictionaries:
	user_instances.append(Tweet_User(user_tweets = diction))

for diction in user_dictionaries2:
	user_instances.append(Tweet_User(user_tweets = diction))


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

tweet_statement = "INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)"

for inst in tweet_instances:
	for tup in inst.zip_lists():
		cur.execute(tweet_statement, tup)
conn.commit()



## Begin setup for Users database
cur.execute("DROP TABLE IF EXISTS Users")
table_spec3 = "CREATE TABLE IF NOT EXISTS Users (user_ID INTEGER PRIMARY KEY, screen_name TEXT, num_favorites_all INTEGER)"
cur.execute(table_spec3)

## Write code to insert user data into User database

user_statement = "INSERT or IGNORE INTO Users VALUES (?,?,?)"

for inst in user_instances:
	cur.execute(user_statement, inst.user_tups())

conn.commit()


## Begin processing the data from the database:
	## 1. Make queries to the database to grab intersections of data, and then use at least four of the processing mechanisms (INNER JOIN needs to be used between the databases -- SEE INSTRUCTIONS)
		## - Possibly use list comprehensions
		## - Look up different things you can do with the collections library!
	## 2. Write that data to a text file -- a sort of "summary stats" page with a clear title
		## - Focus on tweet stats since that's what I want my CSV file to be based on.
		## - <List your 3 movie titles> + Twitter summary, <current date>
				## - Tweet summary = Num of tweets, num of retweets, num of faves, length of tweets (?), etc.
	## 3. Make a CSV file? Analyse data to see which of the 3 movies are most popular on Twitter, and make pie charts comparing the three!



two = "SELECT *FROM Tweets WHERE num_retweets>5"
cur.execute(two)
more_than_5_rts = cur.fetchall()

# print(more_than_5_rts)

f = "SELECT tweet_text FROM Tweets INNER JOIN Movies where IMDB_rating>5"
g = cur.execute(f)
joined_result = g.fetchall()

# print(joined_result)

w = "SELECT *FROM Users WHERE num_favorites_all >5"
cur.execute(w)
more_than_5_favs = cur.fetchall()

# print(more_than_5_favs)

y = "SELECT screen_name FROM Users INNER JOIN Movies where IMDB_rating>5"
r = cur.execute(y)
screen_names = [x[0] for x in r.fetchall()]

# print(screen_names)

m = "SELECT *FROM Movies WHERE IMDB_rating>5"
a = cur.execute(m)
joined_results = a.fetchall()

# print(joined_results)

d = "SELECT director FROM Movies WHERE IMDB_rating>5"
h = cur.execute(d)
results = h.fetchall()

# print(results)
















# # ##---------- TEST CASES ----------
# class CachingTests(unittest.TestCase):
# 	def test_caching(self):
# 		cache = open("finalproject.json","r")
# 		s = cache.read()
# 		cache.close()
# 		self.assertTrue("Rogue One" in s, 'test to see that one of the movies titles I choose is in the cache')

# 	def test_caching_type(self):
# 		self.assertEqual(type(CACHE_DICTION), type({}))


# class MovieTests(unittest.TestCase):
# 	def test_movie1(self):
# 		m = Movie()
# 		self.assertEqual(type(m.title), type(""), 'Checking to make sure that the instance variable .title is a string')

# 	def test_movie2(self):
# 		m = Movie()
# 		self.assertEqual(type(m.rating), type(""), 'testing that the imdb_rating instance variable is a string')
# 	def test_movie3(self):
# 		m = Movie()
# 		self.assertEqual(type(m.tuple_generate()), type(()), 'Testing that tuple_generate method is a tuple')

# class TweetTests(unittest.TestCase):
# 	def test_tweet1(self):
# 		t = Tweet()
# 		self.assertEqual(type(t.retweets[0]), type(int()), "testing that the retweets instance variable is a string type")

# ##~~~~~~~~ Confused about how to write database tests????? ~~~~~~~~
# class DatabaseTests(unittest.TestCase):
# 	def test_db1(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Users');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)==3,"Testing that there are 3 columns in the Users database")
# 		conn.close()
# 	def test_db2(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Tweets');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)==6,"Testing that there are 6 columns in the Tweets database")
# 		conn.close()
# 	def test_db3(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Movies');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)==6,"Testing that there are 6 columns in the Movies database")
# 		conn.close()






# if __name__ == "__main__":
# 	unittest.main(verbosity=2)