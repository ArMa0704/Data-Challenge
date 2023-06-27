import pandas as pd

# Cleaning function
def clean_data(path):
    # these are the columns to keep
    columns_to_keep = ['id', 'id_str', 'in_reply_to_status_id_str', 'text', 'created_at', 'truncated',
                       'extended_tweet.full_text', 'user.id']

    # read the data, but only the columns in columns_to_keep
    df = pd.read_csv(path, usecols=columns_to_keep)

    # remove duplicated text
    df.drop_duplicates(subset='text', inplace=True)

    # ensure 'text' is of string type and nothing else
    df['text'] = df['text'].astype(str)

    # remove rows that have null 'text' field or are retweets
    df = df[df['text'].notna() & ~df['text'].str.contains("RT")]

    # handle truncated tweets
    df['truncated'] = df['truncated'].fillna(False)

    # remove the rows that have an invalid datetime
    df = df[pd.to_datetime(df['created_at'], errors='coerce').notna()]

    # save  cleaned data
    filename = "../cleaned_lufthansa_test"
    df.to_csv(filename, index=False)

    return df



path_lufthansa = r'C:\Users\20221063\OneDrive - TU Eindhoven\Desktop\lufthansa\Full-Lufthansa-Final.csv'
clean_data(path_lufthansa)