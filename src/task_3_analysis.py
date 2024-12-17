import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load Stock Data (example for AAPL)
def load_stock_data(file_path):
    stock_data = pd.read_csv(file_path)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Assuming stock data uses 'Date'
    stock_data = stock_data.sort_values(by='Date')
    stock_data = stock_data.rename(columns={'Date': 'date'})  # Rename 'Date' to 'date' for consistency
    return stock_data

# Load News Data (assumed CSV for simplicity)
def load_news_data(file_path):
    news_data = pd.read_csv(file_path)
    news_data['date'] = pd.to_datetime(news_data['date'])
    return news_data

# Sentiment Analysis using TextBlob
def get_sentiment_score(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Positive, negative, or neutral sentiment

# Aggregate Sentiment by Date
def aggregate_sentiment_by_date(news_data):
    news_data['Sentiment'] = news_data['headline'].apply(get_sentiment_score)
    daily_sentiment = news_data.groupby('date')['Sentiment'].mean().reset_index()
    return daily_sentiment

# Merge News Sentiment with Stock Data
def merge_stock_and_news(stock_data, daily_sentiment):
    merged_data = pd.merge(stock_data, daily_sentiment, how='left', on='date')
    return merged_data

# Calculate Daily Returns from Stock Data
def calculate_daily_returns(stock_data):
    stock_data['Daily Return'] = stock_data['Close'].pct_change() * 100  # percentage change
    return stock_data

# Perform Correlation Analysis
def correlation_analysis(merged_data):
    merged_data = merged_data.dropna(subset=['Daily Return', 'Sentiment'])
    correlation = merged_data['Daily Return'].corr(merged_data['Sentiment'])
    return correlation

# Visualize Sentiment and Stock Returns
def plot_sentiment_vs_stock(merged_data):
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data['date'], merged_data['Sentiment'], label='Sentiment', color='blue')
    plt.plot(merged_data['date'], merged_data['Daily Return'], label='Daily Return', color='red')
    plt.title('Sentiment vs. Stock Returns')
    plt.xlabel('Date')
    plt.ylabel('Sentiment / Daily Return (%)')
    plt.legend()
    plt.show()

# Main function to run the entire analysis
def run_task_3(stock_file, news_file):
    # Load data
    stock_data = load_stock_data(stock_file)
    news_data = load_news_data(news_file)
    
    # Aggregate sentiment by date
    daily_sentiment = aggregate_sentiment_by_date(news_data)
    
    # Merge stock data with sentiment data
    merged_data = merge_stock_and_news(stock_data, daily_sentiment)
    
    # Calculate daily returns
    merged_data = calculate_daily_returns(merged_data)
    
    # Perform correlation analysis
    correlation = correlation_analysis(merged_data)
    
    # Output correlation result
    print(f'Correlation between sentiment and stock returns: {correlation}')
    
    # Plot the data for visualization
    plot_sentiment_vs_stock(merged_data)

# Example usage
if __name__ == "__main__":
    # Replace with your actual file paths
    stock_file = r'C:\Users\teble\financial-news-analysis\notebooks\yfinance_data2\AAPL_historical_data.csv'  # Example stock file
    news_file = r'C:\Users\teble\financial-news-analysis\notebooks\data\news_data.csv'  # Replace with your actual news data file

    run_task_3(stock_file, news_file)
    
def load_stock_data(file_path):
    stock_data = pd.read_csv(file_path)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Ensure that the 'Date' column is in datetime format
    stock_data = stock_data.sort_values(by='Date')  # Sort stock data by date
    stock_data = stock_data.rename(columns={'Date': 'date'})  # Rename 'Date' to 'date' to match news data
    return stock_data

def load_news_data(file_path):
    news_data = pd.read_csv(file_path)
    news_data['date'] = pd.to_datetime(news_data['date'])  # Ensure 'date' is in datetime format
    return news_data

from textblob import TextBlob

# Sentiment Analysis using TextBlob
def get_sentiment_score(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Sentiment score between -1 (negative) and 1 (positive)

def aggregate_sentiment_by_date(news_data):
    news_data['Sentiment'] = news_data['headline'].apply(get_sentiment_score)
    daily_sentiment = news_data.groupby('date')['Sentiment'].mean().reset_index()  # Aggregate by date
    return daily_sentiment

def merge_stock_and_news(stock_data, daily_sentiment):
    merged_data = pd.merge(stock_data, daily_sentiment, how='left', on='date')  # Merge by 'date'
    return merged_data

def calculate_daily_returns(stock_data):
    stock_data['Daily Return'] = stock_data['Close'].pct_change() * 100  # Calculate daily percentage change
    return stock_data

def correlation_analysis(merged_data):
    merged_data = merged_data.dropna(subset=['Daily Return', 'Sentiment'])  # Drop rows with missing data
    correlation = merged_data['Daily Return'].corr(merged_data['Sentiment'])  # Pearson correlation
    return correlation

import matplotlib.pyplot as plt

def plot_sentiment_vs_stock(merged_data):
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data['date'], merged_data['Sentiment'], label='Sentiment', color='blue')
    plt.plot(merged_data['date'], merged_data['Daily Return'], label='Daily Return', color='red')
    plt.title('Sentiment vs. Stock Returns')
    plt.xlabel('Date')
    plt.ylabel('Sentiment / Daily Return (%)')
    plt.legend()
    plt.show()

def run_task_3(stock_file, news_file):
    # Load data
    stock_data = load_stock_data(stock_file)
    news_data = load_news_data(news_file)
    
    # Aggregate sentiment by date
    daily_sentiment = aggregate_sentiment_by_date(news_data)
    
    # Merge stock data with sentiment data
    merged_data = merge_stock_and_news(stock_data, daily_sentiment)
    
    # Calculate daily returns
    merged_data = calculate_daily_returns(merged_data)
    
    # Perform correlation analysis
    correlation = correlation_analysis(merged_data)
    
    # Output correlation result
    print(f'Correlation between sentiment and stock returns: {correlation}')
    
    # Plot the data for visualization
    plot_sentiment_vs_stock(merged_data)

# Example usage
if __name__ == "__main__":
    # Replace with your actual file paths
    stock_file = r'C:\Users\teble\financial-news-analysis\notebooks\yfinance_data\AAPL_historical_data.csv'  # Example stock file
    news_file = r'C:\Users\teble\financial-news-analysis\notebooks\data\news_data.csv'  # Replace with your actual news data file

    run_task_3(stock_file, news_file)

# Visualize Sentiment and Stock Returns
def plot_sentiment_vs_stock(merged_data):
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data['date'], merged_data['Sentiment'], label='Sentiment', color='blue')
    plt.plot(merged_data['date'], merged_data['Daily Return'], label='Daily Return', color='red')
    plt.title('Sentiment vs. Stock Returns')
    plt.xlabel('Date')
    plt.ylabel('Sentiment / Daily Return (%)')
    plt.legend()

    # Save the plot as a .png file
    plt.savefig('sentiment_vs_stock_returns.png')  # Save in the current working directory
    plt.close()  # Close the plot to free up memory
