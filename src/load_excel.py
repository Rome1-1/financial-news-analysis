import os 
import pandas as pd
import talib

# Define the folder path where CSV files are located
folder_path = r"C:\Users\teble\financial-news-analysis\notebooks\yfinance_data2"  # Change this path if needed

# List CSV files in the directory (files that end with '.csv')
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Print the list of found CSV files
print("CSV Files Found:", csv_files)

# Create a dictionary to store DataFrames
dataframes = {}

# Load each CSV file into a DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    stock_symbol = file.split('_')[0]  # Use the first part of the file name (e.g., AAPL) as the key
    dataframes[stock_symbol] = pd.read_csv(file_path)

# Check available stock symbols in the dictionary
print("Available stock symbols:", dataframes.keys())

# Check if 'AAPL' data exists
if 'AAPL' in dataframes:
    print("Inspecting 'AAPL' DataFrame:")
    print(dataframes['AAPL'].info())  # Replace 'AAPL' with any stock symbol
else:
    print("'AAPL' data is not available in the DataFrame.")

# Check if all required columns are present
required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
for symbol, df in dataframes.items():
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in {symbol} DataFrame: {missing_columns}")
    else:
        print(f"All required columns are present in {symbol} DataFrame.")

# Add a Stock Symbol column to each DataFrame
for symbol, df in dataframes.items():
    # Ensure we are working on a copy of the DataFrame to avoid modification warnings
    df['Stock Symbol'] = symbol

# Combine all DataFrames into a single DataFrame
combined_data = pd.concat(dataframes.values(), ignore_index=True)

# Check the combined data
print(combined_data.info())
print(combined_data.head())

# Convert 'Date' to datetime and set as index
combined_data['Date'] = pd.to_datetime(combined_data['Date'])
combined_data.set_index('Date', inplace=True)

# Preview the updated DataFrame
print(combined_data.head())

# Check for missing values
print(combined_data.isnull().sum())  # Check missing values

# Drop rows with missing values
combined_data = combined_data.dropna()

# OR Fill missing values with a method (e.g., forward fill)
# combined_data = combined_data.fillna(method='ffill')

# Drop duplicate rows
combined_data = combined_data.drop_duplicates()

# Print the data types of the columns
print(combined_data.dtypes)

# Save the cleaned data to a CSV file
combined_data.to_csv("cleaned_stock_data.csv", index=True)
print("Cleaned data saved to cleaned_stock_data.csv")

# Filter AAPL data
aapl_data = combined_data[combined_data['Stock Symbol'] == 'AAPL'].copy()  # Ensure this is a copy

# Check the AAPL data preview
print(aapl_data.head())

# Calculate the 20-period SMA for AAPL using TA-Lib
aapl_data.loc[:, 'SMA_20'] = talib.SMA(aapl_data['Close'], timeperiod=20)

# Preview the updated AAPL data with the SMA
print(aapl_data[['Close', 'SMA_20']].head())
