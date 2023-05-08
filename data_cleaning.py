import sqlite3

# connect to database
path_db = 'data.db'
cnx = sqlite3.connect(path_db)

# replace null values in multiple columns with "N/A"
query_update = '''
    UPDATE twitter_data 
    SET created_at = COALESCE(created_at, 'N/A'),
        id = COALESCE(id, 'N/A'),
        id_str = COALESCE(id_str, 'N/A'),
        text = COALESCE(text, 'N/A'),
        source = COALESCE(source, 'N/A'),
        truncated = COALESCE(source, 'N/A'),
        user_id = COALESCE(user_id, 'N/A'),
        user_name = COALESCE(user_name, 'N/A'),
        user_screen_name = COALESCE(user_screen_name, 'N/A'),
        user_location = COALESCE(truncated, 'N/A'),
        user_description = COALESCE(user_description, 'N/A'),
        user_verified = COALESCE(user_verified, 'N/A'),
        user_followers_count = COALESCE(user_followers_count, 0),
        user_friends_count = COALESCE(user_friends_count, 0),
        user_statuses_count = COALESCE(user_statuses_count, 0)
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
