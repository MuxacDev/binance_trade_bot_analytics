#!/usr/bin/python3
import pandas as pd
import numpy as np


sy = "2015"
df0 = pd.read_pickle("./crypto_btcusdt" + sy + ".pkl")
df015 = df0.groupby(pd.Grouper(freq="15Min")).agg(
    {
        "unix": "last",
        "symbol": "last",
        "open": "first",
        "close": "last",
        "low": "min",
        "high": "max",
        "Volume BTC": "sum",
        "Volume USD": "sum",
    }
)
df030 = df0.groupby(pd.Grouper(freq="30Min")).agg(
    {
        "unix": "last",
        "symbol": "last",
        "open": "first",
        "close": "last",
        "low": "min",
        "high": "max",
        "Volume BTC": "sum",
        "Volume USD": "sum",
    }
)


selyear = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]
for sy in selyear:
    #    url = "data/Bitstamp_BTCUSD_" + sy + "_minute.csv"
    #    df = pd.read_csv(url, skiprows = 1)
    #    df.date = pd.to_datetime(df.date)
    #    df.set_index("date", inplace = True)
    #    df = df.iloc[::-1]
    df = pd.read_pickle("./data/crypto_btcusdt" + sy + ".pkl")
    #    df.to_pickle('./crypto_btcusdt' + sy + '.pkl')
    df15 = df.groupby(pd.Grouper(freq="15Min")).agg(
        {
            "unix": "last",
            "symbol": "last",
            "open": "first",
            "close": "last",
            "low": "min",
            "high": "max",
            "Volume BTC": "sum",
            "Volume USD": "sum",
        }
    )
    df015 = pd.concat([df015, df15])
    df30 = df.groupby(pd.Grouper(freq="30Min")).agg(
        {
            "unix": "last",
            "symbol": "last",
            "open": "first",
            "close": "last",
            "low": "min",
            "high": "max",
            "Volume BTC": "sum",
            "Volume USD": "sum",
        }
    )
    df030 = pd.concat([df030, df30])

df015.to_pickle("./data/crypto_btcusdt_15.pkl")
df030.to_pickle("./data/crypto_btcusdt_30.pkl")
