#!/usr/bin/python3
import pandas as pd
import numpy as np

sy = "2015"
url = "data/Bitstamp_BTCUSD_" + sy + "_minute.csv"
df0 = pd.read_csv(url, skiprows=1)
df0.date = pd.to_datetime(df0.date)
df0.set_index("date", inplace=True)
df0 = df0.iloc[::-1]


selyear = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]
for sy in selyear:
    url = "data/Bitstamp_BTCUSD_" + sy + "_minute.csv"
    df = pd.read_csv(url, skiprows=1)
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.iloc[::-1]
    df0 = pd.concat([df0, df])


df0.to_pickle("./data/crypto_btcusdt" + ".pkl")
