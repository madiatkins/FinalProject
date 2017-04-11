import tweepy
import twitter_info
import unittest
import json
import sqlite3
import re
import collections
import itertools

import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer) ##to deal with emojies and other languages



CACHE_FNAME = "finalproject.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# Define your function get_user_tweets here:

def get_user_tweets(username):
	twitter_name = "twitter_"+str(username)
	tweets = []

	if twitter_name in CACHE_DICTION:
		print('using cache')
		response_text = CACHE_DICTION[twitter_name]
		for tweet in response_text[:21]:
			tweets.append(tweet)
	else:
		print('fetching')
		public_tweets = api.user_timeline(id=username)
		CACHE_DICTION[twitter_name] = public_tweets
		response_text = public_tweets

		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

		for tweet in response_text:
			tweets.append(tweet)

	return tweets


def get_tweets(phrase):
	tweets = []
	twitter_phrase = "twitter_"+str(phrase)

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


	for tweet in response_text:
		tweets.append(tweet)


























































##---------- TEST CASES ----------
class CachingTests(unittest.TestCase):
	def test_caching(self):
		cache = open("finalproject.json","r").read()
		self.assertTrue("Twilight" in cache, 'test to see that one of the movies titles I choose is in the cache')
	def test_caching_type(self):
		cache = open("finalproject.json", "r").read()
		self.assertEqual(type(cache), type({}))

class MovieTests(unittest.TestCase):
	def test_movie1(self):
		m = Movie()
		self.assertEqual(type(m.title), type(""), 'Checking to make sure that the instance variable .title is a string')

	def test_movie2(self):
		m = Movie()
		self.assertEqual(type(m.imdb_rating), type(1), 'testing that the imdb_rating instance variable is an integer')

class TweetTests(unittest.TestCase):
	def test_tweet1(self):
		t = Tweet()
		self.assertEqual(type(t.unique), type(""), "testing that the unique instance variable is a string type")

class DatabaseTests(unittest.TestCase):
	def test_db1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==3,"Testing that there are 3 columns in the Users database")
		conn.close()
	def test_db2(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Users database")
		conn.close()
	def test_db3(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Users database")
		conn.close()






if __name__ == "__main__":
	unittest.main(verbosity=2)