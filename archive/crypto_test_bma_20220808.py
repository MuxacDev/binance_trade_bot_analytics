#!/usr/bin/python3
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta, date
import os
import shutil
import mysql.connector


def msgPrint(s, b):
    global skipprt
    skipprt = skipprt + 1
    if skipprt >= 0:
        print(s)
        skipprt = 0


def checkOrders(idx):
    global orders, balUSD, balBTC, currentBid
    ids2remove = []
    # print("check orders ", idx)
    current = df.query("index == '" + str(idx) + "'")
    currentBid = float(current["close"])
    # print(currentBid)
    for chorder in orders:
        # chek for complete
        okBuy = (chorder["type"] == "BUY") and (currentBid <= chorder["price"])
        okSell = (chorder["type"] == "SELL") and (currentBid >= chorder["price"])
        # print(chorder["type"], " || ", chorder["price"], " || ", currentBid)
        # print(okBuy, " - ", okSell)
        if okBuy:
            balBTC = balBTC + chorder["vol"]
            ids2remove.append(chorder["id"])
            print("hit!!!!!!!!!!!!!!!!!!!!!!!!!Buy!!!!!!!")
        if okSell:
            balUSD = balUSD + (chorder["vol"] * chorder["price"])
            ids2remove.append(chorder["id"])
            print("hit!!!!!!!!!!!!!!!!!!!!!!!!!Sell!!!!!!")
        # check old
        if oldOrd > 0:
            tord = datetime.strptime(
                str(chorder["date"]), "%Y-%m-%d %H:%M:%S"
            ) + timedelta(days=oldOrd)
            tnow = datetime.strptime(str(current.index[0]), "%Y-%m-%d %H:%M:%S")
            #            print(tord, "     ", tnow)
            #            exit()
            if tnow >= tord:
                print("hit!!!!!!!!!!!!!!!!!!!!!!!!!OLDORDER!!!!!!!")
                if chorder["type"] == "SELL":
                    balBTC = balBTC + chorder["vol"]
                    ids2remove.append(chorder["id"])
                else:
                    balUSD = balUSD + (chorder["vol"] * chorder["price"])
                    ids2remove.append(chorder["id"])

    for ids in ids2remove:
        idxO = next(z for z in orders if z["id"] == ids)
        orders.remove(idxO)


