from __future__ import division
import operator
import tweepy
import shutil
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import csv 
from textblob import TextBlob
import numpy as np
import os.path

consumer_key = "5Yi6aDwjawLab89gmnEJoB6tG"
consumer_secret = "IRhCyQO7XP4n5P6RNcn2qsEvYC5aL9DSUaEF7RLC1wolRRrTy0"
access_token = "739428501598658561-vOkcOTY1nVeuzOMPxYnyWlIxOoQbafh"
access_token_secret = "vTG2JHnJdUP583AzgzlLGahSFciW6xb9iqu3BbDxnNEwM"

class twitter_analyze:

	def __init__(self):
		pass
	
	def sentiment(self, var):

		if var == 1:
			stock = '$GS'
		elif var == 2:
			stock = '$KO'
		elif var == 3:
			stock = '$DIS'
		elif var == 4:
			stock = '$WMT'
		elif var == 5:
			stock = '$VZ'

		sentiment_list = self.analyze_feelings(stock)
		return max(sentiment_list.iteritems(), key=operator.itemgetter(1))[0]
	
	def analyze_feelings(self, stock):

		tweets = self.analyze_stock(stock)

		sentiment = []
		for index, row in tweets.iterrows():
			value = 0.0
			if isinstance(row['polarity'], float):
				value = round(row['polarity'], 3)
			else:
				x = float(row['polarity'])
				value = round(x, 3)
			if value < 0.0:
				sentiment.append('negative')
			elif value == 0.0:
				sentiment.append('neutral')
			else:
				sentiment.append('positive')

		tweets['sentiment'] = sentiment
		counts_list = {}
		counts_list['positive'] = tweets['sentiment'].value_counts()['positive']
		counts_list['neutral'] = tweets['sentiment'].value_counts()['neutral']
		counts_list['negative'] = tweets['sentiment'].value_counts()['negative']

		return counts_list

	def analyze_stock(self, stock):
		all_tweets = self.get_tweets(stock)
		tweets = pd.DataFrame()
		analysis_list = []
		polarity_list = []
		subjectivity_list = []
		tweet_text = []
		tweet_dates = []
		for tweet in all_tweets:
			tweet_text.append(tweet.text.encode("utf-8"))
			analysis = TextBlob(tweet.text)
			# prints-Sentiment(polarity=0.0, subjectivity=0.0), polarity is how positive or negative, subjectivity is if opinion or fact
			# analysis_list.append('polarity:' + str(analysis.se 1ntiment.polarity) + ' subjectivity:' + str(analysis.sentiment.subjectivity))
			polarity_list.append(str(analysis.sentiment.polarity))
			subjectivity_list.append(str(analysis.sentiment.subjectivity))
			tweet_dates.append(tweet.created_at)

		tweets['text'] = np.array(tweet_text)
		tweets['polarity'] = np.array(polarity_list)
		tweets['subjectivity'] = np.array(subjectivity_list)
		tweets['date'] = np.array(tweet_dates)

		return tweets

	def get_tweets(self, stock):

		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		alltweets = []  
		public_tweets = api.search(stock)
		alltweets.extend(public_tweets)
		oldest = alltweets[-1].id - 1

		while len(public_tweets) > 0:
		    # print "getting tweets before %s" % (oldest)
		    
		    public_tweets = api.search(stock,count=200,max_id=oldest)
		    alltweets.extend(public_tweets)
		    oldest = alltweets[-1].id - 1
		    
		    # print "...%s tweets downloaded so far" % (len(alltweets))

		    if len(alltweets) > 500:
		    	break

		outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in public_tweets]
		# print outtweets
		return alltweets

if __name__ == "__main__":

	# analyze = twitter_analyze()
	# var = 2 
	# print analyze.sentiment(var)
	

