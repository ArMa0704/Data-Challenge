import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data
df = pd.read_csv('../conversation_analysis.csv')

# Parse the datetime_first_tweet column into a datetime type
df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])

# Set datetime_first_tweet as the index of the dataframe
df = df.set_index('datetime_first_tweet')

# Sort the dataframe by the index
df = df.sort_index()

# Resample the dataframe by 3 days and compute the average sentiment
df_resampled = df.resample('3D').mean()

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df_resampled.index, df_resampled['sentiment'], label='Average Sentiment Over 3 Days')
plt.xlabel('Date')
plt.ylabel('Sentiment')
plt.title('Average Sentiment Over 3 Days Interval')
plt.grid(True)
plt.legend()
plt.show()
