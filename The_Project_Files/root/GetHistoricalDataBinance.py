
import matplotlib
import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from io import BytesIO
import base64
import csv
from SentimentAnalysis import append_sentiment_to_training_data

# This script is used to retrieve cryptocurrency price data, the get_currency_data_to_csv() function also calls the append_sentiment_to_training_data()
# function which retrieves twitter data and calculates sentiment scores and appends these values to the dataset


def get_binance_bars(symbol, interval, startTime, endTime):
    url = "https://api.binance.com/api/v3/klines"

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'  # max number of data points returned
    req_params = {"symbol": symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime, 'limit': limit}

    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))

    print(df)

    if len(df.index) == 0:
        return None

    df = df.iloc[:, 0:6]  # the df has many columns, this line means we only take the first 6 columns
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]

    return df


#get_binance_bars('ETHUSDT', '1h', dt.datetime(2020, 1, 1), dt.datetime(2020, 2, 1))


def get_eth_usd_graph():
    # Get All the months in datetime for the data request
    months = [dt.datetime(2017, i, 1) for i in range(1, 13)]
    months.extend([dt.datetime(2018, i, 1) for i in range(1, 13)])
    months.extend([dt.datetime(2019, i, 1) for i in range(1, 13)])
    months.extend([dt.datetime(2020, i, 1) for i in range(1, 13)])
    months.extend([dt.datetime(2021, i, 1) for i in range(1, 4)])

    # BELOW: months[i+1] - dt.timedelta(0, 1) is for subtracting 1 second from the date so that it doesnt go outside list
    df_list = [get_binance_bars('ETHUSDT', '1h', months[i], months[i+1] - dt.timedelta(0, 1)) for i in range(0, len(months) - 1)]

    df = pd.concat(df_list)
    print(df.shape)

    df['close'].astype('float').plot()

    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title('ETH/USD Price Chart')

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.savefig('ETHUSDT_LongTerm_PriceGraph.png')
    plt.show()
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url

#get_eth_usd_graph()

SEQ_LENGTH = 120
FUTURE_PERIOD_PREDICT = 24


def set_future_and_target_columns(csv_data_df):
    def classify(current, future):
        if float(future) > float(current):
            return 1
        else:
            return 0

    csv_data_df['future_close'] = csv_data_df['close'].shift(-FUTURE_PERIOD_PREDICT)
    csv_data_df['target'] = list(map(classify, csv_data_df['close'], csv_data_df['future_close']))
    csv_data_df.to_csv('MachineLearning/training_data_ETH.csv')

def get_currency_data_to_csv(currency_pair, crypto_name):
    colnames = ['time_ID', 'datetime', 'close', 'avg_twitter_sentiment', 'future_close', 'target']
    dataset = f'MachineLearning/MyDatasets/ML_testing_data_{currency_pair}.csv'
    csv_data_df = pd.DataFrame(columns=colnames)

    days = [dt.datetime(2021, 5, i) for i in range(1, 5)]
    days.insert(0, dt.datetime(2021, 4, 30))  # we need the day before the beginning for calc future_close & target

    # BELOW: months[i+1] - dt.timedelta(0, 1) is for subtracting 1 second from the date so that it doesnt go outside list
    df_list = [get_binance_bars(currency_pair, '1h', days[i], days[i + 1] - dt.timedelta(0, 1)) for i in
               range(0, len(days) - 1)]

    df = pd.concat(df_list)

    # index in this for loop is actually the date time information
    for index, row in df.iterrows():
        new_row = {'time_ID': row['datetime'], 'datetime': index, 'close': row['close'], 'avg_twitter_sentiment': '',
                   'future_close': '', 'target': ''}
        csv_data_df = csv_data_df.append(new_row, ignore_index=True)

    set_future_and_target_columns(csv_data_df)
    csv_data_df.to_csv(dataset, header=colnames, index=False)  # now write the data to the csv file

    append_sentiment_to_training_data(dataset, crypto_name)
    return df

get_currency_data_to_csv('ADAUSDT', 'ADA')

def get_eth_data_past_seven_days():
    colnames = ['time_ID', 'datetime', 'close', 'avg_twitter_sentiment', 'future_close', 'target']
    dataset = 'MachineLearning/MyDatasets/ML_training_data_ETH.csv'
    csv_data_df = pd.read_csv(dataset)  #pd.DataFrame(columns=colnames)

    days = [dt.datetime(2021, 4, i) for i in range(18, 20)]
    # days.insert(0, dt.datetime(2021, 3, 31))  # we need the day before the beginning for calc future_close & target

    # BELOW: months[i+1] - dt.timedelta(0, 1) is for subtracting 1 second from the date so that it doesnt go outside list
    df_list = [get_binance_bars('ETHUSDT', '1h', days[i], days[i + 1] - dt.timedelta(0, 1)) for i in
               range(0, len(days) - 1)]

    df = pd.concat(df_list)

    count = 0
    # index in this for loop is actually the date time information
    for index, row in df.iterrows():
        new_row = {'time_ID': row['datetime'], 'datetime': index, 'close': row['close'], 'avg_twitter_sentiment': '', 'future_close': '', 'target': ''}
        csv_data_df = csv_data_df.append(new_row, ignore_index=True)

    set_future_and_target_columns(csv_data_df)
    csv_data_df.to_csv(dataset, header=colnames, index=False)  # now write the data to the csv file

    return df


#get_eth_data_past_seven_days()


# This function was created for merging sentiment data from one csv to another
def csv_data_binding():
    df_nonSentiment = pd.read_csv('MachineLearning/training_data_ETH.csv')
    df_sentiment = pd.read_csv('MachineLearning/MyDatasets/ML_training_data_ETH-Ready.csv')

    for x, row in df_sentiment.iterrows():
        for y, find_row_match in df_nonSentiment.iterrows():
            print(row.datetime)
            if row.datetime == find_row_match.datetime:
                #find_row_match[1].avg_twitter_sentiment = row[1].avg_twitter_sentiment
                df_nonSentiment.at[y, 'avg_twitter_sentiment'] = row.avg_twitter_sentiment
                break

    df_nonSentiment.to_csv('MachineLearning/training_data_ETH.csv')


#csv_data_binding()
