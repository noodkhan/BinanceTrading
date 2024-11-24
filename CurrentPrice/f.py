from binance.client import Client
import pandas as pd
import time
import numpy as np

# API credentials
API_KEY = "api_key"
API_SECRET = "api_secretKey"

client = Client(API_KEY, API_SECRET)

# Strategy parameters
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1MINUTE  # Use 1-minute candlesticks for testing
short_window = 5  # Short moving average
long_window = 15  # Long moving average
initial_balance = 1000  # Simulated balance in USDT
position = 0  # 0 means no position, 1 means holding

# Dataframe to store live data
columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
data = pd.DataFrame(columns=columns)

# Function to calculate moving averages
def calculate_sma(prices, window):
    return prices.rolling(window=window).mean()

# Main loop
try:
    balance = initial_balance
    print("Starting real-time backtest...")
    while True:
        # Fetch the most recent data
        klines = client.get_klines(symbol=symbol, interval=interval, limit=20)
        df = pd.DataFrame(klines, columns=[
            'datetime', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df['close'] = pd.to_numeric(df['close'])
        data = df[['datetime', 'open', 'high', 'low', 'close', 'volume']].copy()

        # Calculate moving averages
        data['SMA_short'] = calculate_sma(data['close'], short_window)
        data['SMA_long'] = calculate_sma(data['close'], long_window)

        # Current prices and signals
        latest_close = data['close'].iloc[-1]
        sma_short = data['SMA_short'].iloc[-1]
        sma_long = data['SMA_long'].iloc[-1]


        print(df)
        print(data)
        print(latest_close)
        print(sma_short)
        print(sma_long)
        


        # Strategy logic
        if position == 0 and sma_short > sma_long:  # Buy signal
            position = 1
            entry_price = latest_close
            print(f"BUY at {entry_price}")
        elif position == 1 and sma_short < sma_long:  # Sell signal
            position = 0
            profit = (latest_close - entry_price) / entry_price * balance
            balance += profit
            print(f"SELL at {latest_close} | Profit: {profit:.2f} | Balance: {balance:.2f}")

        # Wait for the next update
        time.sleep(5)  # Wait 1 minute for the next candle
except KeyboardInterrupt:
    print("Backtest stopped.")
    print(f"Final simulated balance: {balance:.2f}")
