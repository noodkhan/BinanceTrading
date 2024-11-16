# CopyRight Developer Navin Khanthawong Thailand 2024
from binance.client import Client
from collections import deque
import pandas as panda
import datetime 

#############################################################################
        # Connect to Binance Account

# Enter your API key and secret
api_key = "API_KEY"
api_secret = "API_SECRET_KEY"

# Initialize client
client = Client(api_key, api_secret)

# Test connection
account_info = client.get_account()

map = {}
# Set account infomation
for key,value in account_info.items():
    print(key)
    map[key] = value

#############################################################################
        # Personal Account Information 

    # Key Account Information Easy to access
#makerCommission
#takerCommission
#buyerCommission
#sellerCommission
#commissionRates
#canTrade
#canWithdraw
#canDeposit
#brokered
#requireSelfTradePrevention
#preventSor
#updateTime
#accountType

        # Account balances Wallet             

def Get_Balance():
    balance = map["balances"]
    for value in balance : 
        if value["asset"] == "SHIB" : 
            SHIB = value
    return SHIB["free"]

print("My balance is : " , Get_Balance() , " SHIB")

#permissions
#uid
#############################################################################
        # Execute a Trade                       ORDER | BUY
# order = client.create_order(
#     symbol='XRP',
#     side='BUY',
#     type='MARKET',
#     quantity=0.001
# )
# print(order)
#############################################################################
        # Check Price                                   Current Price

target = ["BTCUSDT" , "SHIBUSDT" , "ETHUSDT"]           # INPUT

def GetCurrentPrice(target):
    for key in target : 
        # Get current price of a symbol, e.g., BTC/USDT
        price = client.get_symbol_ticker(symbol=key)
        print(f"Current price of {key} {price['price']}")    # OUTPUT
    return 0

GetCurrentPrice(target)

#############################################################################
        # Check History Price                           History Price

target = ["BTCUSDT" , "SHIBUSDT" , "ETHUSDT"]           # INPUT

def HistoryPrice(target):
    # Fetch historical data for target coins (e.g., 1-day candles)
    for key in target : 
        historical_data = client.get_historical_klines(key , Client.KLINE_INTERVAL_1DAY, "10 month ago UTC")
        for value in historical_data : 
            timeStampSecond = value[0] = value[0] / 1000
            currentTime = datetime.datetime.fromtimestamp(timeStampSecond)
            value[0] = currentTime
            
        dataframe = panda.DataFrame(historical_data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

        dataframe.set_index("timestamp" , inplace=True)
        print(dataframe)                                # Output 

# HistoryPrice(target)
#############################################################################

# make a personal Trading Applications Show Everything 
# make a strategys for price prediction BUY | SELL IN EVERY 5 MINS 
