# import ssl
# import nltk
#
# nltk.download('vader_lexicon')
# import numpy as np
# import pandas as pd
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import re
# import matplotlib.pyplot as plt
# import warnings
# from langdetect import detect
# from translate import Translator
#
# translator = Translator(to_lang="en")
#
# warnings.filterwarnings("ignore")
# warnings.warn("this will not show")
# pd.set_option('display.max_columns', None)
#
# # Loading the first dataset
# df1 = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/dataset/ConversationsLufthansa.csv")
#
# # Loading the second dataset, adjust this path to your second csv file
# df2 = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/dataset/ConversationsAmericanAir.csv")
#
# def translate_text(text):
#     try:
#         return translator.translate(text)
#     except Exception as e:
#         return text
#
# def prepare_df(df):
#     # Convert the time strings to datetime objects
#     df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])
#
#     # Drops null tweets and duplicates
#     df.dropna(subset=['original_tweet'], inplace=True)
#     df.drop_duplicates()
#
#     # Translate 'original_tweet' and 'thread' columns to English
#     df['original_tweet'] = df['original_tweet'].apply(translate_text)
#     df['thread'] = df['thread'].apply(translate_text)
#
#     # Breaks tweets into single words using regular expression
#     rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
#     df['original_tweet'] = df['original_tweet'].map(rt)
#     df['original_tweet'] = df['original_tweet'].str.lower()
#     df['thread'] = df['thread'].map(rt)
#     df['thread'] = df['thread'].str.lower()
#
#     return df
#
# df1 = prepare_df(df1)
# df2 = prepare_df(df2)
#
# # Calling the sentiment analyzer
# analyser = SentimentIntensityAnalyzer()
#
# def get_sentiment(row):
#     score = analyser.polarity_scores(row['original_tweet'])
#     neg = score['neg']
#     pos = score['pos']
#
#     if neg > pos:
#         return "Negative Engagement"
#     elif pos > neg:
#         return "Positive Engagement"
#     else:
#         return "Neutral Engagement"
#
# df1['sentiment'] = df1.apply(get_sentiment, axis=1)
# df2['sentiment'] = df2.apply(get_sentiment, axis=1)
#
# def plot_line(df, title):
#     df['Date'] = pd.to_datetime(df['datetime_first_tweet'].dt.date)
#     df = df[df['sentiment'] == 'Positive Engagement']
#     df.set_index('Date', inplace=True)  # Set 'Date' as the DataFrame's index
#     df = df.resample('D').count()  # Resample the DataFrame by day and count the occurrences
#     plt.plot(df.index, df['sentiment'], label=title)  # Use 'sentiment' column for y-values
#
#
# plt.figure(figsize=(12, 8))
# plot_line(df1, "Lufthansa")
# plot_line(df2, "American Air")
# plt.title('Change in Positive Conversations Over Time')
# plt.xlabel('Date')
# plt.ylabel('Conversations with Positive Sentiment')
# plt.legend()
# plt.show()
#
#
# ssl._create_default_https_context = ssl.create_default_context
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
df1 = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/dataset/ConversationsLufthansa.csv")
df2 = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/dataset/ConversationsAmericanAir.csv")

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
ax2.legend()

# Invert y axis for negative sentiment plot to mirror the positive sentiment plot
ax2.invert_yaxis()

plt.suptitle('Evolution of Sentiment Differences in Conversations')
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Leave space for the suptitle
plt.show()

ssl._create_default_https_context = ssl.create_default_context



