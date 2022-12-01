# from asyncio.windows_events import NULL
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import array as arr


selyear = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
data = np.empty([0, 8])
for sy in selyear:
    df = pd.read_pickle("./data/crypto_btcusdt" + sy + ".pkl")
    data = np.concatenate((data, df.to_numpy()), axis=0)

# sy = "2021"
# data = pd.read_pickle("./crypto_btcusdt" + sy + ".pkl").to_numpy()


N = data.__len__()
x = np.arange(N)
y = data[:, [4]]

fig = plt.figure()
plt.plot(x, y)
plt.grid(True)

xarr1 = arr.array("i", [0])
xarr2 = arr.array("i", [0])
for i in x:
    if i % 43800 == 0:
        if i % 525600 != 0:
            xarr1.append(i)
    if i % 525600 == 0:
        xarr2.append(i)

# print(xarr.__len__())

plt.vlines(xarr1, 0, np.ndarray.max(y), linestyles="dotted", colors="k")
plt.vlines(xarr2, 0, np.ndarray.max(y), linestyles="dashed", colors="k")
plt.show()
