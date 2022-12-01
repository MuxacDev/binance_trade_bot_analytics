# Description : This is a serftiment analysis program that parses the tweets fetched from Twitter using Python

# Import the libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

# Load the data
from google.colab import files

uploaded = files.upload()

# Get the data
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

# Extract 100 tweets from the twitter user
posts = api.user_timeline(
    screen_name="BillGates", count=100, lang="en", tweet_mode="extended"
)
# Print the last 5 tweets from the account
print("Show the 5 recent tweets: \n")
i = 1
for tweet in posts[0:5]:
    print(str(i) + ") " + tweet.full_text + "\n")
    i = i + 1

# Create a dataframe with a column called Tweets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=["Tweets"])
# Show the first 5 rows of data
df.head()

# Clean the text
# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub(r"@[A-Za-z0-9]+", "", text)  # Removed ^mentions
    text = re.sub(r"#", "", text)  # Removing the '#' symbol
    text = re.sub(r"RT[\s]+", "", text)  # Removing RT
    text = re.sub(r"https?:\/\/\S+", "", text)  # Remove the hyper link
    return text


# Cleaning the text
df["Tweets"] = df["Tweets"].apply(cleanTxt)

# Show the cleaned text
df

# Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity


# Create two new columns
df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Tweets"].apply(getPolarity)

# Show the new dataframe with the new columns
df

# Plot The Word Cloud
allWords = " ".join([twts for twts in df["Tweets"]])
wordCloud = WordCloud(
    width=500, height=300, random_state=21, max_font_size=119
).generate(allWords)

plt.imshow(wordCloud, interpolatiop="bilinear")
plt.axis("off")
plt.show()

# Creatie a function to compute the negative, neutral and positive analysis
def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


df["Analysis"] = df["Polarity"].apply(getAnalysis)

# Show the dataframe
df

# Print all of the positive tweets
j = 1
sortedDF = df.sort_values(by=["Polarity"])
for i in range(0, sortedDF.shape[0]):
    if sortedDF["Analysis"][i] == "Positive":
        print(str(j) + ") " + sortedDF["Tweets"][i])
        print()
        j = j + i
