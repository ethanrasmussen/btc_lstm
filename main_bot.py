import functions_bot as bot

username, password = open('credentials.txt', 'r').readlines()

#init bot
tradingbot = bot.TradingBot(username, password)
tradingbot.login()
print(tradingbot.get_dashboard_stats())