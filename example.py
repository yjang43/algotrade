import pandas as pd
import matplotlib.pyplot as plt
import robin_stocks as r
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.tsa.api as smt
from statsmodels.tsa.api import VAR


username = input("username: ")
password = input("password: ")

r.login(username, password)

#stock_to_visualize = input("ticker symbol here: ")

def stock_data_to_df(stock_ticker):
    stock_data = r.get_historicals(stock_ticker, span='week')
    columns = list(stock_data[0].keys())
    df_raw = {col:[] for col in columns}
    for data in stock_data:
        for key in data.keys():
            if df_raw.__contains__(key):
                df_raw[key].append(data[key])
    df = pd.DataFrame(df_raw)
    df['begins_at'] = pd.to_datetime(df['begins_at'])
    df = df.set_index('begins_at')
    df[['open_price', 'close_price', 'high_price', 'low_price', 'volume']] = df[['open_price', 'close_price', 'high_price', 'low_price', 'volume']].apply(pd.to_numeric)
    print(df.head())
    return df

apple = 'goog'
microsoft = 'amzn'
apple_df = stock_data_to_df(apple)
ms_df = stock_data_to_df(microsoft)

# create dataset
apple_price = apple_df['open_price'].rename(apple)
microsoft_price = ms_df['open_price'].rename(microsoft)

dataset = pd.DataFrame({apple_price.name:apple_price, microsoft_price.name:microsoft_price})
print(dataset.head)
print(dataset.shape)


# towardsdatascience.com granger causality code
nobs = 15
X_train, X_test = dataset[0:-nobs], dataset[-nobs:]

print(X_train.shape)
print(X_test.shape)

transform_data = X_train.diff().dropna()
transform_data.head()

maxlag = 12
test = 'ssr_chi2test'
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):
    X_train = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in X_train.columns:
        for r in X_train.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1], 4) for i in range(maxlag)]
            min_p_value = np.min(p_values)
            X_train.loc[r, c] = min_p_value
    X_train.columns = [var + '_x' for var in variables]
    X_train.index = [var + '_y' for var in variables]
    return X_train

granger_ret = grangers_causation_matrix(X_train, variables=X_train.columns)
print(granger_ret)

mod = smt.VAR(transform_data)
res = mod.fit(2)
print(res.summary())

pred = res.forecast(transform_data.values[-5:], 15)
pred_df = pd.DataFrame(pred, index=dataset.index[-15:], columns=dataset.columns)


pred_inverse = pred_df.cumsum()
f = pred_inverse + X_test
print(f)


print(pred_df)




# plot
plt.figure(figsize = (12,5))
plt.xlabel('Date')

ax1 = X_test[apple].plot(color='blue', grid=True, label='Actual apple price')
ax2 = f[apple].plot(color='red', grid=True, secondary_y=True, label='Predicted apple price')

ax1.legend(loc=1)
ax2.legend(loc=2)
plt.show()

r.logout()
