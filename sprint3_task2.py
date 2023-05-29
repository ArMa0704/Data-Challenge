import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')

path_lh_convo = '/Users/polinastp/Documents/uni/year1/Q4/dbl/ConversationsLufthansa.csv'
df = pd.read_csv(path_lh_convo)

# Removing null values in the tweet column
df.dropna(subset=['original_tweet'], inplace=True)

# Dropping duplicates
df = df.drop_duplicates()

df['original_tweet'] = df['original_tweet'].str.lower()

# Getting sentiment
analyser = SentimentIntensityAnalyzer()
for index, row in df['original_tweet'].items():
    score = analyser.polarity_scores(row)

    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    if neg > pos:
        df.loc[index, 'sentiment'] = "Negative Engagement"
    elif pos > neg:
        df.loc[index, 'sentiment'] = "Positive Engagement"
    else:
        df.loc[index, 'sentiment'] = "Neutral Engagement"

# Separating data based on 'is_conversation' column
df_conversation = df[df['is_conversation'] == True]
df_no_conversation = df[df['is_conversation'] == False]

# Plotting sentiment analysis for conversation tweets
plt.figure(figsize=(10, 5))
sns.countplot(x='sentiment', data=df_conversation)
plt.set_ylabel('count', fontsize=16)
plt.title('Sentiment Analysis of Tweets With Conversation', size=16, weight='bold')
# plt.savefig('sentiment_w_convo.png')
plt.show()

# Plotting sentiment analysis for non-conversation tweets
plt.figure(figsize=(10, 5))
sns.countplot(x='sentiment', data=df_no_conversation)
plt.title('Sentiment Analysis of Tweets Without Conversation',size=16, weight='bold')
# plt.savefig('sentiment_wo_convo.png')
plt.show()
