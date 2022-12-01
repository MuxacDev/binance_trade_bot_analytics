# Description: This program gets the sentiment of Bitcoin from Twitter users

# Import the libraries
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

# upload the login file
from google.colab import files

uploaded = files.upload()

# store the data
log = pd.read_csv("Login.csv")

# Twitter API credentials
consumerKey = log["key"][0]
consumerSecret = log["key"][1]
accessToken = log["key"][2]
accessTokenSecret = log["key"][3]

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)
# Create the API object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Gather 2000 tweets about Bitcoin and filter out any retweets 'RT'
search_term = "#bitcoin -filter:retweets"
# Create a cursor object
tweets = tweepy.Cursor(api.search,
                       q=search_term,
                       lang="en",
                       since="2018-11-01",
                       tweet_mode="extended").items(2000)
# Store the tweets in a variable and get the full text
all_tweets = [tweet.full_text for tweet in tweets]

# Create a dataframe to store the tweets with a column called 'Tweets'
df = pd.DataFrame(all_tweets, columns=["Tweets"])
# Show the first 5 rows of data
df.head(5)


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
# Show the data set
df.head(10)


# Create a function to get the subjectivity
def getSubjectivity(twt):
    return TextBlob(twt).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(twt):
    return TextBlob(twt).sentiment.polarity


# Create two new columns
df["Subjectivity"] = df["Cleaned_Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Cleaned_Tweets"].apply(getPolarity)

# Show the data set
df.head(10)


# Create a function to get the text sentiment
def getSentiment(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


# Create a column to store the text sentiment
df["Sentiment"] = ["Polarity"].apply(getSentiment)
# Show the data
df.head()

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
