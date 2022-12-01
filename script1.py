import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date

balOverall = 500
startPoint = date(2015, 1, 1)


df = pd.read_pickle("./crypto_btcusdt.pkl")

print(df.index.__len__())

len = 0
selyear = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
for sy in selyear:
    df = pd.read_pickle("./crypto_btcusdt" + sy + ".pkl")
    len = len + df.index.__len__()

print(len)
