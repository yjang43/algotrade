#prediction of bitcoin prices by Neural network model
#2-layer LongShortTermMemory LSTM & Gated Recurrent Unit GRU architecture of RNN

import numpy as np
import pandas as pd 
import statsmodels.api as sm
from scipy import stats 
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from math import sqrt
from random import randint
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import GRU
from keras.callbacks import EarlyStopping
from keras import initializers
from datetime import date
from matplotlib import pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go 
import ccxt


def create_lookback(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)



exchange = ccxt.binance()

mydf = pd.read_csv('/Users/jae/Documents/Programming/algotrade/source/data/dayohlcv.csv')
mydf.isnull().values.any() #check for presence of null values
myseries = pd.concat([mydf['Time'], mydf['Close']], axis=1)
myseries = myseries.set_index('Time')
print(myseries)

d0 = date(2018, 10, 29)
d1 = date(2020, 1, 1)
delta = d1-d0
days_look = delta.days + 1
print(days_look)

d0 = date(2019, 12, 1)
d1 = date(2020, 3, 11)
delta = d1-d0
days_from_train = delta.days + 1
print(days_from_train)

d0 = date(2020, 2, 15)
d1 = date(2020, 3, 11)
delta = d1-d0
days_from_end = delta.days + 1
print(days_from_end)

df_train= myseries[len(myseries)-days_look-days_from_end:len(myseries)-days_from_train]
df_test= myseries[len(myseries)-days_from_train:]

print(len(df_train), len(df_test))


working_data = [df_train, df_test]
working_data = pd.concat(working_data)

working_data = working_data.reset_index()
working_data['Time'] = pd.to_datetime(working_data['Time'])
working_data = working_data.set_index('Time')

s = sm.tsa.seasonal_decompose(working_data.Close.values, freq=60)

print(s)


trace1 = plt.scatter(x = np.arange(0,len(s.trend), 1), y = s.trend, color = 'b', s = 0.1, label = 'trend')
trace2 = plt.scatter(x = np.arange(0,len(s.seasonal), 1), y = s.seasonal, color = 'r', s = 0.1, label = 'seasonal')
trace3 = plt.scatter(x = np.arange(0,len(s.resid), 1), y = s.resid, color = 'g', s = 0.1, label = 'residual')
trace4 = plt.scatter(x = np.arange(0,len(s.observed), 1), y = s.observed, color = 'y', s = 0.1, label = 'observed')
plt.legend(numpoints = 1)
plt.show()

plt.figure(figsize=(15,7))
ax = plt.subplot(211)
sm.graphics.tsa.plot_acf(working_data.Close.values.squeeze(), lags=48, ax=ax)
ax = plt.subplot(212)
sm.graphics.tsa.plot_pacf(working_data.Close.values.squeeze(), lags=48, ax=ax)
plt.tight_layout()
plt.show()

df_train = working_data[:-60]
df_test = working_data[-60:]

training_set = df_train.values
training_set = np.reshape(training_set, (len(training_set), 1))
test_set = df_test.values
test_set = np.reshape(test_set, (len(test_set), 1))

#scale datasets
scaler = MinMaxScaler()
training_set = scaler.fit_transform(training_set)
test_set = scaler.transform(test_set)

# create datasets which are suitable for time series forecasting
look_back = 1
X_train, Y_train = create_lookback(training_set, look_back)
X_test, Y_test = create_lookback(test_set, look_back)

 # reshape datasets so that they will be ok for the requirements of the LSTM model in Keras
X_train = np.reshape(X_train, (len(X_train), 1, X_train.shape[1]))
X_test = np.reshape(X_test, (len(X_test), 1, X_test.shape[1]))

# initialize sequential model, add 2 stacked LSTM layers and densely connected output neuron
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(LSTM(256))
model.add(Dense(1))

# compile and fit the model
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(X_train, Y_train, epochs=100, batch_size=16, shuffle=False,
                    validation_data=(X_test, Y_test),
                    callbacks = [EarlyStopping(monitor='val_loss', min_delta=5e-5, patience=20, verbose=1)])


trace5 = plt.scatter(x = np.arange(0, len(history.history['loss']), 1), y = history.history['loss'], label = 'Train loss', color = 'r')
trace6 = plt.scatter(x = np.arange(0, len(history.history['val_loss']), 1), y = history.history['val_loss'], label = 'Test loss', color = 'b')
data = [trace5, trace6]
plt.show()

X_test = np.append(X_test, scaler.transform(working_data.iloc[-1][0]))
X_test = np.reshape(X_test, (len(X_test), 1, 1))

# get predictions and then make some transformations to be able to calculate RMSE properly in USD
prediction = model.predict(X_test)
prediction_inverse = scaler.inverse_transform(prediction.reshape(-1, 1))
Y_test_inverse = scaler.inverse_transform(Y_test.reshape(-1, 1))
prediction2_inverse = np.array(prediction_inverse[:,0][1:])
Y_test2_inverse = np.array(Y_test_inverse[:,0])

trace1 = plt.scatter(x = np.arange(0, len(prediction2_inverse), 1), y = prediction2_inverse, label = 'Predicted labels', color = 'r')
trace2 = plt.scatter(x = np.arange(0, len(Y_test2_inverse), 1), y = Y_test2_inverse, label = 'True labels', color = 'b')
plt.show()  


