import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, save_model, load_model
import pandas as pd
import time
import random
from collections import deque
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

# This script is for generating predictions from an already created model, it involves batching input data for model input and generating predictions and plotting results on a graph


SEQ_LENGTH = 24
FUTURE_PERIOD_PREDICT = 24
EPOCHS = 25
BATCH_SIZE = 48
currencyPair = 'ADAUSDT'  # the pairing for this run

def preprocess_df(df):
    #df = df.drop('future_close', 1)  # we don't actually need this anymore, only function was to generate 'target' col
    df = df.drop('datetime', 1)  # we don't need this either as it tis more for human eyes purposes

    price_scalar = MinMaxScaler(feature_range=(0, 1))
    # price_scalar = price_scalar.fit(df['close'])  # set the scalar to the price(close) data
    close_prices = df.future_close.to_numpy()
    price_scalar = price_scalar.fit(close_prices.reshape(-1, 1))

    for col in df.columns:
        if col == 'close' or col == 'future_close':
            # price_scalar = price_scalar.fit(df[[col]])
            df[col] = price_scalar.transform(df[col].to_numpy().reshape(-1, 1))

    #list_for_scaling = list([df["close"], df["avg_twitter_sentiment"]])

    df.dropna(inplace=True)
    sequential_data = []
    prev_days = deque(maxlen=SEQ_LENGTH)

    print(df)
    X = []
    Y = []

    for i in range(0, len(df)):
        prev_days.append([df.at[i, 'close'] - 0.001, df.at[i, 'avg_twitter_sentiment']])
        #prev_days.append([df.at[i, 'close'], df.at[i, 'avg_twitter_sentiment'], df.at[i, 'future_close']])
        if len(prev_days) == SEQ_LENGTH:  # make sure we have 35 sequences!
            X.append(prev_days.copy())
            Y.append(df.at[i, 'future_close'])
            #sequential_data.append([prev_days, [df.at[i, 'future_close'] - 0.001]])  # attach the sequence matched with its target, i.e future price

        '''for i in df.values:
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == SEQ_LENGTH:  # make sure we have 35 sequences!
            sequential_data.append([np.array(prev_days), i[-1]])'''

    #random.shuffle(sequential_data)  # shuffle for good measure.

    '''for seq, future_close, in sequential_data:
        X.append(seq)  # X is the sequences
        Y.append(future_close)  # y is the targets/labels (buys vs sell)'''

    return np.array(X), Y, price_scalar

# Load the model
filepath = 'models/ADAUSDT_LSTM_RNN-50-0.000.model'  # the path to the model we want to load
model = load_model(filepath, compile=True)

# Load Training Data
main_df = pd.read_csv(f'MyDatasets/ML_testing_data_{currencyPair}.csv')
#main_df.set_index('time_ID', drop=True, inplace=True)

times = sorted(main_df.index.values)
#last_10_percent = sorted(main_df.index.values)[-int(0.10 * len(times))]  # this returns last 5% of times

#validation_main_df = main_df[(main_df.index >= last_10_percent)]  # basically anywhere where timestamp is in the last 5%
#validation_main_df = validation_main_df.reset_index(drop=True)  # reset index's so they start from 0, this is important for indexing this df in preprocess_df()

#main_df = main_df[(main_df.index < last_10_percent)]

train_x, train_y, train_scalar = preprocess_df(main_df)
#validation_x, validation_y, validation_scalar = preprocess_df(validation_main_df)

train_x = np.asarray(train_x)
train_y = np.asarray(train_y)
#validation_x = np.asarray(validation_x)
#validation_y = np.asarray(validation_y)

train_x = tf.stack(train_x)
train_y = tf.stack(train_y)
#validation_x = tf.stack(validation_x)
#validation_y = tf.stack(validation_y)

print('train_x:')
print(train_x)
# train_x = train_x.reshape(BATCH_SIZE, 24, 2)
print(train_x.shape)

# train_y = keras.utils.to_categorical(train_y)
print('train_y:')
print(train_y.shape)
#print(train_y[0])
len(train_y)

#print(f"train data: {len(train_x)} validation: {len(validation_x)}")

predictions = model.predict(train_x)
#predictions = predictions.flatten()
print(predictions)

predictions = train_scalar.inverse_transform(predictions)
print(predictions)

#score, acc = model.evaluate(validation_x, validation_y)

#print('Test score:', score)
#print('Test accuracy:', acc)

# Visualise the prediction
plt.figure()
plt.plot(predictions, label='LSTM Model Predictions')

train_y_numpy = np.asarray(train_y)
#train_y_numpy.reshape(-1, 1)
plt.plot(train_scalar.inverse_transform(train_y_numpy.reshape(-1, 1)), label='Real Price Values')
plt.title('Predictions')
plt.ylabel('Price')
plt.xlabel('Hours')
plt.legend()  # Show the labels
plt.savefig(f'{currencyPair}_LSTM_modelPredictionsResults.png', format='png')
plt.show()
