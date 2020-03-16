#prediction of bitcoin prices by Neural network model
#2-layer LongShortTermMemory LSTM & Gated Recurrent Unit GRU architecture of RNN

import numpy as np
import pandas as pd 
import statsmodels.api as sm
from scipy import stats 
from sklearn.metrics import mean_squared_error
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


exchange = ccxt.binance()

mydf = pd.read_csv('/Users/jae/Documents/Programming/algotrade/source/csv/dayohlcv.csv')
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

trace1 = plt.scatter(x = np.arange(0, len(s.trend), 1),y = s.trend, name = 'Trend', c = '#1f77b4')
trace2 = plt.scatter(x = np.arange(0, len(s.seasonal), 1),y = s.seasonal, name = 'Seasonal', c= '#1f77b4')
trace3 = plt.scatter(x = np.arange(0, len(s.resid), 1),y = s.resid, name = 'Residual', c = '#1f77b4')
trace4 = plt.scatter(x = np.arange(0, len(s.observed), 1),y = s.observed, name = 'Observed', c = '#1f77b4')

data = [trace1, trace2, trace3, trace4]
layout = dict(title = 'Seasonal decomposition', xaxis = dict(title = 'Time'), yaxis = dict(title = 'Price, USD'))
fig = dict(data=data, layout=layout)



