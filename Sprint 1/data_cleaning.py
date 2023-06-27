import sqlite3

# connect to database
path_db = 'data.db'
cnx = sqlite3.connect(path_db)

# replace null values in multiple columns with "N/A" in the twitter_data table
query_update_twitter_data = '''
    UPDATE twitter_data 
    SET 
        id = COALESCE(id, 'N/A'),
        id_str = COALESCE(id_str, 'N/A') ,
        text = COALESCE(text, 'N/A'),
        source  = COALESCE(source, 'N/A'),
        truncated = COALESCE(truncated, 'N/A'),
        in_reply_to_status_id = COALESCE(in_reply_to_status_id, 'N/A'),
        in_reply_to_status_id_str = COALESCE(in_reply_to_status_id_str, 'N/A'),
        in_reply_to_user_id = COALESCE(in_reply_to_user_id, 'N/A'),
        in_reply_to_user_id_str = COALESCE(in_reply_to_user_id_str, 'N/A'),
        in_reply_to_screen_name = COALESCE(in_reply_to_screen_name, 'N/A'),
        user_id = COALESCE(user_id, 'N/A'),
        extended_tweet = COALESCE(extended_tweet, 'N/A'),
        entities_id = COALESCE(entities_id, 'N/A');
'''
# replace null values in multiple columns with "N/A" in the user_data table
query_update_user_data = '''
    UPDATE user_data 
    SET 
        id = COALESCE(id, 'N/A'),
        user_id = COALESCE(user_id, 'N/A'),
        user_name = COALESCE(user_name, 'N/A'),
        user_screen_name = COALESCE(user_screen_name, 'N/A'),
        user_location = COALESCE(user_location, 'N/A'),
        user_description = COALESCE(user_description, 'N/A'),
        user_verified = COALESCE(user_verified, 'N/A'),   
        set_followers_count = COALESCE(set_followers_count, 0),
        user_friends_count = COALESCE(user_friends_count, 0),
        user_statuses_count =  COALESCE(user_statuses_count, 0);
'''
# replace null values in multiple columns with "N/A" in the entities_data table
query_update_entities_data = '''
    UPDATE entities_data 
    SET 
        id = COALESCE(id, 'N/A'),
        entities_id = COALESCE(entities_id, 'N/A'),
        hashtags =  COALESCE(hashtags, 'N/A'),
        urls =  COALESCE(urls, 'N/A'),
        user_mentions = COALESCE(user_mentions, 'N/A'),
        symbols = COALESCE(symbols, 'N/A');
        
'''
# replace null values in multiple columns with "N/A" in the extended_tweets_data table
query_update_extended_tweet_data = '''
    UPDATE extended_tweet_data
    SET 
        id = COALESCE(id, 'N/A'),
        ectended_tweet_id = COALESCE(id, 'N/A'),
        full_text = COALESCE(id, 'N/A'),
        display_text_range = COALESCE(id, 'N/A'),
        quote_count = COALESCE(id, 0),
        reply_count = COALESCE(id, 0),
        retweet_count = COALESCE(id, 0),
        favourite_count = COALESCE(id, 0);
'''


# remove duplicates from the 'text' column
query_delete_duplicates = '''
    DELETE FROM twitter_data 
    WHERE ROWID NOT IN (
        SELECT MIN(ROWID) 
        FROM twitter_data 
        GROUP BY text
    )
'''

# execute update query from NULL values
cnx.execute(query_update_twitter_data)
cnx.execute(query_update_user_data)
cnx.execute(query_update_entities_data)
cnx.execute(query_update_extended_tweet_data)

# execute delete duplicates query
cnx.execute(query_delete_duplicates)

# commit changes to database
cnx.commit()

# close database connection
cnx.close()