def mainProc(idx, klines):
    global orders, order, df, balBTC, balUSD, orderIDs, currentBid, firstStart
    # print("mainProc")
    mySymbols = {
        1: {"name": "BTC", "balance": 0, "tax": 0.1, "volume": 0.0015},
        2: {"name": "USD", "balance": 0, "tax": 0.1, "volume": 35.00},
    }

    mySymbols[1]["balance"] = balBTC
    mySymbols[2]["balance"] = balUSD

    current = df.query("index == '" + str(idx) + "'")
    currentBid = float(current["close"])
    print("[", idx, "]")
    myAvailableBalance = mySymbols[1]["balance"] * currentBid + mySymbols[2]["balance"]
    msgPrint(
        "Available Balance:\t"
        + str(round(myAvailableBalance, 2))
        + " "
        + mySymbols[2]["name"],
        True,
    )

    # get orderlist and calculate orders balance
    myOrderBalance = 0
    for j in range(0, len(orders)):
        myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) * currentBid)

    myTotalBalance = myAvailableBalance + myOrderBalance
    realPercentUsage = round(myOrderBalance / myTotalBalance, 2) * 100
    msgPrint(
        "Orders Balance \["
        + str(len(orders))
        + "]:\t"
        + str(round(myOrderBalance, 2))
        + " "
        + "USD"
        + " ("
        + str(round(realPercentUsage, 2))
        + "%) calc with current price: "
        + str(round(currentBid, 2)),
        True,
    )
    msgPrint("Total Balance:\t" + str(round(myTotalBalance, 2)) + " " + "USD", True)

    enableOpenOrders = maxUsage > realPercentUsage
    # get hall of trading
    maxPrice = float(klines["high"].max())
    minPrice = float(klines["low"].min())
    msgPrint("MAX Bid: " + str(round(maxPrice, 2)), True)
    msgPrint("MIN Bid: " + str(round(minPrice, 2)), True)
    msgPrint("Current Bid: " + str(currentBid), True)

    # calc Strategy Type
    mMove = ["grow", "fall"]
    nearByMAX = maxPrice - currentBid
    nearByMIN = currentBid - minPrice
    byMAX = nearByMAX < currentBid * margin
    byMIN = nearByMIN < currentBid * margin

    # detect angel of falling or growing market
    deltaHi = (nearByMAX + nearByMIN) / 4
    deltaLow = (nearByMAX + nearByMIN) / 2
    marketMove = ""
    if (nearByMAX < deltaHi) or (nearByMIN < deltaHi):
        marketMove = "hi "
    elif (nearByMAX < deltaLow) or (nearByMIN < deltaLow):
        marketMove = "low "
    idM = 0
    if nearByMAX > nearByMIN:
        idM = 1
    msgPrint(
        "Market is: *"
        + marketMove
        + mMove[idM]
        + "* \["
        + str(round(nearByMAX, 2))
        + " : "
        + str(round(nearByMIN, 2))
        + "]",
        True,
    )

    sellPrice = round(maxPrice - maxPrice * margin, 2)
    buyPrice = round(minPrice + minPrice * margin, 2)

    if (sellPrice > (currentBid + (currentBid * margin))) and (
        buyPrice < (currentBid - (currentBid * margin))
    ):
        msgPrint(
            "Recomended: Strategy 2 (small hall) SELL: "
            + str(round(sellPrice, 2))
            + " BUY: "
            + str(round(buyPrice, 2)),
            True,
        )
    elif (byMAX) or (byMIN):
        sellPrice = round((currentBid * (1 + margin)), 2)
        buyPrice = round((currentBid - (currentBid * margin)), 2)
        msgPrint(
            "Recomended: Strategy 3 TRTTB (MAX: "
            + str(byMAX)
            + " | MIN: "
            + str(byMIN)
            + ") SELL: "
            + str(round(sellPrice, 2))
            + " BUY: "
            + str(round(buyPrice, 2)),
            True,
        )
    else:
        sellPrice = round((maxPrice * (1 + margin)), 2)
        buyPrice = round((minPrice - (minPrice * margin)), 2)
        msgPrint(
            "Recomended: Strategy 1 (Big Hall). SELL: "
            + str(round(sellPrice, 2))
            + " BUY: "
            + str(round(buyPrice, 2)),
            True,
        )

    # security check Prices for higher or lower from currentbid to suppress overprice buy or sell
    needCorr = (sellPrice <= currentBid) or (buyPrice >= currentBid)
    if needCorr:
        msgPrint("\u203C" + "SELL|BUY price need to correct...", True)

    while needCorr:
        if sellPrice <= currentBid:
            sellPrice = sellPrice * 1.005
        if buyPrice >= currentBid:
            buyPrice = buyPrice * 0.995
        needCorr = (sellPrice <= currentBid) or (buyPrice >= currentBid)

    msgPrint("Calculated sell price is: " + str(round(sellPrice, 2)), True)
    msgPrint("Calculated buy price is: " + str(round(buyPrice, 2)), True)

    if enableOpenOrders:
        msgPrint("Balance is available to open orders!", True)
        if mySymbols[1]["balance"] > volBTC:
            newOrder = order.copy()
            newOrder["type"] = "SELL"
            newOrder["id"] = orderIDs
            newOrder["date"] = idx
            newOrder["vol"] = volBTC
            newOrder["price"] = sellPrice
            orderIDs = orderIDs + 1
            balBTC = balBTC - volBTC
            orders.append(newOrder)
            msgPrint(
                "\u203C"
                + "New Order ["
                + str(orderIDs)
                + "]: SELL on "
                + str(sellPrice)
                + " volume: "
                + str(volBTC),
                True,
            )
        if mySymbols[2]["balance"] > volUSD:
            lQuantity = round((volUSD / buyPrice), 5)
            newOrder = order.copy()
            newOrder["type"] = "BUY"
            newOrder["id"] = orderIDs
            newOrder["date"] = idx
            newOrder["vol"] = lQuantity
            newOrder["price"] = buyPrice
            orderIDs = orderIDs + 1
            balUSD = balUSD - volUSD
            orders.append(newOrder)
            msgPrint(
                "\u203C"
                + "New Order ["
                + str(orderIDs)
                + "]: BUY on "
                + str(buyPrice)
                + " volume: "
                + str(lQuantity),
                True,
            )
    else:
        if oldOrd > 0:
            # rep = checkOldOrders(cfname, bot, openOrders)
            msgPrint(
                "Balance is not available to open orders. Check for old orders (older then "
                + str(oldOrd)
                + " days) to cleanup.",
                True,
            )
            # msgPrint(rep, True)

    if firstStart:
        firstStart = False
        strStart = (
            "Total start balance: "
            + str(round(myTotalBalance, 2))
            + " USD at price: "
            + str(round(currentBid, 2))
        )


