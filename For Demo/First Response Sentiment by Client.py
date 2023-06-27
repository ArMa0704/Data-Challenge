import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def compute_sentiment(path):
    df_conversations = pd.read_json(path)

    df_conversations.loc[df_conversations['is_conversation'] == True, 'sentiment'] = df_conversations.loc[df_conversations['is_conversation'] == True, 'thread'].apply(
        lambda thread: sia.polarity_scores(thread[1])['compound'] if thread is not None and len(thread) > 1 else 0
    )

    df_conversations = df_conversations[df_conversations['is_conversation'] == True]

    df_conversations[['response_time', 'datetime_first_tweet', 'sentiment']].to_csv("conversation_analysis_first_response.csv", index=False)

compute_sentiment("../Conversations/conversations-Lufthansa2.json")
