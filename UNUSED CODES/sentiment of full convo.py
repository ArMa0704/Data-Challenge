import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

def compute_sentiment(path):
    # Load the data
    df_conversations = pd.read_json(path)

    # Compute the sentiment of each conversation where 'is_conversation' is True
    df_conversations.loc[df_conversations['is_conversation'] == True, 'sentiment'] = df_conversations.loc[df_conversations['is_conversation'] == True, 'thread'].apply(
        lambda thread: sum(sia.polarity_scores(tweet)['compound'] for tweet in thread) / len(thread) if thread is not None else 0
    )

    # Filter out conversations where 'is_conversation' is False
    df_conversations = df_conversations[df_conversations['is_conversation'] == True]

    # Save the dataframe to a CSV file with response_time, datetime_first_tweet, and sentiment
    df_conversations[['response_time', 'datetime_first_tweet', 'sentiment']].to_csv("conversation_analysis.csv", index=False)

# Call the function with the path as the argument
compute_sentiment("conversations-Lufthansa2.json")
