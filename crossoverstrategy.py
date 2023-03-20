import pandas as pd
import yfinance as yf

# Define the ticker symbol and download data from Yahoo Finance
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2022-03-20")

# Define the short and long moving averages
short_ma = 50
long_ma = 200

# Calculate the short and long moving averages
data["SMA_short"] = data["Close"].rolling(window=short_ma).mean()
data["SMA_long"] = data["Close"].rolling(window=long_ma).mean()

# Define a function to determine the trading signals
def get_signal(data):
    buy_signal = []
    sell_signal = []
    flag = -1

    for i in range(len(data)):
        if data["SMA_short"][i] > data["SMA_long"][i]:
            if flag != 1:
                buy_signal.append(data["Close"][i])
                sell_signal.append(float('nan'))
                flag = 1
            else:
                buy_signal.append(float('nan'))
                sell_signal.append(float('nan'))
        elif data["SMA_short"][i] < data["SMA_long"][i]:
            if flag != 0:
                buy_signal.append(float('nan'))
                sell_signal.append(data["Close"][i])
                flag = 0
            else:
                buy_signal.append(float('nan'))
                sell_signal.append(float('nan'))
        else:
            buy_signal.append(float('nan'))
            sell_signal.append(float('nan'))

    return (buy_signal, sell_signal)

# Get the trading signals
signals = get_signal(data)

# Add the trading signals to the data frame
data["Buy_signal"] = signals[0]
data["Sell_signal"] = signals[1]

# Plot the closing price and the trading signals
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(data["Close"])
plt.plot(data["SMA_short"], label="SMA_short")
plt.plot(data["SMA_long"], label="SMA_long")
plt.scatter(data.index, data["Buy_signal"], color="green", marker="^", alpha=1)
plt.scatter(data.index, data["Sell_signal"], color="red", marker="v", alpha=1)
plt.legend()
plt.show()
