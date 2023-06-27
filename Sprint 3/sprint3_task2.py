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

# Removing null values in the tweet column
df.dropna(subset=['original_tweet'], inplace=True)

# Dropping duplicates
df = df.drop_duplicates()

df['original_tweet'] = df['original_tweet'].str.lower()
df['thread'] = df['thread'].str.lower()

# sprint 3 part 2 - 1st question

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

# # Plotting sentiment analysis for conversation tweets
# plt.figure(figsize=(10, 5))
# sns.countplot(x='sentiment', data=df[df['is_conversation'] == True], palette=color_palette)
# plt.title('Sentiment Analysis of Tweets With Conversation', size=16, weight='bold')
# plt.show()
#
# # Plotting sentiment analysis for non-conversation tweets
# plt.figure(figsize=(10, 5))
# sns.countplot(x='sentiment', data=df[df['is_conversation'] == False], palette=color_palette)
# plt.title('Sentiment Analysis of Tweets Without Conversation', size=16, weight='bold')
# plt.show()
#

# sprint 3 part 2 - 2nd question


sorry_pattern = r'\bsorry\b'

sorry_count_neg = 0
sorry_count_neu = 0
sorry_count_pos = 0

for index, row in df.iterrows():
    if row['is_conversation'] == True:
        thread_text = str(row['thread'])  # Convert to string
        sorry_match = re.findall(sorry_pattern, thread_text, re.IGNORECASE)

        if sorry_match:
            if row['sentiment'] == 'Negative Engagement':
                sorry_count_neg += 1
            elif row['sentiment'] == 'Neutral Engagement':
                sorry_count_neu += 1
            elif row['sentiment'] == 'Positive Engagement':
                sorry_count_pos += 1


sentiments = ['Negative Engagement', 'Neutral Engagement', 'Positive Engagement']
sorry_counts = [sorry_count_neg, sorry_count_neu, sorry_count_pos]

# plt.figure(figsize=(10, 5))
# plt.bar(sentiments, sorry_counts, color='blue')
# plt.xlabel('Sentiment', size=10, weight='bold')
# plt.ylabel('Amount of messages that include word "Sorry" ', size=10, weight='bold')
# plt.title('Amount of messages that include word "Sorry" per sentiment in Lufthansa conversations', size=12, weight='bold')
# plt.show()
# Iterate over rows to calculate sentiment
for index, row in df.iterrows():
    if row['is_conversation'] == True:
        score = analyser.polarity_scores(row['thread'])
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        if neg > pos:
            df.loc[index, 'sentiment_thread'] = "Negative Engagement"
        elif pos > neg:
            df.loc[index, 'sentiment_thread'] = "Positive Engagement"
        else:
            df.loc[index, 'sentiment_thread'] = "Neutral Engagement"

        if 'sorry' in row['thread']:
            score = analyser.polarity_scores(row['original_tweet'])
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            if neg > pos:
                df.loc[index, 'sentiment_original_tweet'] = "Negative Engagement"
            elif pos > neg:
                df.loc[index, 'sentiment_original_tweet'] = "Positive Engagement"
            else:
                df.loc[index, 'sentiment_original_tweet'] = "Neutral Engagement"

# Calculate percentages for sentiment of original tweet when the thread contains the word 'sorry'
original_tweet_sentiments = df[df['sentiment_original_tweet'].notna()]['sentiment_original_tweet'].value_counts(normalize=True) * 100

# Calculate percentages for sentiment based on the thread
thread_sentiments = df[df['sentiment_thread'].notna()]['sentiment_thread'].value_counts(normalize=True) * 100

# Pie chart for sentiment of original tweet when the thread contains the word 'sorry'
plt.figure(figsize=(8, 6))
plt.pie(original_tweet_sentiments, labels=original_tweet_sentiments.index, autopct='%1.1f%%', colors=['red', 'grey', 'green'])
plt.title('Sentiment of Original Tweet when Thread Contains "Sorry"', size=16, weight='bold')
plt.show()

# Pie chart for sentiment based on the thread
plt.figure(figsize=(8, 6))
plt.pie(thread_sentiments, labels=thread_sentiments.index, autopct='%1.1f%%', colors=['green', 'red', 'grey'])
plt.title('Sentiment Based on Thread after reply with a "Sorry"', size=16, weight='bold')
plt.show()