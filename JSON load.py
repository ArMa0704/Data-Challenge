
import os
import json
import sqlite3

json_folder = '/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL Data Challenge/data'

# create a connection to the SQLite database
conn = sqlite3.connect('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL Data Challenge/data.db')
c = conn.cursor()

# ... (table creation code remains the same)

# loop through each file in the folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            # read all the lines in the file and remove extra spaces
            lines = (line.strip() for line in f)

            # loop through each line and parse the JSON object
            for line in lines:
                try:
                    json_obj = json.loads(line)

                    # extract the required fields from the JSON object
                    # ... (previous fields remain the same)

                    user_followers_count = json_obj['user']['followers_count']
                    user_friends_count = json_obj['user']['friends_count']
                    user_listed_count = json_obj['user']['listed_count']
                    user_favourites_count = json_obj['user']['favourites_count']
                    user_statuses_count = json_obj['user']['statuses_count']
                    user_created_at = json_obj['user']['created_at']
                    user_utc_offset = json_obj['user']['utc_offset']
                    user_time_zone = json_obj['user']['time_zone']
                    user_geo_enabled = json_obj['user']['geo_enabled']
                    user_lang = json_obj['user']['lang']
                    user_contributors_enabled = json_obj['user']['contributors_enabled']
                    user_is_translator = json_obj['user']['is_translator']
                    user_profile_background_color = json_obj['user']['profile_background_color']
                    user_profile_background_image_url = json_obj['user']['profile_background_image_url']
                    user_profile_background_image_url_https = json_obj['user']['profile_background_image_url_https']
                    user_profile_background_tile = json_obj['user']['profile_background_tile']
                    user_profile_link_color = json_obj['user']['profile_link_color']
                    user_profile_sidebar_border_color = json_obj['user']['profile_sidebar_border_color']
                    user_profile_sidebar_fill_color = json_obj['user']['profile_sidebar_fill_color']
                    user_profile_text_color = json_obj['user']['profile_text_color']
                    user_profile_use_background_image = json_obj['user']['profile_use_background_image']
                    user_profile_image_url = json_obj['user']['profile_image_url']
                    user_profile_image_url_https = json_obj['user']['profile_image_url_https']
                    user_profile_banner_url = json_obj['user']['profile_banner_url']
                    user_default_profile = json_obj['user']['default_profile']
                    user_default_profile_image = json_obj['user']['default_profile_image']
                    geo = json_obj['geo']
                    coordinates = json_obj['coordinates']
                    place = json_obj['place']
                    contributors = json_obj['contributors']
                    is_quote_status = json_obj['is_quote_status']
                    quote_count = json_obj['quote_count']
                    reply_count = json_obj['reply_count']
                    json_text = json.dumps(json_obj)

                    # insert the data into the SQLite database
                    c.execute('''INSERT INTO json_data
                                 (created_at, id_str, text, display_text_range, source, truncated,
                                  in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id,
                                  in_reply_to_user_id_str, in_reply_to_screen_name, user_id, user_name,
                                  user_screen_name, user_location, user_description, user_protected,
                                  user_verified, user_followers_count, user_friends_count, user_listed_count,
                                  user_favourites_count, user_statuses_count, user_created_at, user_utc_offset,
                                  user_time_zone, user_geo_enabled, user_lang, user_contributors_enabled,
                                  user_is_translator, user_profile_background_color, user_profile_background_image_url,
                                  user_profile_background_image_url_https, user_profile_background_tile,
                                  user_profile_link_color, user_profile_sidebar_border_color, user_profile_sidebar_fill_color,
                                  user_profile_text_color, user_profile_use_background_image, user_profile_image_url,
                                  user_profile_image_url_https, user_profile_banner_url, user_default_profile,
                                  user_default_profile_image, geo, coordinates, place, contributors, is_quote_status,
                                  quote_count, reply_count, json_text)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                 (created_at, id_str, text, display_text_range, source, truncated,
                                  in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id,
                                  in_reply_to_user_id_str, in_reply_to_screen_name, user_id, user_name,
                                  user_screen_name, user_location, user_description, user_protected,
                                  user_verified, user_followers_count, user_friends_count, user_listed_count,
                                  user_favourites_count, user_statuses_count, user_created_at, user_utc_offset,
                                  user_time_zone, user_geo_enabled, user_lang, user_contributors_enabled,
                                  user_is_translator, user_profile_background_color, user_profile_background_image_url,
                                  user_profile_background_image_url_https, user_profile_background_tile,
                                  user_profile_link_color, user_profile_sidebar_border_color, user_profile_sidebar_fill_color,
                                  user_profile_text_color, user_profile_use_background_image, user_profile_image_url,
                                  user_profile_image_url_https, user_profile_banner_url, user_default_profile,
                                  user_default_profile_image, geo, coordinates, place, contributors, is_quote_status,
                                  quote_count, reply_count, json_text))

                    # commit the changes and close the connection
                    conn.commit()

                except Exception as e:
                    print(f"Error processing line: {line}")
                    print(f"Error: {e}")

# close the connection to the SQLite database
conn.close()

