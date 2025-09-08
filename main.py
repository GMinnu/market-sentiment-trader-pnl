import pandas as pd
import matplotlib.pyplot as plt

# Load trader data
trader_df = pd.read_csv('historical_data.csv')

# Load sentiment (fear+greed) data
sentiment_df = pd.read_csv('fear_greed_index.csv')

# Convert datetime fields to date-only
# For trader data, 'Timestamp IST' column like "02-12-2024 22:50"
trader_df['Timestamp IST'] = pd.to_datetime(trader_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
trader_df['Date'] = trader_df['Timestamp IST'].dt.date

# For sentiment data, ensure 'date' is datetime date
sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

# Select only needed columns for analysis
trader_df = trader_df[['Account', 'Execution Price', 'Size USD', 'Side', 'Date', 'Closed PnL']]
sentiment_df = sentiment_df[['date', 'classification']]

# Merge datasets on date
merged_df = pd.merge(trader_df, sentiment_df, left_on='Date', right_on='date', how='left')

# Calculate daily total PnL by sentiment type
daily_pnl = merged_df.groupby(['Date', 'classification'])['Closed PnL'].sum().reset_index()

# Calculate avg. daily PnL for each sentiment
avg_pnl_by_sentiment = daily_pnl.groupby('classification')['Closed PnL'].mean().reset_index()
print(avg_pnl_by_sentiment)

# Visualize results
plt.figure(figsize=(8,5))
plt.bar(avg_pnl_by_sentiment['classification'], avg_pnl_by_sentiment['Closed PnL'])
plt.xlabel('Market Sentiment')
plt.ylabel('Average Daily Closed PnL')
plt.title('Trader Performance vs. Bitcoin Market Sentiment')
plt.show()
