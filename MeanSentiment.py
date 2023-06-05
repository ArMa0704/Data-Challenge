import nltk

import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import warnings
from langdetect import detect
from translate import Translator

translator = Translator(to_lang = 'eng')
analyser = SentimentIntensityAnalyzer()

warnings.filterwarnings("ignore")
warnings.warn("this will not show")
pd.set_option('display.max_columns', None)

dataset = "ConversationsLufthansa.csv"
df = pd.read_csv(dataset)
print('[CSV ' + "ConversationsLufthansa.csv" + ' loaded]')

# Drops null tweets and duplicates
df.dropna(subset=['original_tweet'], inplace=True)
df.drop_duplicates()
print('[Dupes dropped]')

# Counting the number of conversations in the dataset
convo_count = 0
for index, row in df.iterrows():
    if row['is_conversation'] == False:
        continue
    elif row['is_conversation'] == True:
        convo_count += 1
print('[Convos Counted: ' + str(convo_count) + ']')

# Tranlates tweets
def translate_text(text):
    try:
        return translator.translate(text)
    except Exception as e:
        print(str(e))
        return text

# # Translate 'original_tweet' and 'thread' columns to English
# for row in df['thread']:
#     df['thread'] = translate_text(text = df['thread'])
# print('[Threads translated]')
# df['thread'] = df['thread'].apply(translate_text)
# print('[Translated]')

def customer_sent():

    # Breaks tweets into single words using regular expression
    # rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
    # df['original_tweet'] = df['original_tweet'].map(rt)
    # df['original_tweet'] = df['original_tweet'].str.lower()
    # df['thread'] = df['thread'].map(rt)
    # df['thread'] = df['thread'].str.lower()
    # print(df['original_tweet'])

    # Sentiment object

    global total_comp_sentiment
    total_comp_sentiment = 0

    for index, row in df.iterrows():

        if row['is_conversation'] == False:
            # print('[Not a Convo]')
            continue
        
        elif row['is_conversation'] == True:

            # print('Unformatted thread: ' + row['thread'])
            thread = row['thread'].strip('"]["').split('","')
            # print('List form: ' + str(thread))

            if row['number_of_tweets'] == 1 or row['number_of_tweets'] == 2:
                text = thread[0]
                # print(text)
                score = analyser.polarity_scores(text)
                # print(score['compound'])
                total_comp_sentiment += score['compound']

            elif row['number_of_tweets'] == 3 or row['number_of_tweets'] == 4:
                text = thread[0] + ' ' + thread[2]
                # print(text)
                score = analyser.polarity_scores(text)
                # print(score['compound'])
                total_comp_sentiment += score['compound']

            elif row['number_of_tweets'] == 5:
                text = thread[0] + ' ' + thread[2] + ' ' + thread[4]
                # print(text)
                score = analyser.polarity_scores(text)
                # print(score['compound'])
                total_comp_sentiment += score['compound']
            
            else:
                print('[ERROR on row: ' + str(index) + ']')
    
    mean_sentiment = total_comp_sentiment/convo_count
    return mean_sentiment



def customer_sent_progress():

    change_values = []
    change_multipliers = []

    for index, row in df.iterrows():

        if row['is_conversation'] == False:
            # print('[Not a Convo]')
            continue

        elif row['is_conversation'] == True:

            text = row['thread'].strip('"]["').split('","')

            if row['number_of_tweets'] == 3 or row['number_of_tweets'] == 4:
                score0 = analyser.polarity_scores(text[0])['compound']
                score1 = analyser.polarity_scores(text[2])['compound']
                change_values.append(score1 - score0)
                if score0 != 0:
                    change_multipliers.append(score1 / score0)
                elif score0 == 0:
                    change_multipliers.append(0)

            elif row['number_of_tweets'] == 5:
                score0 = analyser.polarity_scores(text[0])['compound']
                score1 = analyser.polarity_scores(text[1])['compound']
                score2 = analyser.polarity_scores(text[2])['compound']
                change_values.append(score1 - score0)
                if score0 != 0:
                    change_multipliers.append(score1 / score0)
                elif score0 == 0:
                    change_multipliers.append(0)
                change_values.append(score2 - score1)
                if score1 != 0:
                    change_multipliers.append(score2 / score1)
                elif score1 == 0:
                    change_multipliers.append(0)
            
    # print(change_values)
    # print(change_multipliers)

    mean_change_values = sum(change_values) / len(change_values)
    mean_change_multipliers = sum(change_multipliers) / len(change_multipliers)

    return mean_change_values, mean_change_multipliers

print('Mean sentiment of the customer for ' + dataset + ' =', round(customer_sent(), 4))
print('Mean change value for ' + dataset + ' =', round(customer_sent_progress()[0], 4))
print('Mean value multiplier for ' + dataset + ' =', round(customer_sent_progress()[1], 4))