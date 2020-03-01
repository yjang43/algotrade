import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from threading import Timer
from time import sleep
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from algorithm import ema

exchange = ccxt.binance()

def ARIMAalgorithm():
    mydf = pd.read_csv('/Users/jae/Documents/Programming/algotrade/source/csv/dayohlcv.csv')
    series = pd.concat([mydf['Time'], mydf['Close']], axis=1)
    series = series.set_index('Time')
    X = series.values
    print(X)
    size = int(len(X))
    train, test = X[0:size], X[size:len(X) +3]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order = (5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))

    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='yellow')
    pyplot.show()
    #pd.plotting.autocorrelation_plot(series)
    #pyplot.show()
    model = ARIMA(series, order = (5,0,0))
    model_fit = model.fit(disp = 0)
    print(model_fit.summary())
    # plot residual errors
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    pyplot.show()
    residuals.plot(kind='kde')
    pyplot.show()
    print(residuals.describe())