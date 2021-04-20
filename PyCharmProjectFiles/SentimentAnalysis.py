import tweepy
import csv
import math
import pandas
import string
import re
import nltk
import datetime as dt
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from statistics import mean
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

consumer_key = 'ilCWWG0qsksVOXAfdciosm5zG'
consumer_secret = 'EUQpqLRVo11NmVsZwloZu7UcVRvCd13KnwmA5lhyVgKzR6C7pH'
access_token = '1336806106916679683-X8bNJoBcxjFJpWv2r5rnlAdSUdC2kb'
access_token_secret = 'bV4IUcoREWwcCTbtOft3eac9af5gvzyAEHp9UlitCbU73'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# bitcoin_tweets = api.search("bitcoin", count=10)
# for tweet in bitcoin_tweets:
# print(tweet.text)
# Creating a textblob object and assigning the sentiment property
# analysis = TextBlob(tweet.text).sentiment
# print(analysis)

def getSentimentData():
    # Csv file handling
    csvfile = open('my_scraped_tweets.csv', 'w', encoding="utf-8")
    csvwriter = csv.writer(csvfile)

    # csvwriter.writerow(["index", "created_at", "favourite_count", "retweet_count", "text", "user_follower_count"])

    tweets = api.search(q="#ETH", result_type='popular', count=500)
    index = 0
    for tweet in tweets:
        print(tweet.created_at)
        csvwriter.writerow([index, tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.text,
                            tweet.user.followers_count])
        print(tweet.text)
        index += 1;

        # Creating a textblob object and assigning the sentiment property
        # analysis = TextBlob(tweet.text).sentiment
        # print(analysis)


def remove_punctuation(text):
    text = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text


# Perform tokenization: Converting a sentence into a list of words
def tokenization(text):
    text = re.split('\W+', text)
    return text


# Removes stopwords from text, e.g 'woman', 'man', 'girl','boy','one'
def remove_stopwords(text):
    stopwords = nltk.corpus.stopwords.words('english')
    text = [word for word in text if word not in stopwords]
    return text


def perform_stemming_and_lammitization(text):
    # Stemming:
    ps = nltk.PorterStemmer()  # remove suffixs from end of word (e. running -> run)
    text = [ps.stem(word) for word in text]

    # Lemmatizer
    wnl = nltk.WordNetLemmatizer()
    text = [wnl.lemmatize(word) for word in text]
    return text


def clean_text(text):
    print(text)
    text = text.lower()  # first lets make the text lowercase
    print(text)
    text = remove_punctuation(text)
    print(text)
    text = tokenization(text)
    print(text)
    text = remove_stopwords(text)
    print(text)
    text = perform_stemming_and_lammitization(text)
    print(text)
    return text


def get_extra_datetime(last_datetime_str):
    hours = 1
    hours_added = dt.timedelta(hours=hours)
    extra_datetime = dt.datetime.strptime(last_datetime_str, '%Y-%m-%d %H:%M:%S') + hours_added
    return str(extra_datetime)


def append_sentiment_to_training_data():
    # Extract the datetime data points from our csv
    colnames = ['datetime', 'close', 'avg_twitter_sentiment']
    csv_data = pandas.read_csv('MachineLearning/MyDatasets/ML_training_data_ETH.csv')
    datetime_data = csv_data.datetime.to_list()

    # We need to add an extra datetime so we have the hour interval for the last row in our database
    last_datetime = datetime_data[-1]   # this gets the last (datetime)item in the list
    extra_datetime = get_extra_datetime(last_datetime)
    datetime_data.append(extra_datetime)

    sentiment_analyzer = SentimentIntensityAnalyzer()
    print(len(datetime_data))  # this just so ya know where to start from baii
    # Loop each datetime, acquire relevant tweets posted in the hour interval, calc avg sentiment and update the training data csv
    for i in range(360, len(datetime_data) - 1):
        row = csv_data.loc[csv_data['datetime'] == datetime_data[i]]
        if not math.isnan(row['avg_twitter_sentiment']):
            continue
        # Acquire the tweets posted between 2 data points
        all_tweet_data = api.search(q="ETH", start_time=datetime_data[i], end_time=datetime_data[i + 1],
                                    result_type='mixed', count=300, lang='en',
                                    tweet_mode='extended')  # tweet_mode='extended' is to have the full text. (without this the text is truncated to 140 characters)
        # result_type='mixed' is to include both popular and real time results in the response

        # Extract only text data, as this is all we want
        tweets_text_data = []
        for tweet in all_tweet_data:
            tweets_text_data.append(tweet.full_text)

        # Preprocessing & cleaning of textual data:
        cleaned_tweets = []
        for tweet in tweets_text_data:
            cleaned_tweet = clean_text(tweet)
            cleaned_tweets.append(cleaned_tweet)

        # Perform Sentiment Analysis on textual data
        sentiment_values = []
        for tweet in cleaned_tweets:
            tweet_string = " "
            tweet_string = tweet_string.join(tweet)  # turn our cleaned data back into a string, as nltk sentiment input needs to be a sting

            sentiment_values.append(sentiment_analyzer.polarity_scores(tweet_string)["compound"])
            print(sentiment_values)
            # sentiment_values.append(TextBlob(tweet).sentiment)

        average_sentiment = mean(sentiment_values)
        # Append the average sentiment for this time to the csv training data
        csv_data.loc[csv_data["datetime"] == datetime_data[i], "avg_twitter_sentiment"] = average_sentiment
        # the above code: finds any row with datatime == dt[i] and sets the col avg_t_sent to avg_sent

        csv_data.to_csv('MachineLearning/MyDatasets/ML_training_data_ETH.csv', index=False)


append_sentiment_to_training_data()
