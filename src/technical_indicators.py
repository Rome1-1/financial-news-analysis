import pandas as pd
import os
import talib
import matplotlib.pyplot as plt

# Path to the folder containing the CSV files
folder_path = r"C:\Users\teble\financial-news-analysis\notebooks\yfinance_data2"  # Update with the correct path

# Ensure the visualization directory exists
visualization_path = "visualizations/plots"
os.makedirs(visualization_path, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(folder_path, file)

    # Read the CSV file
    df = pd.read_csv(file_path, parse_dates=['Date'])

    # Extract stock symbol from the filename
    stock_symbol = file.split('_')[0]

    # Calculate technical indicators
    df['SMA_10'] = talib.SMA(df['Close'], timeperiod=10)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Plot and save Closing Price along with SMA_10 and SMA_50
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price', color='blue')
    plt.plot(df['Date'], df['SMA_10'], label='SMA 10', color='red')
    plt.plot(df['Date'], df['SMA_50'], label='SMA 50', color='green')
    plt.title(f'{stock_symbol} Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.savefig(f"{visualization_path}/{stock_symbol}_sma_plot.png")
    plt.close()

    # Plot and save RSI
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['RSI'], label='RSI', color='orange')
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
    plt.title(f'RSI for {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('RSI Value')
    plt.legend(loc='best')
    plt.savefig(f"{visualization_path}/{stock_symbol}_rsi_plot.png")
    plt.close()

    # Plot and save MACD
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['MACD'], label='MACD', color='purple')
    plt.plot(df['Date'], df['MACD_Signal'], label='MACD Signal', color='red')
    plt.bar(df['Date'], df['MACD_Hist'], label='MACD Histogram', color='gray', alpha=0.3)
    plt.title(f'MACD for {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('MACD Value')
    plt.legend(loc='best')
    plt.savefig(f"{visualization_path}/{stock_symbol}_macd_plot.png")
    plt.close()

    print(f"Plots for {stock_symbol} saved in {visualization_path}.")
