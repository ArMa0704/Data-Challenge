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
    "extended_tweet",
    "entities"
]

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {', '.join([f"{col} TEXT" for col in columns])})''')

existing_columns = []
cursor.execute(f"PRAGMA table_info({table_name})")
for col in cursor.fetchall():
    existing_columns.append(col[1])

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
                        json.dumps(data.get("extended_tweet")) if data.get("extended_tweet") else None,
                        json.dumps(data.get("entities")) if data.get("entities") else None
                    ]

                    cursor.execute("REPLACE INTO {} ({}) VALUES ({})".format(table_name, ', '.join(columns),
                                                                             ', '.join(['?' for _ in columns])), values)
                    conn.commit()

conn.close()