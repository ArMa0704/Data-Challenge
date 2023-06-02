import spacy
from langdetect import detect
from spacytextblob.spacytextblob import SpacyTextBlob
from translate import Translator
import ssl
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import warnings
from langdetect import detect
from textblob import TextBlob
import seaborn as sns

translator = Translator(to_lang="en")
df = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/ConversationsAmericanAir.csv")
print(df.info())

df['language'] = np.nan

#Detect Language
for i in range(len(df.index)):
    try:
        if df['original_tweet'][i].strip():  # check if text is not empty or whitespace
            lang = detect(df['original_tweet'][i])
            df.loc[i, 'language'] = lang
        else:
            df.loc[i, 'language'] = 'unknown'
    except Exception as e:
        print(f"Error at index {i}: {e}")
        df.loc[i, 'language'] = 'unknown'

# Tranlates tweets
def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        print(str(e))
        return text


# Translate 'original_tweet' and 'thread' columns to English
df['original_tweet'] = df['original_tweet'].apply(translate_text)

# Breaks tweets into single words using regular expression
rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
df['original_tweet'] = df['original_tweet'].map(rt)
df['original_tweet'] = df['original_tweet'].str.lower()

#Sentiment Analysis
df['sentiment'] = np.nan

analyser = SentimentIntensityAnalyzer()
for index, row in df.iterrows():
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

# Create a color mapping for each sentiment
color_dict = {"Positive Engagement": "green", "Negative Engagement": "red", "Neutral Engagement": "blue"}

# Loop over each language
for lang, lang_full in [('en', 'English'), ('de', 'German'), ('es', 'Spanish')]:
    # Filter dataframe for the current language
    df_lang = df[df['language'] == lang]

    # Create a countplot to visualize the sentiments.
    plt.figure(figsize=(10, 5))
    sns.countplot(x='sentiment', data=df_lang, palette=color_dict)
    plt.title(f'Count of Sentiments for {lang_full}')
    plt.show()