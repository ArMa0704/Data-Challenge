import json
import os
import sqlite3

def validate_json(json_data):
    try:
        json.loads(json_data)
        return True
    except ValueError as e:
        return False

json_dir = "/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/data"
db_filename = "data.db"
table_name = "twitter_data"

columns = [
    "created_at",
    "id",
    "id_str",
    "text",
    "source",
    "truncated",
    "user_geo",
    "user_coordinates",
    "user_place",
    "user_contributors",
    "user_is_quote_status",
    "extended_tweet_quote_count",
    "extended_tweet_reply_count",
    "extended_tweet_retweet_count",
    "extended_tweet_favourite_count",
    "entities_favourited",
    "entities_retweeted",
    "entities_filter_level",
    "entities_lang",
    "entities_timestamp_ms",
    "retweeted_status_id",
    "retweeted_status_id_str",
    "retweeted_status_user_id",
    "retweeted_status_user_id_str",
    "retweeted_status_user_screen_name",
    "quoted_status_id",
    "quoted_status_id_str",
    "quoted_status_user_id",
    "quoted_status_user_id_str",
    "quoted_status_user_screen_name"
]

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Check if columns already exist in table
existing_columns = []
cursor.execute(f"PRAGMA table_info({table_name})")
for col in cursor.fetchall():
    existing_columns.append(col[1])

# Add new columns to table
for col in columns:
    if col not in existing_columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col} TEXT")
        conn.commit()
        print(f"Added column {col} to table {table_name}")

for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        with open(os.path.join(json_dir, filename), "r", encoding="utf-8") as f:
            for line in f:
                if validate_json(line):
                    data = json.loads(line)

                    user = data.get("user")
                    extended_tweet = data.get("extended_tweet")
                    entities = data.get("entities")
                    retweeted_status = data.get("retweeted_status")
                    quoted_status = data.get("quoted_status")

                    if user is not None:
                        user_geo = user.get("geo")
                        user_coordinates = user.get("coordinates")
                        user_place = user.get("place")
                        user_contributors = user.get("contributors")
                        user_is_quote_status = user.get("is_quote_status")
                    else:
                        user_geo = None
                        user_coordinates = None
                        user_place = None
                        user_contributors = None
                        user_is_quote_status = None

                    if extended_tweet is not None:
                        extended_tweet_quote_count = extended_tweet.get("quote_count")
                        extended_tweet_reply_count = extended_tweet.get("reply_count")
                        extended_tweet_retweet_count = extended_tweet.get("retweet_count")
                        extended_tweet_favourite_count = extended_tweet.get("favourite_count")
                    else:
                        extended_tweet_quote_count = None
                        extended_tweet_reply_count = None
                        extended_tweet_retweet_count = None
                        extended_tweet_favourite_count = None

                    if entities is not None:
                        entities_favourited = entities.get("favourited")
                        entities_retweeted = entities.get("retweeted")
                        entities_filter_level = entities.get("filter_level")
                        entities_lang = entities.get("lang")
                        entities_timestamp_ms = entities.get("timestamp_ms")
                    else:
                        entities_favourited = None
                        entities_retweeted = None
                        entities_filter_level = None
                        entities_lang = None
                        entities_timestamp_ms = None

                    if retweeted_status is not None:
                        retweeted_status_id = retweeted_status.get("id")
                        retweeted_status_id_str = retweeted_status.get("id_str")
                        retweeted_status_user_id = retweeted_status.get("user").get("id")
                        retweeted_status_user_id_str = retweeted_status.get("user").get("id_str")
                        retweeted_status_user_screen_name = retweeted_status.get("user").get("screen_name")
                    else:
                        retweeted_status_id = None
                        retweeted_status_id_str = None
                        retweeted_status_user_id = None
                        retweeted_status_user_id_str = None
                        retweeted_status_user_screen_name = None

                    if quoted_status is not None:
                        quoted_status_id = quoted_status.get("id")
                        quoted_status_id_str = quoted_status.get("id_str")
                        quoted_status_user_id = quoted_status.get("user").get("id")
                        quoted_status_user_id_str = quoted_status.get("user").get("id_str")
                        quoted_status_user_screen_name = quoted_status.get("user").get("screen_name")
                    else:
                        quoted_status_id = None
                        quoted_status_id_str = None
                        quoted_status_user_id = None
                        quoted_status_user_id_str = None
                        quoted_status_user_screen_name = None

                    values = [
                        data.get("created_at"),
                        data.get("id"),
                        data.get("id_str"),
                        data.get("text"),
                        data.get("source"),
                        data.get("truncated"),
                        user_geo,
                        user_coordinates,
                        user_place,
                        user_contributors,
                        user_is_quote_status,
                        extended_tweet_quote_count,
                        extended_tweet_reply_count,
                        extended_tweet_retweet_count,
                        extended_tweet_favourite_count,
                        entities_favourited,
                        entities_retweeted,
                        entities_filter_level,
                        entities_lang,
                        entities_timestamp_ms,
                        retweeted_status_id,
                        retweeted_status_id_str,
                        retweeted_status_user_id,
                        retweeted_status_user_id_str,
                        retweeted_status_user_screen_name,
                        quoted_status_id,
                        quoted_status_id_str,
                        quoted_status_user_id,
                        quoted_status_user_id_str,
                        quoted_status_user_screen_name
                    ]

                    cursor.execute("REPLACE INTO {} ({}) VALUES ({})".format(table_name, ', '.join(columns), ', '.join(['?' for _ in columns])), values)
                    conn.commit()

conn.close()
