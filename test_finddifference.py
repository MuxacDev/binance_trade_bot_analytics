import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import array as arr


selyear = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
data = np.empty([0, 8])
dataId = list()
for sy in selyear:
    df = pd.read_pickle("./data/crypto_btcusdt" + sy + ".pkl")
    data = np.concatenate((data, df.to_numpy()), axis=0)
    for i in df.index:
        dataId.append(str(i))

N = data.__len__()
x = np.arange(N)
y = data[:, [3]]

printlist = list()
sumarr = arr.array("d", [0])
sum = 0.0
last = 0.0
for i in x:
    sum += abs(y[i] - last)
    last = y[i]
    if i % 43800 == 0:
        sumarr.append(sum)
        printlist.append([str(dataId[i]), str(sum)])
        sum = 0.0

# print(max(sumarr))
# for i in printlist:
#     print(i[0] + " " + i[1])

N1 = sumarr.__len__()
x1 = np.arange(N1)

xarr1 = arr.array("i", [0])
xarr2 = arr.array("i", [0])
for i in x1:
    if i % 12 != 0:
        xarr1.append(i)
    else:
        xarr2.append(i)

fig = plt.figure()
plt.plot(x1, sumarr, "bo")
plt.grid(True)
plt.vlines(xarr1, 0, max(sumarr), linestyles="dotted", colors="k")
plt.vlines(xarr2, 0, max(sumarr), linestyles="dashed", colors="k")
plt.show()
