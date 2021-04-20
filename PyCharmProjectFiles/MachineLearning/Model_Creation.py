import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
import time
import random
from collections import deque
# from GetHistoricalDataBinance import get_eth_data_past_seven_days

SEQ_LENGTH = 12
FUTURE_PERIOD_PREDICT = 24
EPOCHS = 25
BATCH_SIZE = 48
NAME = f"{SEQ_LENGTH}-SEQ-{FUTURE_PERIOD_PREDICT}-PRED-{int(time.time())}"


def preprocess_df(df):
    df = df.drop('future_close', 1)  # we don't actually need this anymore, only function was to generate 'target' col
    df = df.drop('datetime', 1)  # we don't need this either as it tis more for human eyes purposes

    for col in df.columns:
        if col != 'target' and col != 'datetime':
            df[col] = df[col].pct_change()
            df.dropna(inplace=True)
            df[col] = preprocessing.scale(df[col].values)

    df.dropna(inplace=True)
    len(df)
    sequential_data = []
    prev_days = deque(maxlen=SEQ_LENGTH)

    for i in df.values:
        prev_days.append([n for n in i[:-1]])  # store all but the target
        if len(prev_days) == SEQ_LENGTH:  # make sure we have 35 sequences!
            sequential_data.append([np.array(prev_days), i[-1]])

    random.shuffle(sequential_data)  # shuffle for good measure.

    # We need to Balance the data set, so that we have even number of buy + sell situations(e.g target 0 or 1)
    buys = []
    sells = []

    for seq, target in sequential_data:
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
    random.shuffle(sequential_data)  # shuffle it all up again

    X = []
    Y = []

    for seq, target, in sequential_data:
        X.append(seq)  # X is the sequences
        Y.append(target)  # y is the targets/labels (buys vs sell)

    return np.array(X), Y


def build_model(data_length, label_length):

    # Load Training Data
    main_df = pd.read_csv('MyDatasets/ML_training_data_ETH.csv')
    main_df.set_index('time_ID', drop=True, inplace=True)
    len(main_df)
    close_prices = main_df.close.to_list()
    sentiment_values = main_df.avg_twitter_sentiment.to_list()

    times = sorted(main_df.index.values)
    last_10_percent = sorted(main_df.index.values)[-int(0.10*len(times))]  # this returns last 5% of times

    validation_main_df = main_df[(main_df.index >= last_10_percent)]  # basically anywhere where timestamp is in the last 5%
    print(len(validation_main_df))
    main_df = main_df[(main_df.index < last_10_percent)]
    print(len(main_df))
    train_x, train_y = preprocess_df(main_df)
    validation_x, validation_y = preprocess_df(validation_main_df)

    train_x = np.asarray(train_x)
    train_y = np.asarray(train_y)
    validation_x = np.asarray(validation_x)
    validation_y = np.asarray(validation_y)

    print(f"train data: {len(train_x)} validation: {len(validation_x)}")
    # print(f"Dont buys: {train_y.count(0)}, buys: {train_y.count(1)}")
    # print(f"VALIDATION Dont buys: {validation_y.count(0)}, buys: {validation_y.count(1)}")

    model = Sequential()
    model.add(LSTM(128, input_shape=(train_x.shape[1:]), return_sequences=True, activation="relu"))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())

    model.add(LSTM(128, input_shape=(train_x.shape[1:]), return_sequences=True, activation="relu"))
    model.add(Dropout(0.1))
    model.add(BatchNormalization())

    model.add(LSTM(128, input_shape=(train_x.shape[1:]), activation="relu"))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())

    model.add(Dense(32, activation="relu"))
    model.add(Dropout(0.2))

    model.add(Dense(2, activation="softmax"))

    optimiser = tf.keras.optimizers.Adam(learning_rate=0.001, decay=1e-6)

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimiser,
                  metrics=['accuracy'])

    tensorboard = TensorBoard(log_dir=f'logs/{NAME}')

    filepath = "RNN_Final-{epoch:02d}-{val_accuracy:.3f}"  # unique file name that will include the epoch and the validation acc for that epoch
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



    '''price = keras.Input(shape=(data_length, 1), name='price')
    sentiment = keras.Input(shape=(data_length, 1), name='sentiment')

    price_layers = LSTM(64, return_sequences=True)(price)
    sentiment_layers = LSTM(64, return_sequences=True)(sentiment)

    output = keras.concatenate(
        [
            price_layers,
            sentiment_layers
        ]
    )

    output = Dense(label_length, activation='linear', name)

    # price_data = get_eth_data_past_seven_days()



    # Prepare Data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(price_data['close'].values.reshape(-1, 1))

    prediction_days = 7

    x_train = []
    y_train = []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x - prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build Neural Network Model
    model = Sequential()

    model.add(LSTM(units=64, return_sequences=True, input_shape=(x_train.shape[1:], 1)), activation='relu')
    model.add(Dropout(0.2))
    model.add(LSTM(units=64, return_sequences=True), activation='relu')
    model.add(Dropout(0.2))
    model.add(LSTM(units=64))
    model.add(Dropout(0.2))
    model.add(Dense(units=16), activation='relu')  # Prediction of next closing price
    model.add(Dropout(0.2))
    model.add(Dense(units=16), activation='softmax')

    opt = keras.optimizers.Adam(lr=1e-3, decay=1e-5)
    model.compile(optimizer=opt, loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, validation_data=(x_test, y_test))

    # Test the model accuracy on Existing Data

    # Load Test Data'''


build_model(1, 1)
