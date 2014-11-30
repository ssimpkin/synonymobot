#!/usr/bin/env python
#-*- coding: utf-8 -*-

# special thanks to:
# http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/
# http://stackoverflow.com/questions/18314749/setup-for-python-tweepy

# ssimpkin's first twitter bot, requires wordnik and tweepy

import tweepy 
from wordnik import *

# From Twitter:
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# From Wordnik:
apiUrl = 'http://api.wordnik.com/v4'
apiKey = ''
client = swagger.ApiClient(apiKey, apiUrl)

# Listen for tweets
class TweetListener(tweepy.StreamListener):
    def on_status(self, status):
        tweeted_words = status.text
        print 'Tweeted phrase: ' + tweeted_words

        # Isolate term to look up
        tweeted_word = tweeted_words.split(" ")
        print 'Word to look up is: ' + tweeted_word[1]

        # Retrieve synonyms from Wordnik:
        search_word = tweeted_word[1]
        wordApi = WordApi.WordApi(client)
        synonym = wordApi.getRelatedWords(search_word, relationshipTypes='synonym', limitPerRelationshipType=3)
        print synonym[0].words
        api.update_status('@' + status.user.screen_name + ' synonyms for ' + search_word + ': ' + ', '.join(synonym[0].words), in_reply_to_status_id = status.id)
        return True
    
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timed out'
        return True

# Filter incoming tweets to @-mentions
if __name__ == '__main__':
    print 'Showing all tweets to @synonymobot'
    stream = tweepy.streaming.Stream(auth, TweetListener())
    stream.filter(track=['@YOUR_USER_NAME'])




