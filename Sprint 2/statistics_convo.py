import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt
from translate import Translator
import re

path_luftahsa = "/Users/polinastp/Documents/uni/year1/Q4/dbl/ConversationsLufthansa.csv"
path_american = "/Users/polinastp/Documents/uni/year1/Q4/dbl/ConversationsAmericanAir.csv"

# reading csv files
df1 = pd.read_csv(path_luftahsa)
df2 = pd.read_csv(path_american)

df1_convo_count = 0
df2_convo_count = 0

# df1 = df1.dropna(subset=['number_of_tweets'], inplace=True)
# df2 = df2.dropna(subset=['number_of_tweets'], inplace=True)

for index, row in df1.iterrows():
    if row['is_conversation'] == True:
        df1_convo_count += 1


for index, row in df2.iterrows():
    if row['is_conversation'] == True:
        df2_convo_count += 1

print(df1_convo_count) # 6468
print(df2_convo_count) # 35296


stats_lufthansa = df1['number_of_tweets'].describe()
stats_american = df2['number_of_tweets'].describe()

print(stats_lufthansa)
print(stats_american)