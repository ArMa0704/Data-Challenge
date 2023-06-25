import ssl
import nltk

nltk.download('vader_lexicon')
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

df = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/dataset/ConversationsLufthansa.csv")

# Convert the time strings to datetime objects
df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])

# Ask the user to enter a month
month = int(input("Please enter a month (1-12): "))

# Filter the dataframe for the specific month
df = df[df['datetime_first_tweet'].dt.month == month]

print(df.info())

# Drops null tweets and duplicates
df.dropna(subset=['original_tweet'], inplace=True)
df.drop_duplicates()


# Tranlates tweets
def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        # print(str(e))
        return text


# Translate 'original_tweet' and 'thread' columns to English
df['original_tweet'] = df['original_tweet'].apply(translate_text)
df['thread'] = df['thread'].apply(translate_text)

# Breaks tweets into single words using regular expression
rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
df['original_tweet'] = df['original_tweet'].map(rt)
df['original_tweet'] = df['original_tweet'].str.lower()
df['thread'] = df['thread'].map(rt)
df['thread'] = df['thread'].str.lower()

# Calling the sentiment analyzer
analyser = SentimentIntensityAnalyzer()
df['sentiment'] = np.nan
df['sentiment_2'] = np.nan  # NUMBER OF TWEET=2 MEANS IT HAS 1 REPLY!!!
df['sentiment_3'] = np.nan
df['sentiment_4'] = np.nan
df['sentiment_5'] = np.nan

for index, row in df.iterrows():

    if row['number_of_tweets'] == 2:
        # Concatenating 'original_tweet' and 'thread' and analyzing
        combined_text = row['original_tweet'] + ' ' + row['thread']
        score = analyser.polarity_scores(combined_text)
        neg = score['neg']
        pos = score['pos']

        if neg > pos:
            df.loc[index, 'sentiment_2'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment_2'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment_2'] = "Neutral Engagement"

    elif row['number_of_tweets'] == 3:
        # Concatenating 'original_tweet' and 'thread' and analyzing
        combined_text = row['original_tweet'] + ' ' + row['thread']
        score = analyser.polarity_scores(combined_text)
        neg = score['neg']
        pos = score['pos']

        if neg > pos:
            df.loc[index, 'sentiment_3'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment_3'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment_3'] = "Neutral Engagement"

    elif row['number_of_tweets'] == 4:
        # Concatenating 'original_tweet' and 'thread' and analyzing
        combined_text = row['original_tweet'] + ' ' + row['thread']
        score = analyser.polarity_scores(combined_text)
        neg = score['neg']
        pos = score['pos']

        if neg > pos:
            df.loc[index, 'sentiment_4'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment_4'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment_4'] = "Neutral Engagement"

    elif row['number_of_tweets'] == 5:
        # Concatenating 'original_tweet' and 'thread' and analyzing
        combined_text = row['original_tweet'] + ' ' + row['thread']
        score = analyser.polarity_scores(combined_text)
        neg = score['neg']
        pos = score['pos']

        if neg > pos:
            df.loc[index, 'sentiment_5'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment_5'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment_5'] = "Neutral Engagement"

    else:  # no replies
        score = analyser.polarity_scores(row['original_tweet'])

        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        if neg > pos:
            df.loc[index, 'sentiment'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment'] = "Neutral Engagement"


# Regular expressions for flight related issues
flight_related_re = re.compile(r'\bdelay|\bcancel|\blate|\bearly|\breschedule', re.IGNORECASE)

def is_flight_related(text):
    if flight_related_re.search(text):
        return True
    return False

df['flight_related'] = df['original_tweet'].apply(is_flight_related)

def plot_bar_flight_related(column, title, flight_related):
    if df[df['flight_related'] == flight_related][column].notnull().any():
        sentiment_counts = df[df['flight_related'] == flight_related][column].value_counts()

        colors = {
            'Positive Engagement': 'green',
            'Negative Engagement': 'red',
            'Neutral Engagement': 'gray'
        }

        sentiment_colors = [colors.get(sentiment, 'yellow') for sentiment in sentiment_counts.index]

        plt.figure(figsize=(20, 10))
        sentiment_counts.plot.bar(color=sentiment_colors)
        plt.title(title, fontsize=24)
        plt.ylabel('Count', fontsize=24)
        plt.xlabel('Sentiment', fontsize=24)
        plt.xticks(rotation=0)
        plt.show()
    else:
        print(f"No data to plot for {title}")

plot_bar_flight_related('sentiment', 'Sentiments for flight-related Conversations without replies', True)
plot_bar_flight_related('sentiment_2', 'Sentiments for flight-related Conversations with reply count 1', True)
plot_bar_flight_related('sentiment_3', 'Sentiments for flight-related Conversations with reply count 2', True)
plot_bar_flight_related('sentiment_4', 'Sentiments for flight-related Conversations with reply count 3', True)
plot_bar_flight_related('sentiment_5', 'Sentiments for flight-related Conversations with reply count 4', True)

ssl._create_default_https_context = ssl.create_default_context
