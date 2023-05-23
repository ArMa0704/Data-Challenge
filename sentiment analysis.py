import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
nltk.download('vader_lexicon')

import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
warnings.warn("this will not show")
pd.set_option('display.max_columns', None)

df = pd.read_csv("/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full_AmericanAir-Final.csv")
df.dropna(subset=['text'], inplace=True)

rt = lambda x: re.sub("[^a-zA-Z]", ' ', str(x))
df['text'] = df['text'].map(rt)
df['text'] = df['text'].str.lower()

df[['polarity', 'subjectivity']] = df['text'].apply(lambda Text:pd.Series(TextBlob(Text).sentiment))

analyser = SentimentIntensityAnalyzer()
for index, row in df['text'].items():   # here I replaced iteritems() with items()
    score = analyser.polarity_scores(row)

    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    if neg > pos:
        df.loc[index, 'sentiment'] = "Negative Engagement"
    elif pos > neg:
        df.loc[index, 'sentiment'] = "Positive Engagement"
    else:
        df.loc[index, 'sentiment'] = "Neutral Engagement"

# Now we'll create a countplot to visualize the sentiments.
plt.figure(figsize=(10,5))
sns.countplot(x='sentiment', data=df)
plt.title('Count of Sentiments')
plt.show()

ssl._create_default_https_context = ssl.create_default_context
