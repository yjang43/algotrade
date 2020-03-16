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
    #flags = {correct : 0, wrong : 0}
    #setting training and testing data
    mydf = pd.read_csv('/Users/jae/Documents/Programming/algotrade/source/csv/dayohlcv.csv')
    mydf = mydf[:]
    myseries = pd.concat([mydf['Time'], mydf['Close']], axis=1)
    myseries = myseries.set_index('Time')

    # pd.plotting.autocorrelation_plot(series)
    # pyplot.show()
    dfforecast = pd.DataFrame()

    for x in range(50):
        print ("////////////////////////////////////////////////////////////////////////////////////")
        series = myseries[0: len(myseries) - 50 + x]
        splitpoint = len(series) - 1
        train, test = series[0:splitpoint], series[splitpoint:]
        print('Train %d, Test %d' % (len(train), len(test)))
        train.to_csv('csv/train.csv')
        test.to_csv('csv/test.csv')


        #loading them back in
        X = train.values
        #fit model
        model = ARIMA(X, order = (5,0,1))
        model_fit = model.fit(disp = 0)
        #print summary
        #print(model_fit.summary())

        # one-step out-of sample forecast
        forecast = model_fit.forecast(steps = 1)[0]

        error = mean_squared_error(test, forecast)
        print("Error", error)
        print("Test", test)

        dfforecast1 = pd.DataFrame({
            'Time' : test.index,
            'Close': forecast
            })
        dfforecast1 = dfforecast1.set_index('Time')
        dfforecast = dfforecast.append(dfforecast1)
    
    print(dfforecast)
    splitpoint = len(series) - 50
    train, test = series[0:splitpoint], series[splitpoint:]
    # history = [x for x in train]
    # predictions = list()
    # for t in range(len(test)):
    #     model = ARIMA(history, order = (5,1,0))
    #     model_fit = model.fit(disp=0)
    #     output = model_fit.forecast()
    #     yhat = output[0]
    #     predictions.append(yhat)
    #     obs = test[t]
    #     history.append(obs)
    #     print('predicted=%f, expected=%f' % (yhat, obs))

    # error = mean_squared_error(test, predictions)
    # print('Test MSE: %.3f' % error)
    # plot
    pyplot.plot(train, color = 'red')
    pyplot.plot(test, color = 'green')
    pyplot.plot(dfforecast, color='blue')
    pyplot.show()

    #pd.plotting.autocorrelation_plot(series)
    #pyplot.show()

    # model = ARIMA(series, order = (5,0,0))
    # model_fit = model.fit(disp = 0)
    # print(model_fit.summary())
    # # plot residual errors
    # residuals = pd.DataFrame(model_fit.resid)
    # residuals.plot()
    # pyplot.show()
    # residuals.plot(kind='kde')
    # pyplot.show()
    # print(residuals.describe())