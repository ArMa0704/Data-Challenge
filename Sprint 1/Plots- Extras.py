# USER LOCATION LUFTHANSA
import pandas as pd
import matplotlib.pyplot as plt
import langid
import os

# Load the CSV file into a Pandas DataFrame
chunksize = 10 ** 7  # adjust this value to fit your needs
chunks = []
for chunk in pd.read_csv('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv',
                         chunksize=chunksize,
                         # delimiter=';',
                         # quotechar="'",
                         escapechar=None,
                         on_bad_lines='skip',
                         engine='python'):
    chunks.append(chunk)


df = pd.concat(chunks, axis=0)

# Filter rows where 'user.location' is not separated by a comma or is not in English
df = df[df['user.location'].apply(lambda x: isinstance(x, str) and ',' in x and langid.classify(x)[0] == 'en')]

# Extract user locations and count occurrences
location_counts = df['user.location'].value_counts()

# Create a DataFrame from the location counts
location_df = pd.DataFrame({'Location': location_counts.index, 'Count': location_counts.values})

# Plot the bar graph
plt.figure(figsize=(15,10)) # Set the figure size to be 15x10 inches
plt.bar(location_df['Location'][:50], location_df['Count'][:50]) # Limit the data to the first 50 columns
plt.xlabel('Location')
plt.ylabel('Number of Users')
plt.ylim(0, 1500) # Set the y-axis limits to 0 and 1500
plt.title("Popular Location of Lufthana's user") # Add a title to the graph
plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 90-degrees
# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv')
output_filename = os.path.join(output_dir, 'user-location.png')
plt.savefig(output_filename)
plt.show()


#TWEETS IN HOLIDAY SEASON
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import os

# Load the CSV file into a Pandas DataFrame
chunksize = 10 ** 7  # adjust this value to fit your needs
chunks = []
for chunk in pd.read_csv('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv',
                         chunksize=chunksize,
                         # delimiter=';',
                         # quotechar="'",
                         escapechar=None,
                         on_bad_lines='skip',
                         engine='python'):
    chunks.append(chunk)
df = pd.concat(chunks, axis=0)

# Convert the "created_at" column to a datetime format
valid_dates = []
for date_str in df['created_at']:
    if date_str is not None:  # Added this condition
        try:
            date_obj = dt.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
            valid_dates.append(date_obj)
        except ValueError:
            valid_dates.append(None)
    else:
        valid_dates.append(None)  # Append None when date_str is None
df['created_at'] = valid_dates

# Filter out the rows with invalid dates
df = df[df['created_at'].notnull()]

# Filter the data to include only the relevant dates
start_date = dt.date(dt(2019, 12, 20))
end_date = dt.date(dt(2020, 1, 2))
df = df[(df['created_at'].dt.date >= start_date) & (df['created_at'].dt.date <= end_date)]

# Group the data by date and count the number of texts per day
texts_count = df.groupby(df['created_at'].dt.date)['text'].count()

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(texts_count.index, texts_count.values)
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title("How Holiday season affects the number of tweets by Lufthansa's customers")
# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv')
output_filename = os.path.join(output_dir, 'holiday-season.png')
plt.savefig(output_filename)
plt.show()

#LANGUAGE DETECTION
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file into a Pandas DataFrame
chunksize = 10 ** 7  # adjust this value to fit your needs
chunks = []
for chunk in pd.read_csv('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv',
                         chunksize=chunksize,
                         escapechar=None,
                         on_bad_lines='skip',
                         engine='python'):
    chunks.append(chunk)

df = pd.concat(chunks, axis=0)

# Assuming 'lang' column contains language abbreviations
df['language'] = df['lang']

# Create a bar chart with the number of texts from each language
lang_counts = df['language'].value_counts()
plt.figure(figsize=(10, 10))
plt.bar(lang_counts.index, lang_counts.values)
plt.xlabel('Language')
plt.ylabel('Number of Texts')
plt.title('Number of Texts per Language')
plt.xticks(rotation=90)
# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv')
output_filename = os.path.join(output_dir, 'language-distribution.png')
plt.savefig(output_filename)

plt.show()

#NUMBER OF VERIFIED USERS TWEETING ABOUT LUFTHANSA; shows how popular it is amongst famous individuals
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file into a Pandas DataFrame
chunksize = 10 ** 7  # adjust this value to fit your needs
chunks = []
for chunk in pd.read_csv('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv',
                         chunksize=chunksize,
                         escapechar=None,
                         on_bad_lines='skip',
                         engine='python'):
    chunks.append(chunk)

df = pd.concat(chunks, axis=0)

# Get the counts of verified and non-verified users
verification_counts = df['user.verified'].value_counts()

# Create a pie chart with the percentage of verified and non-verified users
plt.figure(figsize=(10, 10))
plt.pie(verification_counts, labels=['Verified' if index else 'Non-Verified' for index in verification_counts.index], autopct='%1.1f%%')
plt.title('Percentage of Verified and Non-Verified Users')

# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/tushargupta/Desktop/Uni/Y1/Q4/DBL/Full-Lufthansa-Final.csv')
output_filename = os.path.join(output_dir, 'verification-distribution.png')
plt.savefig(output_filename)

plt.show()
