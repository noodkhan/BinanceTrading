# CopyRight Developer Navin Khanthawong Thailand 2024
from binance.client import Client
from collections import deque
import pandas as panda
import datetime 

#############################################################################
        # Connect to Binance Account

# Enter your API key and secret
api_key = "api_key"
api_secret = "api_secrectKey"


# Initialize client
client = Client(api_key, api_secret)

# Test connection
account_info = client.get_account()


map = {}
# Set account infomation
for key,value in account_info.items():
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
        historical_data = client.get_historical_klines(key , Client.KLINE_INTERVAL_1DAY, "12 month ago UTC")
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


HistoryPrice(target) # f(input)

    # dcc.Graph(figure=scatChart) , 
    # dcc.Graph(figure=violinChart) , 
    # dcc.Graph(figure=funnelChart) , 
    # dcc.Graph(figure=scat2dChat) , 
    # dcc.Graph(figure=choroplethChart) , 
    # dcc.Graph(figure=contourChart) , 
    # dcc.Graph(figure=sankeyChart) , 
    # dcc.Graph(figure=scat3DChart) ,  
    # dcc.Graph(figure=mesh3Dchart) , 



# Binance API credentials

# API_KEY = "your_api_key"
# API_SECRET = "your_api_secret"

# # 1. Scatter 3D Chart
# scat3DChart.update_layout(
#     title="3D Scatter Chart",
#     scene=dict(
#         xaxis_title="X Axis",
#         yaxis_title="Y Axis",
#         zaxis_title="Z Axis"
#     ),
#     template="plotly_dark"
# )

# scatChart = go.Figure(go.Scattergeo(
#     lat=[37.7749],
#     lon=[-122.4194],
#     mode="markers"
# ))


# # 2. 3D Mesh Chart
# mesh3Dchart.update_layout(
#     title="3D Mesh Chart",
#     scene=dict(
#         xaxis_title="X Axis",
#         yaxis_title="Y Axis",
#         zaxis_title="Z Axis"
#     ),
#     template="plotly_dark"
# )

# # 3. Geographic Scatter Chart
# scatChart.update_layout(
#     title="Geographic Scatter Chart",
#     geo=dict(
#         showland=True,
#         landcolor="rgb(217, 217, 217)",
#         showlakes=True,
#         lakecolor="rgb(255, 255, 255)",
#         showocean=True,
#         oceancolor="rgb(204, 204, 255)"
#     ),
#     template="plotly_dark"
# )

# # 4. Choropleth Chart
# choroplethChart.update_layout(
#     title="Choropleth Chart",
#     geo=dict(
#         showframe=False,
#         showcoastlines=True,
#         projection_type="equirectangular"
#     ),
#     template="plotly_dark"
# )


# # 6. Contour Chart
# contourChart.update_layout(
#     title="Contour Chart",
#     xaxis_title="X Axis",
#     yaxis_title="Y Axis",
#     template="plotly_dark"
# )

# # 8. Sankey Diagram
# sankeyChart.update_layout(
#     title="Sankey Diagram",
#     template="plotly_dark"
# )

# # 9. 2D Scatter Chart
# scat2dChat.update_layout(
#     title="2D Scatter Chart",
#     xaxis_title="X Axis",
#     yaxis_title="Y Axis",
#     template="plotly_dark"
# )


# violinChart = go.Figure(go.Violin(
#     y=[7,8,9,10,10,11]
# ))



# funnelChart = go.Figure(go.Funnel(
#     y =["stage1" , "stage2" , "stage3"] , 
#     x = [100 , 50 , 25]
# ))

# scat3DChart = go.Figure(go.Scatter3d(
#     x=[1, 2, 3], 
#     y=[4, 5, 6], 
#     z=[7, 8, 9], 
#     mode="markers"
#     ))

# mesh3Dchart = go.Figure(go.Mesh3d(
#     x=[1, 2, 3],
#     y=[4, 5, 6],
#     z=[7, 8, 9]
# ))

# choroplethChart = go.Figure(go.Choropleth(
#     z=[10, 20, 30],
#     locations=["USA", "CAN", "MEX"],
#     locationmode="ISO-3"
# ))

# contourChart = go.Figure(go.Contour(
#     z=[[1, 2], [3, 4]]
# ))

# sankeyChart = go.Figure(go.Sankey(
#     node=dict(label=["A", "B", "C"]),
#     link=dict(source=[0, 1], target=[1, 2], value=[8, 4])
# ))

# scat2dChat = go.Figure(go.Scatter(
#     x=[1, 2, 3], 
#     y=[4, 5, 6], 
#     mode="markers", 
#     marker=dict(size=[10, 20, 30])
# ))

