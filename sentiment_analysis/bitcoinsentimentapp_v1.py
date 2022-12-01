# Import the libraries
from itertools import count
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

# store the data
log = pd.read_csv("./sentiment_analysis/Login.csv")

consumerKey = log["key"][0]
consumerSecret = log["key"][1]
accessToken = log["key"][2]
accessTokenSecret = log["key"][3]

# Create the authentication object
authenticate = tweepy.OAuth1UserHandler(consumerKey, consumerSecret)
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)
# Create the API object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Gather 2000 tweets about Bitcoin and filter out any retweets 'RT'
search_term = "#bitcoin -filter:retweets"
# Create a cursor object
tweets = tweepy.Cursor(api.search_tweets,
                       q=search_term,
                       lang="en",
                       tweet_mode="extended").items(801)

# Store the tweets in a variable and get the full text
all_tweets = [[tweet.full_text, tweet.created_at] for tweet in tweets]

# Create a dataframe to store the tweets with a column called 'Tweets'
df = pd.DataFrame(all_tweets, columns=["Tweets", "Creation_Time"])


# Create a function to clean the tweets
def cleanTwt(twt):
    twt = re.sub("#bitcoin", "bitcoin", twt)  # Removes the '#' from bitcoin
    twt = re.sub("#Bitcoin", "Bitcoin", twt)  # Removes the '#' from Bitcoin
    twt = re.sub("#[A-Za-z0-9]+", "", twt)  # Removes any strings with a '#'
    twt = re.sub("\\n", "", twt)  # Removes the '\n' string
    twt = re.sub("https?:\/\/\S+", "", twt)  # Remove the hyper link
    return twt


# Cleaning the text
df["Cleaned_Tweets"] = df["Tweets"].apply(cleanTwt)


# Create a function to get the subjectivity
def getSubjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity


# Create two new columns
df["Subjectivity"] = df["Cleaned_Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Cleaned_Tweets"].apply(getPolarity)


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
