import functions_bot as bot
from tensorflow.keras.models import load_model
import requests as req
import time

import keras.initializers.initializers_v1
import pandas as pd
import numpy as np
import math
import datetime as dt
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots



# import LSTM model
model = load_model('btc_lstm')
print("LSTM Model loaded.")
# init bot
username, password = open('credentials.txt', 'r').readlines()
tradingbot = bot.TradingBot(username, password)
print("TradingBot instance initiated.")


# loop @ ~9am
bot_running = True
lastday = 0
print("Starting loop...")
while bot_running:
    currenttime = dt.datetime.now()
    runbot = False
    # CHECK IF DAY HAS BEEN USED YET & IF IT IS 9AM
    if lastday != currenttime.day and currenttime.hour == 9:
        runbot = True
        lastday = currenttime.day
    if runbot:
        print(f"BOT EXECUTING:\n"
              f"------------------\n"
              f"Date: {currenttime.month}/{currenttime.day}/{currenttime.year}\n"
              f"Time: {currenttime.hour}:{currenttime.minute}")
        # TRY/EX FOR BOT & POSITION RESET:
        try:
            tradingbot.reset_option_pull()
            tradingbot.quit_driver()
            tradingbot.reset_driver()
            tradingbot.login()
            tradingbot.flatten_all_positions()
            time.sleep(60) # 1 min wait time to ensure that position flattening goes through
        except:
            print("ERROR: There was an error resetting the trading bot and/or flattening existing positions."); break
        # TRY/EX FOR PRICING DATA & PORFOLIO DATA:
        try:
            btc_price = int(tradingbot.get_BTC_price())
            portfolio_stats = tradingbot.get_dashboard_stats()
            print(f"Current BTC Price: ${btc_price}\n"
                  f"Portfolio Balance: {portfolio_stats['balance']}\n"
                  f"Net P/L: {portfolio_stats['net_pl']}")
        except:
            print("ERROR: There was an error getting pricing & portfolio data."); break
        # TRY/EX FOR MARKET DATA:
        try:
            today = int(time.mktime(dt.datetime(currenttime.year, currenttime.month, currenttime.day, 0, 0).timetuple()))
            startdate = int(today-7776000)
            # fetch & parse market data
            pred_data = pd.read_csv(
                f'https://query1.finance.yahoo.com//v7/finance/download/BTC-USD?period1={startdate}&period2={today}&interval=1d&events=history&includeAdjustedClose=true')
            pred_data = pred_data.tail(7)
            pred_data = pred_data.reindex(index=pred_data.index[::-1])
            pred_data = pred_data['Close']
            print("Market data successfully parsed.")
        except:
            print("ERROR: There was an error fetching and/or processing relevant market data."); break
        # TRY/EX FOR MODEL PREDICTION:
        try:
            # scale market data
            scaler = MinMaxScaler(feature_range=(0, 1))
            # use full historical data for scaler transform to ensure rescaled prediction values from 1-week data scale equivalent to training data
            pred_data = scaler.fit_transform(np.array((pd.read_csv('BTC-USD.csv')['Close'])).reshape(-1, 1))
            # make new price prediction
            prediction = model.predict(pred_data)
            # rescale prediction
            prediction = scaler.inverse_transform(prediction)
            print(f"PREDICTED BTC PRICE: ${prediction[0][0]}")
        except:
            print("ERROR: There was an error generating the LSTM model price prediction."); break
        # TRY/EX FOR PICKING STRATEGY:
        try:
            strategy = tradingbot.choose_strategy(prediction[0][0])
            print(f"STRATEGY: {strategy}")
        except:
            print("ERROR: There was an error selecting the optimal strategy.")
        # TRY/EX FOR EXECUTING STRATEGY
        try:
            if strategy == "nothing":
                print("Strategy successful. Nothing done.")
            elif strategy == "straddle":
                # bot will attempt to build a long straddle
                tradingbot.build_straddle()
                print("Successfully built Long Straddle.")
            elif strategy == "ironcondor":
                # bot will use the IC function to attempt to build an IC around strike
                # if IC fails due to margin/bal, a brokenwing butterfly will be attempted, if that too fails, the entire process will be terminated
                trade = tradingbot.build_iron_condor(prediction, btc_price)
                print(f"Successfully attempted Iron Condor strategy. Trade Code: {trade}")
        except:
            print("ERROR: Strategy could not be executed by webdriver."); break
    print("Bot cycle complete for the day.\n")
    time.sleep(600) #wait 10m in between loop runs