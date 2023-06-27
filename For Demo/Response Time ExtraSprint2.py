import pandas as pd
import matplotlib.pyplot as plt
import isodate


def convert_to_minutes(duration):
    return isodate.parse_duration(duration).total_seconds() / 60


df1 = pd.read_json(
    r"C:\Users\danie\OneDrive\Documents\GitHub\Data-Challenge\Conversations\conversations-Lufthansa2.json")
df1 = df1.dropna(subset=['response_time', 'datetime_first_tweet'])
df1['datetime_first_tweet'] = pd.to_datetime(df1['datetime_first_tweet'])
df1['response_time_minutes'] = df1['response_time'].apply(convert_to_minutes)
df1.set_index('datetime_first_tweet', inplace=True)
weekly_avg_response_time1 = df1['response_time_minutes'].resample('W').mean()

df2 = pd.read_csv(r'C:\Users\danie\Downloads\ConversationsAmericanAir.csv')
df2 = df2.dropna(subset=['response_time', 'datetime_first_tweet'])
df2['datetime_first_tweet'] = pd.to_datetime(df2['datetime_first_tweet'])
df2['response_time_minutes'] = df2['response_time'].apply(convert_to_minutes)
df2.set_index('datetime_first_tweet', inplace=True)
weekly_avg_response_time2 = df2['response_time_minutes'].resample('W').mean()

plt.figure(figsize=(12, 6))

plt.plot(weekly_avg_response_time1, marker='o', linestyle='-', label='Lufthansa')

plt.plot(weekly_avg_response_time2, marker='o', linestyle='-', label='AmericanAir')

plt.xlabel('Week', fontsize=14, weight='bold')
plt.ylabel('Average Response Time (Minutes)', fontsize=14, weight='bold')
plt.title('Average Response Time Over Time', fontsize=16, weight='bold')

plt.legend(prop={'size': 12, 'weight': 'bold'})
# plt.xlim([pd.to_datetime('2019-12-01'), pd.to_datetime('2020-03-31')])

plt.grid(True)
plt.show()
