import pandas as pd
import matplotlib.pyplot as plt
import isodate

def convert_to_minutes(duration):
    return isodate.parse_duration(duration).total_seconds() / 60

df = pd.read_csv('conversation_analysis_first_response.csv')

df['response_time_minutes'] = df['response_time'].apply(convert_to_minutes)

df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])

df = df[(df['datetime_first_tweet'] >= '2020-03-01') & (df['response_time_minutes'] >= 100)]

plt.figure(figsize=(12,6))

plt.scatter(df['response_time_minutes'], df['sentiment'], edgecolors='r')

# Bold and larger font size for labels and title
plt.xlabel('Response Time (Minutes)', fontsize=14, weight='bold')
plt.ylabel('Sentiment', fontsize=14, weight='bold')
plt.title('Lufthansa Response Time vs Sentiment During Covid (March 2020 and onwards)', fontsize=16, weight='bold')

plt.grid(True)
plt.show()
