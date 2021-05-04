import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
import time
from datetime import datetime
import random
import os
from collections import deque
# from GetHistoricalDataBinance import get_eth_data_past_seven_days


params = {
    "batch_size": 1,
    "epochs": 50,
    "lr": 0.0000010000,
    "time_steps": 24
}
TIME_STEPS = params["time_steps"]

CURRENCY_PAIR = "ETHUSDT"           # the currency pairing for this model creation, either (BTCUSDT, ADAUSDT, ETHUSDT) for current databases
SEQ_LENGTH = 24              # the number of observations(1h intervals) in a sequence. (the model makes a prediction after processing a sequence)
FUTURE_PERIOD_PREDICT = 24   # how many intervals(1h) into the future we want to predict
EPOCHS = 50                  # the number of times we want to process the data
BATCH_SIZE = params["batch_size"]   # the number of training examples in one forward/backward pass. The higher the batch size, the more memory space you'll need.
NAME = f"{CURRENCY_PAIR}" + "_LSTM_{SEQ_LENGTH}-SEQ-{FUTURE_PERIOD_PREDICT}-PRED-{int(time.time())}"  # Name we save model as


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

    df.dropna(inplace=True)
    prev_days = deque(maxlen=SEQ_LENGTH)

    test = 0
    print(df)
    X = []
    Y = []

    for i in range(0, len(df)):
        print(i)
        print(df.at[i, 'close'])
        prev_days.append([df.at[i, 'close'] - 0.001, df.at[i, 'avg_twitter_sentiment']])
        #prev_days.append([df.at[i, 'close'], df.at[i, 'avg_twitter_sentiment'], df.at[i, 'future_close']])
        if len(prev_days) == SEQ_LENGTH:  # make sure we have 35 sequences!
            X.append(prev_days.copy())
            Y.append([df.at[i, 'future_close']])
            #sequential_data.append([prev_days, [df.at[i, 'future_close'] - 0.001]])  # attach the sequence matched with its target, i.e future price
            test = test + 1

        '''for i in df.values:
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == SEQ_LENGTH:  # make sure we have 35 sequences!
            sequential_data.append([np.array(prev_days), i[-1]])'''

    #random.shuffle(sequential_data)  # shuffle for good measure.



    '''for seq, future_close, in sequential_data:
        X.append(seq)  # X is the sequences
        Y.append(future_close)  # y is the targets/labels (buys vs sell)'''

    return np.array(X), Y, price_scalar

    '''# We need to Balance the data set, so that we have even number of buy + sell situations(e.g target 0 or 1)
    buys = []
    sells = []

    for seq, future_close in sequential_data:
        if target == 0:
            sells.append([seq, target])
        elif target == 1:
            buys.append([seq, target])

    random.shuffle(buys)
    random.shuffle(sells)

    lower = min(len(buys), len(sells))  # find lowest length of 2 lists
    # resize the lists so we have even buys & sells
    buys = buys[:lower]
    sells = sells[:lower]

    sequential_data = buys + sells
    random.shuffle(sequential_data)  # shuffle it all up again'''


def build_model(currencyPair):

    # Load Training Data
    main_df = pd.read_csv(f'MyDatasets/ML_training_data_{currencyPair}.csv')
    #main_df.set_index('time_ID', drop=True, inplace=True)
    len(main_df)
    close_prices = main_df.close.to_list()
    sentiment_values = main_df.avg_twitter_sentiment.to_list()

    times = sorted(main_df.index.values)
    last_10_percent = sorted(main_df.index.values)[-int(0.10*len(times))]  # this returns last 5% of times

    validation_main_df = main_df[(main_df.index >= last_10_percent)]  # basically anywhere where timestamp is in the last 5%
    validation_main_df = validation_main_df.reset_index(drop=True)  # reset index's so they start from 0, this is important for indexing this df in preprocess_df()
    main_df = main_df[(main_df.index < last_10_percent)]
    train_x, train_y, train_scalar = preprocess_df(main_df)
    validation_x, validation_y, validation_scalar = preprocess_df(validation_main_df)


    train_x = np.asarray(train_x)
    train_y = np.asarray(train_y)
    validation_x = np.asarray(validation_x)
    validation_y = np.asarray(validation_y)

    train_x = tf.stack(train_x)
    train_y = tf.stack(train_y)
    validation_x = tf.stack(validation_x)
    validation_y = tf.stack(validation_y)

    print(f"train data: {len(train_x)} validation: {len(validation_x)}")
    #print(f"Dont buys: {train_y.count(0)}, buys: {train_y.count(1)}")
    #print(f"VALIDATION Dont buys: {validation_y.count(0)}, buys: {validation_y.count(1)}")

    model = Sequential()
    # input_shape=(TIME_STEPS, 2) == 24 timesteps per batch, 2 features for each time step
    model.add(LSTM(100, input_shape=(TIME_STEPS, 2), return_sequences=True, activation="relu", kernel_initializer='random_uniform'))
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(LSTM(60, return_sequences=True, activation="relu"))
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(LSTM(32, activation="relu"))
    model.add(Dropout(0.2))
    #model.add(BatchNormalization())
    model.add(Dense(20, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation="linear"))

    optimiser = tf.keras.optimizers.Adam(lr=params["lr"])     # learning_rate=0.001, decay=1e-6)

    model.compile(loss='mean_squared_error', optimizer=optimiser, metrics=['accuracy'])

    model.summary()

    tboard_log_dir = os.path.join("logs", NAME)
    tensorboard = TensorBoard(log_dir=tboard_log_dir)

    filepath = f"{currencyPair}" + "_LSTM_RNN-{epoch:02d}-{val_accuracy:.3f}"  # unique file name that will include the epoch and the validation acc for that epoch
    checkpoint = ModelCheckpoint("models/{}.model".format(filepath, monitor='val_accuracy', verbose=1, save_best_only=True,
                                                         mode='max'))  # saves only the best ones

    # Train model
    history = model.fit(
        train_x, train_y,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(validation_x, validation_y),
        callbacks=[tensorboard, checkpoint],
    )

    #validation_x.shape
    predictions = model.predict(validation_x)
    predictions = validation_scalar.inverse_transform(predictions)

    print(predictions)

    score, acc = model.evaluate(validation_x, validation_y)

    print('Test score:', score)
    print('Test accuracy:', acc)


build_model(CURRENCY_PAIR)
