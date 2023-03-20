#from chatgpt

import pandas as pd
import numpy as np
import yfinance as yf

# choose stock or cryptocurrency
ticker = 'AAPL'

# download historical data
data = yf.download(ticker, start='2015-01-01', end='2023-03-20')

# calculate moving averages
short_ma = data['Close'].rolling(window=50).mean()
long_ma = data['Close'].rolling(window=200).mean()

# create signal to buy or sell
data['Signal'] = np.where(short_ma > long_ma, 1, 0)
data['Signal'] = np.where(short_ma < long_ma, -1, data['Signal'])

# set up stop-loss and take-profit orders
data['Stop Loss'] = data['Close'] * 0.95
data['Take Profit'] = data['Close'] * 1.05

# create position and strategy returns
data['Position'] = data['Signal'].shift(1)
data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
data['Strategy Returns'] = data['Position'] * data['Returns']

# plot strategy returns
data[['Returns', 'Strategy Returns']].cumsum().plot()
