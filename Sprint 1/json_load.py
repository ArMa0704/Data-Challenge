import json
import os
import sqlite3

def validate_json(json_data):
    try:
        json.loads(json_data)
        return True
    except ValueError as e:
        return False

json_dir = "/Users/polinastp/Documents/uni/year1/Q4/dbl/data"
db_filename = "data_air.db"
table_name = "twitter_data"
user_table_name = "user_data"
extended_tweet_table_name = "extended_tweet_data"
entities_table_name = "entities_data"

columns = [
    "id_str",
    "text",
    "source",
    "truncated",
    "in_reply_to_status_id",
    "in_reply_to_status_id_str",
    "in_reply_to_user_id",
    "in_reply_to_user_id_str",
    "in_reply_to_screen_name",
    "user_id",
    "extended_tweet_id",
    "entities_id"
]

user_columns = [
    "user_id",
    "user_name",
    "user_screen_name",
    "user_location",
    "user_description",
    "user_verified",
    "user_followers_count",
    "user_friends_count",
    "user_statuses_count"
]

extended_tweet_columns = [
    "extended_tweet_id",
    "full_text",
    "display_text_range",
    "quote_count",
    "reply_count",
    "retweet_count",
    "favorite_count"
]

entities_columns = [
    "entities_id",
    "hashtags",
    "urls",
    "user_mentions",
    "symbols"
]

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create main table
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join([f"{col} TEXT" for col in columns])})''')

# Create user table
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {user_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join([f"{col} TEXT" for col in user_columns])})''')

# Create extended_tweet table
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {extended_tweet_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join([f"{col} TEXT" for col in extended_tweet_columns])})''')

# Create entities table
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {entities_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join([f"{col} TEXT" for col in entities_columns])})''')

# Function to create a new record in the user table
def insert_user(user):
    user_values = [
        user.get("id"),
        user.get("name"),
        user.get("screen_name"),
        user.get("location"),
        user.get("description"),
        user.get("verified"),
        user.get("followers_count"),
        user.get("friends_count"),
        user.get("statuses_count")
    ]
    cursor.execute(f"REPLACE INTO {user_table_name} ({', '.join(user_columns)}) VALUES ({', '.join(['?' for _ in user_columns])})", user_values)
    conn.commit()

# Function to create a new record in the extended_tweet table
def insert_extended_tweet(extended_tweet):
    extended_tweet_values = [
        extended_tweet.get("id"),
        extended_tweet.get("full_text"),
        str(extended_tweet.get("display_text_range")),
        extended_tweet.get("quote_count"),
        extended_tweet.get("reply_count"),
        extended_tweet.get("retweet_count"),
        extended_tweet.get("favorite_count")
    ]
    cursor.execute(
        f"REPLACE INTO {extended_tweet_table_name} ({', '.join(extended_tweet_columns)}) VALUES ({', '.join(['?' for _ in extended_tweet_columns])})",
        extended_tweet_values)
    conn.commit()

    # Function to create a new record in the entities table


def insert_entities(entities):
    entities_values = [
        entities.get("id"),
        json.dumps(entities.get("hashtags")),
        json.dumps(entities.get("urls")),
        json.dumps(entities.get("user_mentions")),
        json.dumps(entities.get("symbols"))
    ]
    cursor.execute(
        f"REPLACE INTO {entities_table_name} ({', '.join(entities_columns)}) VALUES ({', '.join(['?' for _ in entities_columns])})",
        entities_values)
    conn.commit()


for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        with open(os.path.join(json_dir, filename), "r", encoding="utf-8") as f:
            for line in f:
                if validate_json(line):
                    data = json.loads(line)
                    user = data.get("user")
                    extended_tweet = data.get("extended_tweet")
                    entities = data.get("entities")

                    if user:
                        insert_user(user)
                    if extended_tweet:
                        extended_tweet["id"] = data.get("id_str")
                        insert_extended_tweet(extended_tweet)
                    if entities:
                        entities["id"] = data.get("id_str")
                        insert_entities(entities)

                    values = [
                        data.get("id_str"),
                        data.get("text"),
                        data.get("source"),
                        data.get("truncated"),
                        data.get("in_reply_to_status_id"),
                        data.get("in_reply_to_status_id_str"),
                        data.get("in_reply_to_user_id"),
                        data.get("in_reply_to_user_id_str"),
                        data.get("in_reply_to_screen_name"),
                        user.get("id") if user else None,
                        data.get("id_str") if extended_tweet else None,
                        data.get("id_str") if entities else None
                    ]

                    cursor.execute("REPLACE INTO {} ({}) VALUES ({})".format(table_name, ', '.join(columns),
                                                                             ', '.join(['?' for _ in columns])), values)
                    conn.commit()

conn.close()
