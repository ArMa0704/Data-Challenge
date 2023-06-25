import ssl
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import warnings
from langdetect import detect
from translate import Translator

translator = Translator(to_lang="en")

warnings.filterwarnings("ignore")
warnings.warn("this will not show")
pd.set_option('display.max_columns', None)

nltk.download('vader_lexicon')
analyser = SentimentIntensityAnalyzer()
df1 = pd.read_csv("data/ConversationsLufthansa.csv")
df2 = pd.read_csv("data/ConversationsAmericanAir.csv")

def month(df):
    # Convert the time strings to datetime objects
    df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])

    # Ask the user to enter a month
    month = int(input("Please enter a month (1-12): "))

    # Filter the dataframe for the specific month
    df = df[df['datetime_first_tweet'].dt.month == month]
    return df

df1=month(df1)
df2=month(df2)

def get_sentiment_difference(row):
    original_tweet_score = analyser.polarity_scores(row['original_tweet'])
    thread_score = analyser.polarity_scores(row['thread'])
    return thread_score['compound'] - original_tweet_score['compound']

def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        return text

def prepare_df(df):
    df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])
    df.dropna(subset=['original_tweet', 'thread'], inplace=True)
    df.drop_duplicates()
    df['original_tweet'] = df['original_tweet'].apply(translate_text)
    df['thread'] = df['thread'].apply(translate_text)
    rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
    df['original_tweet'] = df['original_tweet'].map(rt).str.lower()
    df['thread'] = df['thread'].map(rt).str.lower()
    df['sentiment_difference'] = df.apply(get_sentiment_difference, axis=1)
    df['date'] = pd.to_datetime(df['datetime_first_tweet'].dt.date)
    return df

df1 = prepare_df(df1)
df2 = prepare_df(df2)

def plot_line(df, title, ax, sentiment_type):
    df_temp = df[df['sentiment_difference'] > 0] if sentiment_type == 'positive' else df[df['sentiment_difference'] < 0]
    df_temp.set_index('date', inplace=True)
    df_temp = df_temp.resample('D').count()
    ax.plot(df_temp.index, df_temp['sentiment_difference'], label=title)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

plot_line(df1, "Lufthansa", ax1, 'positive')
plot_line(df2, "American Air", ax1, 'positive')
ax1.set(ylabel='Positive Difference')
ax1.legend()

plot_line(df1, "Lufthansa", ax2, 'negative')
plot_line(df2, "American Air", ax2, 'negative')
ax2.set(xlabel='Date', ylabel='Negative Difference')
# ax2.legend()

# Invert y axis for negative sentiment plot to mirror the positive sentiment plot
ax2.invert_yaxis()

plt.suptitle('Evolution of Sentiment Differences in Conversations')
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Leave space for the suptitle
plt.show()

ssl._create_default_https_context = ssl.create_default_context