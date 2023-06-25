import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Load the data
df = pd.read_csv("../conversation_analysis_first_response.csv")

# Convert response_time to total number of minutes (or seconds depending on your needs)
df['response_time'] = df['response_time'].apply(lambda x: pd.to_timedelta(x).total_seconds()/60)

# Remove rows where response_time is less than or equal to 0
df = df[df['response_time'] > 0]


# Create a model
X = df["response_time"]
y = df["sentiment"]
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

df['Predicted'] = model.predict(X)
df['Residuals'] = model.resid

# Create residual plot
plt.figure(figsize=(8, 6))
sns.residplot(x=df['Predicted'], y=df['Residuals'], lowess=True, line_kws={'color': 'red', 'lw': 1, 'alpha': 1})
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted values')
plt.xlim(left=0)  # Setting x limit
plt.show()

