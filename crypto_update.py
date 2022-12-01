#!/usr/bin/python3
import pandas as pd
import numpy as np

selyear = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
# selyear = ["2014"]
for sy in selyear:
    url = "data/Bitstamp_BTCUSD_" + sy + "_minute.csv"
    df = pd.read_csv(url, skiprows=1)
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df = df.iloc[::-1]
    print(df)
    df.to_pickle("./crypto_btcusdt" + sy + ".pkl")
