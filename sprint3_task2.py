import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt
from translate import Translator

translator = Translator(to_lang="en")

nltk.download('vader_lexicon')

path_lh_convo = '/Users/polinastp/Documents/uni/year1/Q4/dbl/ConversationsLufthansa.csv'
df = pd.read_csv(path_lh_convo)

# Removing null values in the tweet column
df.dropna(subset=['original_tweet'], inplace=True)

# Dropping duplicates
df = df.drop_duplicates()

df['original_tweet'] = df['original_tweet'].str.lower()


# Tranlates tweets
def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        print(str(e))
        return text


# Translate 'original_tweet' and 'thread' columns to English
df['original_tweet'] = df['original_tweet'].apply(translate_text)

# Getting sentiment
analyser = SentimentIntensityAnalyzer()

# Iterate over rows to calculate sentiment
for index, row in df.iterrows():
    if row['is_conversation'] == True:
        score = analyser.polarity_scores(row['thread'])
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        if neg > pos:
            df.loc[index, 'sentiment'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment'] = "Neutral Engagement"
    else:
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


color_palette = {
    "Positive Engagement": "green",
    "Negative Engagement": "red",
    "Neutral Engagement": "blue"
}

# Plotting sentiment analysis for conversation tweets
plt.figure(figsize=(10, 5))
sns.countplot(x='sentiment', data=df[df['is_conversation'] == True], palette=color_palette)
plt.title('Sentiment Analysis of Tweets With Conversation', size=16, weight='bold')
plt.show()

# Plotting sentiment analysis for non-conversation tweets
plt.figure(figsize=(10, 5))
sns.countplot(x='sentiment', data=df[df['is_conversation'] == False], palette=color_palette)
plt.title('Sentiment Analysis of Tweets Without Conversation', size=16, weight='bold')
plt.show()