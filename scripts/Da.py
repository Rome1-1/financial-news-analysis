import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load the dataset
try:
    news_data = pd.read_csv('C:/Users/teble/financial-news-analysis/notebooks/raw_analyst_ratings.csv')  # Adjust path if necessary
    logging.info("Dataset successfully loaded!")
except FileNotFoundError:
    logging.error("The file 'raw_analyst_ratings.csv' was not found. Check the file path.")
    exit()

# Check if essential columns exist
if 'publisher' not in news_data.columns or 'headline' not in news_data.columns or 'date' not in news_data.columns:
    logging.error("The dataset must contain 'publisher', 'headline', and 'date' columns.")
    exit()

# Handle missing values
if news_data['publisher'].isnull().any():
    logging.warning("Some articles are missing publisher information.")
    news_data['publisher'].fillna('Unknown', inplace=True)

if news_data['headline'].isnull().any():
    logging.warning("Some articles are missing headlines. Removing these rows.")
    news_data = news_data[news_data['headline'].notnull()]

# Normalize publisher names
news_data['publisher'] = news_data['publisher'].str.strip().str.lower()

# Optimize memory usage
logging.info("Optimizing memory usage...")
for col in news_data.select_dtypes(include=['int', 'float']):
    news_data[col] = pd.to_numeric(news_data[col], downcast='unsigned')

for col in news_data.select_dtypes(include=['object']):
    if news_data[col].nunique() / len(news_data[col]) < 0.5:
        news_data[col] = news_data[col].astype('category')

# Descriptive Statistics
# Headline Length Analysis
news_data['headline'] = news_data['headline'].astype(str)  # Ensure all headlines are strings
news_data['headline_length'] = news_data['headline'].str.len()
logging.info("Descriptive Statistics for Headline Lengths:")
logging.info(news_data['headline_length'].describe())

# Publisher Activity
article_counts = news_data['publisher'].value_counts()
logging.info("Articles per Publisher:")
logging.info(article_counts)

# Visualize Publisher Activity
plt.figure(figsize=(10, 6))
top_publishers = article_counts.head(10)
top_publishers.plot(kind='bar', title='Top 10 Publishers by Article Count')
plt.xlabel('Publisher')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Publication Date Parsing and Handling
news_data['date'] = pd.to_datetime(news_data['date'], errors='coerce')

# Log rows with invalid dates
invalid_dates = news_data[news_data['date'].isnull()]
logging.warning(f"Rows with invalid dates: {len(invalid_dates)}")

# Drop rows with invalid dates
if invalid_dates.shape[0] > 0:
    logging.warning("Dropping rows with invalid dates.")
    news_data = news_data[news_data['date'].notnull()]

# Publication Trends Over Time
publication_trends = news_data['date'].dt.date.value_counts().sort_index()
logging.info("Publication Trends Over Time:")
logging.info(publication_trends)

# Plot publication frequency over time
publication_trends.plot(kind='line', title='Publication Trends Over Time', figsize=(10, 6))
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.show()

# Sentiment Analysis
news_data['sentiment'] = news_data['headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
news_data['sentiment_label'] = news_data['sentiment'].apply(
    lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral'
)

logging.info("Sentiment Analysis Results:")
logging.info(news_data['sentiment_label'].value_counts())

# Visualize sentiment distribution
news_data['sentiment_label'].value_counts().plot(kind='bar', title='Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.show()

# Topic Modeling (Common Keywords)
vectorizer = CountVectorizer(max_features=10, stop_words='english')
X = vectorizer.fit_transform(news_data['headline'].dropna())
logging.info("Top Keywords:")
logging.info(vectorizer.get_feature_names_out())

# Publisher Analysis (Extracting domains if applicable)
news_data['publisher_domain'] = news_data['publisher'].str.extract(r'@([a-zA-Z0-9.-]+)')[0]
logging.info("Publisher Domains:")
logging.info(news_data['publisher_domain'].value_counts())

# Save publisher counts to CSV (optional)
try:
    article_counts.to_csv('articles_per_publisher.csv', header=True)
    logging.info("Article counts saved to 'articles_per_publisher.csv'.")
except Exception as e:
    logging.error(f"Error saving to CSV: {e}")
