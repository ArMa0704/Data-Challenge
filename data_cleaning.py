import sqlite3

# connect to database
path_db = 'data.db'
cnx = sqlite3.connect(path_db)

# replace null values in multiple columns with "N/A"
query_update = '''
    UPDATE twitter_data 
    SET 
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
        entities = COALESCE(entities, 'N/A');
        
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

# execute update query
cnx.execute(query_update)

# execute delete duplicates query
cnx.execute(query_delete_duplicates)

# commit changes to database
cnx.commit()

# close database connection
cnx.close()
