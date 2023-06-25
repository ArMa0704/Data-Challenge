import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("conversation_analysis_first_response.csv")

df['response_time'] = df['response_time'].apply(lambda x: pd.to_timedelta(x).total_seconds()/60)

df = df[(df['response_time'] > 1) & (df['response_time'] <= 1000)]

plt.figure(figsize=(12,8))
plt.scatter(df['response_time'], df['sentiment'], alpha=0.5)

plt.xlabel('Response Time (minutes)', fontsize=13, fontweight='bold')
plt.ylabel('Client Conversation Sentiment', fontsize=13, fontweight='bold')
plt.title('Lufthansa - Response Time vs Sentiment', fontsize=20, fontweight='bold')
plt.xlim(0, 100)

plt.show()
