import functions_bot as bot

username, password = open('credentials.txt', 'r').readlines()

#init bot
tradingbot = bot.TradingBot(username, password)
tradingbot.login()

print(tradingbot.get_dashboard_stats())

# tradingbot.open_options_simulator()
print(tradingbot.get_BTC_price())
print(tradingbot.get_options())

#tradingbot.purchase_option(chain_index=11, buy=True, qty=1, call=True, on_chain=True)
#tradingbot.build_straddle()
#tradingbot.build_iron_condor()