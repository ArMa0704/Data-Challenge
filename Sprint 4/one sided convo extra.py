import pandas as pd
import ssl
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
from langdetect import detect
from translate import Translator

translator = Translator(to_lang="en")

pd.set_option('display.max_columns', None)

# nltk.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()

df = pd.read_csv("data/lufthansa addeduser id.csv")

# Convert the time strings to datetime objects
df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])

# Ask the user to enter a month
month = int(input("Please enter a month (1-12): "))

# Filter the dataframe for the specific month
df = df[df['datetime_first_tweet'].dt.month == month]

def get_sentiment(row):
    original_tweet_score = analyser.polarity_scores(row['original_tweet'])
    return original_tweet_score['compound']

def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        return text

def prepare_df(df_x):
    df_x['datetime_first_tweet'] = pd.to_datetime(df_x['datetime_first_tweet'])
    df_x.dropna(subset=['original_tweet'], inplace=True)
    df_x.drop_duplicates(inplace=True)
    rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
    df_x['original_tweet'] = df_x['original_tweet'].map(rt).str.lower()
    df['original_tweet'] = df['original_tweet'].apply(translate_text)
    df_x['sentiment'] = df_x.apply(get_sentiment, axis=1)
    df_x['date'] = pd.to_datetime(df_x['datetime_first_tweet'].dt.date)
    return df_x

df = prepare_df(df)

# Remove users with more than 15 original_tweet entries
df = df.groupby('user_id').filter(lambda x: len(x) <= 15)

# Get the 10 users with the most tweets
top_users = df['user_id'].value_counts().head(10).index

# plot superimposed sentiment scores
for user_id, group in df[df['user_id'].isin(top_users)].groupby('user_id'):
    group = group.reset_index(drop=True)  # reset the index for each group
    plt.plot(group.index, group['sentiment'], label=user_id, alpha=0.5, linewidth=2)

plt.xlabel('Index of the Tweet')
plt.ylabel('Sentiment Score')
plt.title('Sentiment Scores by Tweet Index for Users')
plt.ylim(-1, 1)  # set the y-axis from -1 to 1
plt.xlim(0,10)
plt.show()
