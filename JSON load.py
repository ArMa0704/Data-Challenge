
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

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, ', '.join([f'{col} TEXT' if col != 'id' else f'{col} INTEGER PRIMARY KEY' for col in columns])))
conn.commit()

for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        with open(os.path.join(json_dir, filename), "r", encoding="utf-8") as f:
            for line in f:
                if validate_json(line):
                    data = json.loads(line)

                    user = data.get("user")
                    if user is not None:
                        values = [
                            data.get("created_at"),
                            data.get("id"),
                            data.get("id_str"),
                            data.get("text"),
                            data.get("source"),
                            data.get("truncated"),
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

                        cursor.execute("REPLACE INTO {} ({}) VALUES ({})".format(table_name, ', '.join(columns), ', '.join(['?' for _ in columns])), values)
                        conn.commit()

conn.close()





