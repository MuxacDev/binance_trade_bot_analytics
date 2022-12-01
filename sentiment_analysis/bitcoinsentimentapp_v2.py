# Import the libraries
from itertools import count
from click import open_file
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

# with open("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets.csv",
#           "r",
#           encoding="UTF-8") as f:
#     head = [next(f) for x in range(10)]
#     with open('./sentiment_analysis/result_v2.txt', 'a',
#               encoding="UTF-8") as f:
#         print(head, file=f)  # Python 3.x

df0 = pd.read_pickle("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets.pkl")

# for i in range(len(df)):
#     if i % 5000 == 0:
#         print(str(df.index[i]) + " " + str(df["date"][i]))

df = df0[['date', 'text']]


# Create a function to clean the tweets
def cleanTwt(twt):
    twt = str(twt)
    twt = re.sub("#bitcoin", "bitcoin", twt)  # Removes the '#' from bitcoin
    twt = re.sub("#Bitcoin", "Bitcoin", twt)  # Removes the '#' from Bitcoin
    twt = re.sub("#[A-Za-z0-9]+", "", twt)  # Removes any strings with a '#'
    twt = re.sub("\\n", "", twt)  # Removes the '\n' string
    twt = re.sub("https?:\/\/\S+", "", twt)  # Remove the hyper link
    return twt


# Cleaning the text
df["Cleaned_Tweets"] = df["text"].apply(cleanTwt)
print("Cleaned tweets")


# Create a function to get the subjectivity
def getSubjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity


# Create two new columns
df["Subjectivity"] = df["Cleaned_Tweets"].apply(getSubjectivity)
print("Subjectivity")
df["Polarity"] = df["Cleaned_Tweets"].apply(getPolarity)
print("Polarity")


# Create a function to get the text sentiment
def getSentiment(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


# Create a column to store the text sentiment
df["Sentiment"] = df["Polarity"].apply(getSentiment)
print("Sentiment")

print(df.head(100))
df.to_pickle("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets_Analysed.pkl")
exit()
df.to_csv("./sentiment_analysis/result.csv",
          index=False,
          columns=["Creation_Time", "Cleaned_Tweets"])
exit()
# Create a scatter plot to show the subjectivity and the polarity
plt.figure(figsize=(8, 6))
for i in range(0, df.shape[0]):
    plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color="Purple")
plt.title("Sentiment Analysis Scatter Plot")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity (objective -> subjective)")
plt.show()

# Create a bar chart to show the count of Positive, Neutral, and Negative sentiments
df["Sentiment"].value_counts().plot(kind="bar")
plt.title("Sentiment Analysis Bar Plot")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.show()
