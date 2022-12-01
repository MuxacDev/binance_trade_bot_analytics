import numpy as np
import pandas as pd

with open("data/Bitstamp_BTCUSD_2015_minute.csv") as f:
    df = pd.read_csv(f, skiprows=1)
f.close()
df = df.iloc[::-1]

data = df.to_numpy()
a = ""
for col in df.columns:
    a += col + "\t"
print(a)
for i in range(1000):
    print(
        str(data[i][0])
        + " "
        + str(data[i][1])
        + " "
        + str(data[i][2])
        + " "
        + str(data[i][3])
        + " "
        + str(data[i][4])
        + " "
        + str(data[i][5])
        + " "
        + str(data[i][6])
        + " "
        + str(data[i][7])        
        + " "
        + str(data[i][8])
    )
