# LSTM-Based Algorithmic Option Trading Bot:

### Concept:
This Python bot was designed for the UIUC Spring 2022 Trading Challenge (hosted by the Margolis Market Information Lab & CME Group). 
The bot uses a basic LSTM model trained on historical data to predict current Bitcoin (BTC) prices based on the past week of activity. 
Then, the bot will select the optimal BTC option trading strategy (selecting between a long straddle, iron condor, and broken-wing butterfly) to account for BTC price movement. 
BTC was chosen as the optimal security among CME's selection due to its volatility (making it ideal for options trading). 
Finally, once a strategy is chosen, the proper trades will be automatically submitted to the CME Challenge Simulator website using Selenium-powered web automation. 

### Model Performance:
LSTM model has ±5.1% average error. Given that BTC prices are currently hovering around $40,000 it would generally be optimal for the model to be far more accurate (as 5% of $40k is $2,000, which is a pretty wide margin). 
Fortunately, since this trading bot is based more on an accurate prediction of directional volatility than accurate price prediction, the model proved sufficient for the purposes of option trading. 
However, I do hope to continue learning how to improve and optimize machine learning models (including LSTMs). This is the first LSTM model I've made, and I hope to improve as I gain more experience.

### Competition Performance:
N/A yet. Competition is currently in progress during the month of March!

### More Info:
N/A yet.