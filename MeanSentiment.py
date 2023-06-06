import nltk

import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import warnings
from langdetect import detect
from translate import Translator

all_datasets = ['ConversationsLufthansa.csv', 'ConversationsAmericanAir.csv', 'SingaporeConvo.csv',
                'EtihadConvo.csv', 'AirFranceConvo.csv', 'EasyJet.csv', 'KLMConvo.csv', 'BritishConvo.csv']
all_dataset_names = ['Lufthansa', 'AmericanAir', 'Singapore', 'Ethiad', 'AirFrance', 'EasyJet', 'KLM', 'British']

translator = Translator(to_lang = 'eng')
analyser = SentimentIntensityAnalyzer()

warnings.filterwarnings("ignore")
warnings.warn("this will not show")
pd.set_option('display.max_columns', None)


def customer_sent(dataset):

    print('[CustomerMean ' + dataset + ']')

    df = pd.read_csv(dataset)
    print('[CSV ' + dataset + ' loaded]')

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

            elif row['number_of_tweets'] == 5 or row['number_of_tweets'] == 6:
                text = thread[0] + ' ' + thread[2] + ' ' + thread[4]
                # print(text)
                score = analyser.polarity_scores(text)
                # print(score['compound'])
                total_comp_sentiment += score['compound']
            
            else:
                print('[ERROR on row: ' + str(index) + ']')
    
    mean_sentiment = total_comp_sentiment/convo_count
    return mean_sentiment



def customer_sent_progress(dataset):

    print('[CustomerProgress ' + dataset + ']')


    df = pd.read_csv(dataset)
    print('[CSV ' + dataset + ' loaded]')

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
                    change_multipliers.append(abs(score1 / score0))
                elif score0 == 0:
                    change_multipliers.append(0)

            elif row['number_of_tweets'] == 5:
                score0 = analyser.polarity_scores(text[0])['compound']
                score1 = analyser.polarity_scores(text[1])['compound']
                score2 = analyser.polarity_scores(text[2])['compound']
                change_values.append(score1 - score0)
                if score0 != 0:
                    change_multipliers.append(abs(score1 / score0))
                elif score0 == 0:
                    change_multipliers.append(0)
                change_values.append(score2 - score1)
                if score1 != 0:
                    change_multipliers.append(abs(score2 / score1))
                elif score1 == 0:
                    change_multipliers.append(0)
            
    # print(change_values)
    # print(change_multipliers)

    mean_change_values = sum(change_values) / len(change_values)
    mean_change_multipliers = sum(change_multipliers) / len(change_multipliers)

    return mean_change_values, mean_change_multipliers

def result_list():

    all_means = []
    all_values = []
    all_multipliers = []

    for set in all_datasets:
        all_means.append(round(customer_sent(dataset = set), 3))
        all_values.append(round(customer_sent_progress(dataset = set)[0], 3))
        all_multipliers.append(round(customer_sent_progress(set)[1], 3))
    
    return all_means, all_values, all_multipliers

def mean_comparison_chart(data, title):

    plt.figure(figsize = (10, 7))
    plt.title(title)
    plt.bar(all_dataset_names, data)
    plt.ylim(0, 2)
    plt.xticks(rotation = 45)
    plt.show()

# results = result_list()
results = [[0.032, 0.006, 0.084, 0.145, 0.025, 0.006, 0.034, 0.039], [0.286, 0.239, 0.281, 0.481, 0.307, 0.184, 0.137, 0.198], [1.058, 1.047, 0.906, 1.27, 0.893, 0.587, 0.652, 0.691]]
print(results)

mean_comparison_chart(results[2], 'Mean customer sentiment change multiplier by company')