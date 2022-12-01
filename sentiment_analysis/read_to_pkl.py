#!/usr/bin/python3
import numpy as np
import pandas as pd

url = "./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets.csv"
df = pd.read_csv(
    url,
    encoding="UTF-8",
    parse_dates=['date', 'user_created'],
    #date_parser=True,
    dtype={
        'user_name': str,
        'user_location': str,
        'user_description': str,
        #'user_created': datetime64,
        'user_followers': str,
        'user_friends': str,
        'user_favourites': str,
        'user_verified': str,
        #'date': datetime64,
        'text': str,
        'hashtags': str,
        'source': str,
        'is_retweet': str
    })
df.sort_values(by="date", inplace=True)
#df.date = pd.to_datetime(df.date,)
df['id'] = range(len(df))
df.set_index("id", inplace=True)
#df = df.iloc[::-1]
df.to_pickle("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets.pkl")