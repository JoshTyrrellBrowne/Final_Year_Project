import tweepy

import pandas as pd
import csv
import re
import string
import preprocessor as p

consumer_key = 'ilCWWG0qsksVOXAfdciosm5zG'
consumer_secret = 'EUQpqLRVo11NmVsZwloZu7UcVRvCd13KnwmA5lhyVgKzR6C7pH'
access_key = '1336806106916679683-X8bNJoBcxjFJpWv2r5rnlAdSUdC2kb'
access_secret = 'bV4IUcoREWwcCTbtOft3eac9af5gvzyAEHp9UlitCbU73'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

csvFile = open('file-name', 'a')
csvWriter = csv.writer(csvFile)

search_words = "corona virus"  # enter your words
new_search = search_words + " -filter:retweets"

for tweet in tweepy.Cursor(api.search, q=new_search, count=2,
                           lang="en",
                           since_id=0).items():
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet.user.screen_name.encode('utf-8'),
                        tweet.user.location.encode('utf-8')])
