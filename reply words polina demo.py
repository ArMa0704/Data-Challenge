import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt
from translate import Translator
import re

translator = Translator(to_lang="en")

nltk.download('vader_lexicon')

path_lh_convo = '/Users/polinastp/Documents/uni/year1/Q4/dbl/ConversationsLufthansa.csv'
df = pd.read_csv(path_lh_convo)

# # Convert the time strings to datetime objects
# df['datetime_first_tweet'] = pd.to_datetime(df['datetime_first_tweet'])
#
# # Ask the user to enter a month
# month = int(input("Please enter a month (1-12): "))
#
# # Filter the dataframe for the specific month
# df = df[df['datetime_first_tweet'].dt.month == month]

# Check if there is data available for the selected month
if df.empty:
    print("No data available for the selected month.")
else:
    # Removing null values in the tweet column
    df.dropna(subset=['original_tweet'], inplace=True)

    # Dropping duplicates
    df = df.drop_duplicates()

    df['original_tweet'] = df['original_tweet'].str.lower()
    df['thread'] = df['thread'].str.lower()
    df['thread'] = df['thread'].fillna('')

    # Translates tweets
    def translate_text(text):
        try:
            return translator.translate(text)
        except Exception as e:
            print(str(e))
            return text

    # Translate 'original_tweet' and 'thread' columns to English
    df['original_tweet'] = df['original_tweet'].apply(translate_text)
    df['thread'] = df['thread'].apply(translate_text)  # Translate thread to English

    # Getting sentiment
    analyser = SentimentIntensityAnalyzer()

    keywords = ['sorry', 'sorry to hear', 'apologies', 'please']

    for keyword in keywords:
        df['sentiment_' + keyword.replace(' ', '_')] = None

    # Iterate over rows to calculate sentiment
    for index, row in df.iterrows():
        for keyword in keywords:
            if keyword in row['thread']:
                score = analyser.polarity_scores(row['thread'])
                neg = score['neg']
                neu = score['neu']
                pos = score['pos']
                if neg > pos:
                    df.loc[index, 'sentiment_' + keyword.replace(' ', '_')] = "Negative Engagement"
                elif pos > neg:
                    df.loc[index, 'sentiment_' + keyword.replace(' ', '_')] = "Positive Engagement"
                else:
                    df.loc[index, 'sentiment_' + keyword.replace(' ', '_')] = "Neutral Engagement"

    # Plotting sentiment analysis for each keyword
    color_palette = {"Positive Engagement": "green", "Negative Engagement": "red", "Neutral Engagement": "grey"}

    for keyword in keywords:
        # Calculate percentages for sentiment of thread when it contains the keyword
        thread_sentiments = df[df['sentiment_' + keyword.replace(' ', '_')].notna()]['sentiment_' + keyword.replace(' ', '_')].value_counts(normalize=True) * 100

        # Pie chart for sentiment based on the thread
        plt.figure(figsize=(8, 6))
        plt.pie(thread_sentiments, labels=thread_sentiments.index, autopct='%1.1f%%', colors=[color_palette[sentiment] for sentiment in thread_sentiments.index])
        plt.title(f'Sentiment after Lufthansa replies with "{keyword}"', size=16, weight='bold')
        plt.show()