def main(startPoint, finishPoint, count):
    global currentBid
    tik = 0
    stopMain = False
    for nowt in df.index:
        stopMain = False
        if nowt > finishPoint or nowt < startPoint:
            stopMain = True
            continue
        # print(nowt)
        start_date = nowt - timedelta(days=1)
        mask = (df15.index > start_date) & (df15.index <= nowt)
        checkOrders(nowt)
        # return 0
        tik = tik + 1
        if (tik == (step * 60)) and (nowt > startPoint):
            per = df15.loc[mask]
            mainProc(nowt, per)
            tik = 0
        if tik == (step * 60):
            tik = 0
    #        if nowt > pd.Timestamp(date(2022, 1, 3)): break
    if stopMain:
        return

    myOrderBalance = 0
    for j in range(0, len(orders)):
        myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) * currentBid)

    print(orders)
    print(" --------------------------------------------------------------------- ")
    print(strStart)
    print(" --------------------------------------------------------------------- ")
    print("Current Price:", round(currentBid, 2))
    print("balance BTC:", round(balBTC, 6), " in USD ", round(balBTC * currentBid, 2))
    print("balance USD:", round(balUSD, 2))
    print("balance Orders:", round(myOrderBalance, 2))
    print(
        "Total finish Balance:",
        round((balBTC * currentBid) + balUSD + myOrderBalance, 2),
    )

    totalSum = str(round((balBTC * currentBid) + balUSD + myOrderBalance, 2))
    csvRow = (
        ",".join(
            [
                str(period0),
                str(volBTC0),
                str(volUSD0),
                str(balBTC0),
                str(balUSD0),
                str(oldOrd0),
                str(maxUsage0),
                str(margin0),
                totalSum,
            ]
        )
        + "\n"
    )
    with open("document.csv", "a") as fd:
        fd.write(csvRow)

    with open("index.txt", "w") as fd:
        fd.write(str(count))


# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# shutil.copy("document_new.csv", "document.csv")

startPoint = pd.Timestamp(date(2020, 12, 30))
finishPoint = pd.Timestamp(date(2021, 6, 30))

periodArr = [720, 1440, 2160, 2880]
volBTCArr = [0.0005, 0.001, 0.0015, 0.002, 0.0025]
volUSDArr = [20.0, 30.0, 40.0, 50.0, 60.0]
oldOrdArr = [0, 3, 6, 9, 12]
maxUsageArr = [60, 70, 80]
marginArr = [0.005, 0.01, 0.015, 0.02, 0.025]
count = -1
for period in periodArr:
    period0 = period
    for volBTC in volBTCArr:
        volBTC0 = volBTC
        for volUSD in volUSDArr:
            volUSD0 = volUSD
            for oldOrd in oldOrdArr:
                oldOrd0 = oldOrd
                for maxUsage in maxUsageArr:
                    maxUsage0 = maxUsage
                    for margin in marginArr:
                        margin0 = margin
                        count = count + 1

                        with open("index.txt", "r") as fd:
                            if count < int(fd.read()):
                                continue

                        selyear = [
                            "2015",
                            "2016",
                            "2017",
                            "2018",
                            "2019",
                            "2020",
                            "2021",
                            "2022",
                        ]
                        for sy in selyear:
                            # sy="2022"
                            df = pd.read_pickle("./crypto_btcusdt" + sy + ".pkl")
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
                            step = 3
                            balBTC = 0.02  # [0.01,0.015,0.02,0.025,0.03]
                            balUSD = 550.0  # [150.0,200.0,250.0,300.0,350.0]
                            balBTC0 = balBTC
                            balUSD0 = balUSD
                            orders = []
                            complete = []

                            orderIDs = 0

                            currentBid = 0.0
                            skipprt = 0
                            firstStart = True
                            strStart = ""

                            order = {
                                "type": "BUY",
                                "date": startPoint,
                                "id": 0,
                                "vol": 0.0,
                                "price": 0.0,
                            }

                            start_time = time.time()
                            main(startPoint, finishPoint, count)
                            print("--- %s seconds ---" % (time.time() - start_time))
