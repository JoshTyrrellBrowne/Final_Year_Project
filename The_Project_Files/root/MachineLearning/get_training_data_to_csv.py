import tweepy
import csv
from textblob import TextBlob

consumer_key = 'ilCWWG0qsksVOXAfdciosm5zG'
consumer_secret = 'EUQpqLRVo11NmVsZwloZu7UcVRvCd13KnwmA5lhyVgKzR6C7pH'
access_token= '1336806106916679683-X8bNJoBcxjFJpWv2r5rnlAdSUdC2kb'
access_token_secret = 'bV4IUcoREWwcCTbtOft3eac9af5gvzyAEHp9UlitCbU73'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Csv file handling
csv_file = open('my_scraped_tweets.csv', 'w', encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["index", "created_at", "favourite_count", "retweet_count", "text", "user_follower_count"])

def getSentimentData():
    tweets = api.search(q="#ETH", result_type='popular', count=500)
    index = 0
    for tweet in tweets:
        print(tweet.created_at)
        csv_writer.writerow([index, tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.text,
                             tweet.user.followers_count])
        print(tweet.text)
        index += 1;

        # Creating a textblob object and assigning the sentiment property
        #analysis = TextBlob(tweet.text).sentiment
        #print(analysis)


getSentimentData()