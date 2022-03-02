import functions_bot as bot

username, password = open('credentials.txt', 'r').readlines()

#init bot
tradingbot = bot.TradingBot(username, password)
tradingbot.login()

print(tradingbot.get_dashboard_stats())

# tradingbot.open_options_simulator()
#print(tradingbot.get_BTC_price())
print(tradingbot.get_options())

tradingbot.flatten_all_positions()