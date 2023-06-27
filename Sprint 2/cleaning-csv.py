import pandas as pd

# Cleaning function
def clean_data(path):
    columns_to_keep = ['id', 'id_str', 'in_reply_to_status_id_str', 'text', 'created_at', 'truncated',
                       'extended_tweet.full_text', 'user.id']

    df = pd.read_csv(path, usecols=columns_to_keep)

    # Remove Duplicate
    df.drop_duplicates(subset='text', inplace=True)

    df['text'] = df['text'].astype(str)

    df = df[df['text'].notna() & ~df['text'].str.contains("RT")]

    df['truncated'] = df['truncated'].fillna(False)

    # Replace 'text' with 'extended_tweet.full_text' when 'truncated' is True
    df.loc[df['truncated'] == True, 'text'] = df['extended_tweet.full_text']

    df = df[pd.to_datetime(df['created_at'], errors='coerce').notna()]

    filename = "../cleaned/cleaned_lufthansa"
    df.to_csv(filename, index=False)

    return df



path = r"C:\Users\danie\Downloads\all-data\Final CSV\Full-Lufthansa-Final (1).csv"
clean_data(path)
