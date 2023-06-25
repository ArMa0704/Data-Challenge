import pandas as pd


def build_reply_map(dataframe):
    reply_df = dataframe[dataframe['in_reply_to_status_id_str'].notna()]
    return reply_df.groupby('in_reply_to_status_id_str')['id_str'].apply(list).to_dict()


def get_conversations(dataframe, airline_id):
    dataframe['created_at'] = pd.to_datetime(dataframe['created_at'])
    dataframe = dataframe.sort_values('created_at')

    reply_map = build_reply_map(dataframe)

    # get all original tweets (not in reply to others)
    original_tweets = dataframe[dataframe['in_reply_to_status_id_str'].isna()]

    def process_row(row):
        convo = {'user_id': row['user.id'],
                 'original_tweet': row['text'],
                 'datetime_first_tweet': row['created_at'],
                 'is_conversation': False}

        if row['id_str'] in reply_map:
            replies = dataframe.loc[dataframe['id_str'].isin(reply_map[row['id_str']]), :]
            airline_replies = replies.loc[replies['user.id'] == airline_id, :]

            if not airline_replies.empty:
                convo['datetime_first_response'] = airline_replies.iat[0, dataframe.columns.get_loc('created_at')]
                convo['response_time'] = convo['datetime_first_response'] - convo['datetime_first_tweet']
                convo['is_conversation'] = True
                convo['thread'] = [row['text']] + airline_replies['text'].tolist()
                convo['number_of_tweets'] = 1 + len(airline_replies)
                convo['response_user_ids'] = [row['user.id']] + airline_replies['user.id'].tolist()

        return convo

    all_conversations = original_tweets.apply(process_row, axis=1).tolist()

    # Convert the list of dictionaries to a dataframe
    df_conversations = pd.DataFrame(all_conversations)

    # Save the dataframe to a JSON file
    df_conversations.to_json("conversations-Lufthansa2.json", orient='records', date_format='iso')



# Load cleaned data
data_path = "cleaned/cleaned_lufthansa"
dataframe = pd.read_csv(data_path)
dataframe['id'] = dataframe['id'].astype(str)

# Extract conversations
airline_id = 124476322
get_conversations(dataframe, airline_id)
