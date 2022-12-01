import pandas as pd

df0 = pd.read_pickle(
    "./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets_Analysed.pkl")

# with open("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets_Analysed.csv",
#           'a',
#           encoding="UTF-8") as f:
#     print(df.head(100), file=f)  # Python 3.x

df = df0.iloc[:1000]
df.to_csv("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets_Analysed.csv",
          index=False,
          sep="\t")
