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


def plot_pie(column, title):
    # Check if the column contains any non-null values
    if df[column].notnull().any():
        # Count the occurrences of each sentiment
        sentiment_counts = df[column].value_counts()

        # Define colors for each sentiment
        colors = {
            'Positive Engagement': 'green',
            'Negative Engagement': 'red',
            'Neutral Engagement': 'gray'
        }

        # Map the colors to the sentiment counts
        sentiment_colors = [colors.get(sentiment, 'yellow') for sentiment in sentiment_counts.index]

        # Plot the pie chart
        plt.figure(figsize=(10, 5))
        sentiment_counts.plot.pie(autopct='%1.1f%%', colors=sentiment_colors)
        plt.title(title)
        plt.ylabel('')  # Hide the 'None' ylabel
        plt.show()
    else:
        print(f"No data to plot for {title}")



plot_pie('sentiment', 'Percentage of Sentiments for tweets without replies')
# plot_pie('sentiment_1', 'Percentage of Sentiments for tweets with reply count 1')
plot_pie('sentiment_2', 'Percentage of Sentiments for tweets with reply count 1')
plot_pie('sentiment_3', 'Percentage of Sentiments for tweets with reply count 2')
plot_pie('sentiment_4', 'Percentage of Sentiments for tweets with reply count 3')
plot_pie('sentiment_5', 'Percentage of Sentiments for tweets with reply count 4')

ssl._create_default_https_context = ssl.create_default_context
