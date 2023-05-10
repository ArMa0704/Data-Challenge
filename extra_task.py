# LUFTHANSA CUSTOMER ENGAGEMENT
import pandas as pd
import matplotlib.pyplot as plt
import os
# Load the CSV file into a Pandas DataFrame
chunksize = 10 ** 7  # adjust this value to fit your needs
chunks = []
for chunk in pd.read_csv('/Users/polinastp/Documents/uni/year1/Q4/dbl/Lufthansa-data-u.csv',
                         chunksize=chunksize,
                         escapechar=None,
                         on_bad_lines='skip',
                         engine='python'):
    chunks.append(chunk)

df = pd.concat(chunks, axis=0)

# Separate the DataFrame into two DataFrames: one for answered tweets and one for unanswered tweets
answered_tweets = df[df['in_reply_to_screen_name'] == 'lufthansa']
unanswered_tweets = df[df['in_reply_to_screen_name'].isna()]

# Count the number of answered and unanswered tweets
num_answered = len(answered_tweets)
num_unanswered = len(unanswered_tweets)

# Labels for the sections of our pie chart
labels = ['Answered', 'Unanswered']

# The values for each section of our pie chart
sizes = [num_answered, num_unanswered]

# The colors of each section of the pie chart
colors = ['#ff9999','#66b3ff']

# Creating the pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title("Lufthansa's engagement with their customers on Twitter")
# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')

# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/polinastp/Documents/uni/year1/Q4/dbl/Lufthansa-data-u.csv')
output_filename = os.path.join(output_dir, 'engagement_chart.png')
plt.savefig(output_filename)

# Display the chart
plt.show()


#PREDICTION OF TWEETS VS AMERICAN AIRLINES
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset

# Suppress Intel MKL Warnings
os.environ['MKL_CBWR'] = 'AUTO'

# Load the data from csv
lufthansa_path = '/Users/polinastp/Documents/uni/year1/Q4/dbl/Lufthansa-data-u.csv'
american_path = '/Users/polinastp/Documents/uni/year1/Q4/dbl/Full_AmericanAir-Final.csv'

df1 = pd.read_csv(lufthansa_path)
df2 = pd.read_csv(american_path)

# Convert datetime
df1['created_at'] = pd.to_datetime(df1['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')
df2['created_at'] = pd.to_datetime(df2['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')

# Convert datetime to numeric for training.
X1 = df1['created_at'].map(pd.Timestamp.timestamp)
X2 = df2['created_at'].map(pd.Timestamp.timestamp)

# Checking for empty data
if X1.empty or df1['retweeted_status.retweet_count'].empty:
    print("Data in df1 is empty!")
else:
    print("Number of tweets in df1: ", len(df1))

if X2.empty or df2['retweeted_status.retweet_count'].empty:
    print("Data in df2 is empty!")
else:
    print("Number of tweets in df2: ", len(df2))

# Reshape data because sklearn wants you to
X1 = np.array(X1).reshape(-1, 1)
X2 = np.array(X2).reshape(-1, 1)

y1 = df1['retweeted_status.retweet_count']
y2 = df2['retweeted_status.retweet_count']

# Handling NaN values in y1 and y2
y1 = y1.fillna(y1.mean())
y2 = y2.fillna(y2.mean())

# Split the data into training and test sets
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

# Create the model
model1 = LinearRegression()
model2 = LinearRegression()

# Train the model
model1.fit(X1_train, y1_train)
model2.fit(X2_train, y2_train)

# Predict the test set
y1_pred = model1.predict(X1_test)
y2_pred = model2.predict(X2_test)

# Evaluate the model
print(f"Model 1 RMSE: {np.sqrt(mean_squared_error(y1_test, y1_pred))}")
print(f"Model 2 RMSE: {np.sqrt(mean_squared_error(y2_test, y2_pred))}")

# Generate future dates for 6 months
future_dates = [df1['created_at'].max() + DateOffset(days=x) for x in range(0,180)]
future_dates_unix = [x.timestamp() for x in future_dates]

# Predict future values
future_pred1 = model1.predict(np.array(future_dates_unix).reshape(-1, 1))
future_pred2 = model2.predict(np.array(future_dates_unix).reshape(-1, 1))

# Plot the results
plt.figure(figsize=(10,6))

# Future predictions
plt.plot(future_dates, future_pred1, color='cyan', label='Future Predicted Retweets Lufthansa')
plt.plot(future_dates, future_pred2, color='magenta', label='Future Predicted Retweets American Air')

# Add labels and title
plt.xlabel('Time of Tweet')
plt.ylabel('Predicted Retweet Count')
plt.title('Future Predicted Retweet Counts for Two Airlines')

# Add legend
plt.legend()

# Save the graph to a PNG file
output_dir = os.path.dirname('/Users/polinastp/Documents/uni/year1/Q4/dbl/Lufthansa-data-u.csv')
output_filename = os.path.join(output_dir, 'predicted-retweets.png')
plt.savefig(output_filename)

# Show the plot
plt.show()








