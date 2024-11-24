from dash import Dash, dcc, html
import plotly.graph_objects as go
from binance.client import Client
import pandas as pd
import datetime 
import time
#############################################################################
targets = ["BTCUSDT" , "SHIBUSDT" , "ETHUSDT"]           # INPUT
#############################################################################
API_KEY = "api_key"
API_SECRET = "api_secretKey"
# Initialize Binance client
client = Client(API_KEY, API_SECRET)
# Test connection
account_info = client.get_account()

#############################################################################
map = {}
# Set account infomation
for key,value in account_info.items():
    map[key] = value
# Account balances Wallet             
def Get_Balance():
    balance = map["balances"]
    for value in balance : 
        if value["asset"] == "SHIB" : 
            SHIB = value
    return SHIB["free"]

print("My balance is : " , Get_Balance() , " SHIB")
# Check Price                                   
def GetCurrentPrice(target):
    for key in target : 
        # Get current price of a symbol, e.g., BTC/USDT
        price = client.get_symbol_ticker(symbol=key)
        # print(f"Current price of {key} {price['price']}")    # OUTPUT
    return 0

#############################################################################
        # Check History Price                           History Price
def HistoryPrice(target):
    # Fetch historical data for target coins (e.g., 1-day candles)
    for key in target : 
        historical_data = client.get_historical_klines(key , Client.KLINE_INTERVAL_1DAY, "12 month ago UTC")
        for value in historical_data : 
            timeStampSecond = value[0] = value[0] / 1000
            currentTime = datetime.datetime.fromtimestamp(timeStampSecond)
            value[0] = currentTime 
        dataframe = pd.DataFrame(historical_data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        dataframe.set_index("timestamp" , inplace=True)
        # print(dataframe)                                # Output 
#############################################################################
# Fetch historical candlestick data
def fetch_binance_data(symbol, interval , limit):
    candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'trades', 
        'taker_base', 'taker_quote', 'ignore'
    ])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    return df.astype(float)

#############################################################################

dataFrame = fetch_binance_data("BTCUSDT", "1d" , limit=100)
#dataFrameSHIB = fetch_binance_data("SHIBUSDT", "5d" , limit=100)
#############################################################################
# Chart 1: Candlestic khart 
candleChart = go.Figure(data=[

    go.Candlestick(
        x = dataFrame.index,
        open = dataFrame['open'] , 
        low = dataFrame['low'] , 
        high = dataFrame['high'] , 
        close = dataFrame['close'] , 
    ),

    # go.Candlestick(
    #     x = dataFrameSHIB.index,
    #     open = dataFrameSHIB['open'] , 
    #     low = dataFrameSHIB['low'] , 
    #     high = dataFrameSHIB['high'] , 
    #     close = dataFrameSHIB['close'] , 
    # ),

])

# Chart 2: Line chart
lineChart = go.Figure(data=go.Scatter(
    x = dataFrame.index, 
    y = dataFrame['close'] , 
    mode="lines+markers",
    name="Price"
))

barchart = go.Figure(data=[
    go.Bar(
        x = dataFrame.index , 
        y = dataFrame['open'] ,  
        name = "Opening Price" , 
        marker=dict(color='blue')  
    ), 
    go.Bar(
        x = dataFrame.index , 
        y = dataFrame['close'] ,  
        name = "Close Price" , 
        marker=dict(color='orange')  
    ), 

    go.Bar(
        x = dataFrame.index , 
        y = dataFrame['volume'] ,  
        name = "volume" , 
        marker=dict(color='green')  
    ), 
])


barchartVolume = go.Figure(data=[
    go.Bar(
        x = dataFrame.index , 
        y = dataFrame['volume'] ,  
        name = "volume" , 
        marker=dict(color='green')  
    ), 
])


coinDetails = []
# fetch latest prices for all trading pairs
prices = client.get_all_tickers()

market = 0

for price in prices :
    market = market + float(price['price'])

for price in prices:
    array = []
    array.append(price['symbol'])
    percentage = float(price['price']) / market
    percentage = percentage
    array.append(percentage * 100)
    coinDetails.append(array)


names = []
percentages = []
for array in coinDetails : 
    names.append(array[0])
    percentages.append(array[1])


# print(f" World MarketCap Total : {market} $ Dollar")

pieChart = go.Figure(data=go.Pie(
    labels=names, 
    values=percentages,
    textinfo='label+percent' , 
    marker=dict(colors=["#ff6347" , "#4682b4"  , "#32cd32"]) , 
))

# 4.Heatmap 
heatmapChart = go.Figure(go.Heatmap(
    z=[[1, 2], [3, 4]]
))

boxplotChart = go.Figure(go.Box(
    y=[7,8,9,10,10,11]
))

sunburstChart = go.Figure(go.Sunburst(
    labels=["A", "B", "C"], 
    parents=["", "A", "A"]
))

#############################################################################
# Update Layout for Each Chart
candleChart.update_layout(
    title="Real Time Binance CnadleStick Chart" , 
    xaxis_title = "Time" , 
    yaxis_title = "Price" , 
    template = "plotly_dark" , 
    xaxis_rangeslider_visible=False
)

lineChart.update_layout(
    title="Line Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)


barchart.update_layout(
    title="Price and Volume Comparison" , 
    xaxis_title = "Date" , 
    yaxis_title = "price / Volume" , 
    barmode = 'group' , 
    template = "plotly_dark" , 
    showlegend=True , 
    legend_title = "Data Type" , 
    font=dict(color="white") , 
    title_x=0.5
)

barchartVolume.update_layout(
    title="Volume Chart" , 
    xaxis_title = "Date" , 
    yaxis_title = "Volume" , 
    barmode = 'group' , 
    template = "plotly_dark" , 
    showlegend=True , 
    legend_title = "Data Type" , 
    font=dict(color="white") , 
    title_x=0.5
)


# Update layout
pieChart.update_layout(
    title="OHLC and Volume Distribution",
    template="plotly_dark",
    showlegend=True
)


# 5. Heatmap Chart
heatmapChart.update_layout(
    title="Heatmap Chart",
    xaxis_title="X Axis",
    yaxis_title="Y Axis",
    template="plotly_dark"
)

# 7. Sunburst Chart
sunburstChart.update_layout(
    title="Sunburst Chart",
    template="plotly_dark"
)

#############################################################################

# GetCurrentPrice(target)
# HistoryPrice(target) # f(input)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph' , animate=True , figure=candleChart), 
    dcc.Interval(
        id='graph-update',
        interval=1*1000, #update Every second (1000 ms)
        n_intervals =0
    ),
    dcc.Graph(figure=lineChart) , 
    dcc.Graph(figure=barchart) , 
    dcc.Graph(figure=barchartVolume) , 
    # dcc.Graph(figure=pieChart) ,      Slow Algorithms
    # dcc.Graph(figure=sunburstChart) , UnderDevelopment
    # dcc.Graph(figure=heatmapChart) ,  UnderDevelopment
    # dcc.Graph(figure=boxplotChart) ,  UnderDevelopment
])

if __name__ == "__main__" :
    app.run_server(debug=True)

#############################################################################


#permissions
#uid
#############################################################################
        # Execute a Trade                       
# order = client.create_order(
#     symbol='XRP',
#     side='BUY',
#     type='MARKET',
#     quantity=0.001
# )
# print(order)
#############################################################################

