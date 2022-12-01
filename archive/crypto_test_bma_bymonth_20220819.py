#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta, date
import mysql.connector

stop = False


def spinning_cursor():
    while True:
        for cursor in "|/-\\":
            yield cursor


def msgPrint(s, b):
    global skipprt
    skipprt = skipprt + 1
    if skipprt >= 0:
        # print(s)
        skipprt = 0


def checkOrders(idx):
    global orders, balUSD, balBTC, currentBid
    ids2remove = []
    sysstdbs = False
    # print("check orders ", idx)
    current = df.query("index == '" + str(idx) + "'")
    currentBid = float(current["close"])
    # print(currentBid)
    for chorder in orders:
        # chek for complete
        okBuy = (chorder["type"] == "BUY") and (currentBid <= chorder["price"])
        okSell = (chorder["type"]
                  == "SELL") and (currentBid >= chorder["price"])
        # print(chorder["type"], " || ", chorder["price"], " || ", currentBid)
        # print(okBuy, " - ", okSell)
        if okBuy:
            balBTC = balBTC + chorder["vol"]
            ids2remove.append(chorder["id"])
            if not sysstdbs:
                sys.stdout.write("\b")
                sysstdbs = True
            tord = datetime.strptime(str(chorder["date"]), "%Y-%m-%d %H:%M:%S")
            print("hit[" + str(tord) + "]!!!!!!!!!!!!!!!!!!!!!!!!!" +
                  chorder["type"] + "!!!!!!![" + str(chorder["vol"]) + "/" +
                  str(chorder["price"]) + "]")
        if okSell:
            balUSD = balUSD + (chorder["vol"] * chorder["price"])
            ids2remove.append(chorder["id"])
            if not sysstdbs:
                sys.stdout.write("\b")
                sysstdbs = True
            tord = datetime.strptime(str(chorder["date"]), "%Y-%m-%d %H:%M:%S")
            print("hit[" + str(tord) + "]!!!!!!!!!!!!!!!!!!!!!!!!!" +
                  chorder["type"] + "!!!!!!![" + str(chorder["vol"]) + "/" +
                  str(chorder["price"]) + "]")
        # check old
        if oldOrd > 0:
            tord = datetime.strptime(str(
                chorder["date"]), "%Y-%m-%d %H:%M:%S") + timedelta(days=oldOrd)
            tnow = datetime.strptime(str(current.index[0]),
                                     "%Y-%m-%d %H:%M:%S")
            #            print(tord, "     ", tnow)
            #            exit()
            if tnow >= tord:
                if not sysstdbs:
                    sys.stdout.write("\b")
                    sysstdbs = True
                print("hit!!!!!!!!!!!!!!!!!!!!!!!!!OLDORDER!!!!!!!")
                if chorder["type"] == "SELL":
                    balBTC = balBTC + chorder["vol"]
                    ids2remove.append(chorder["id"])
                else:
                    balUSD = balUSD + (chorder["vol"] * chorder["price"])
                    ids2remove.append(chorder["id"])

    for ids in ids2remove:
        idxO = False
        for z in orders:
            if z["id"] == ids:
                idxO = z
                break
        if idxO:
            orders.remove(idxO)


def mainProc(idx, klines):
    global orders, order, df, balBTC, balUSD, orderIDs, currentBid, firstStart, strStart
    # print("mainProc")
    mySymbols = {
        1: {
            "name": "BTC",
            "balance": 0,
            "tax": 0.1,
            "volume": 0.0015
        },
        2: {
            "name": "USD",
            "balance": 0,
            "tax": 0.1,
            "volume": 40.00
        },
    }

    mySymbols[1]["balance"] = balBTC
    mySymbols[2]["balance"] = balUSD

    current = df.query("index == '" + str(idx) + "'")
    currentBid = float(current["close"])
    print("[", idx, "]")
    myAvailableBalance = mySymbols[1]["balance"] * currentBid + mySymbols[2][
        "balance"]
    msgPrint(
        "Available Balance:\t" + str(round(myAvailableBalance, 2)) + " " +
        mySymbols[2]["name"],
        True,
    )

    # get orderlist and calculate orders balance
    myOrderBalance = 0
    for j in range(0, len(orders)):
        if orders[j]["type"] == "BUY":
            myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) *
                                               orders[j]["price"])
        else:
            myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) *
                                               currentBid)

    myTotalBalance = myAvailableBalance + myOrderBalance
    realPercentUsage = round(myOrderBalance / myTotalBalance, 2) * 100
    msgPrint(
        "Orders Balance \[" + str(len(orders)) + "]:\t" +
        str(round(myOrderBalance, 2)) + " " + "USD" + " (" +
        str(round(realPercentUsage, 2)) + "%) calc with current price: " +
        str(round(currentBid, 2)),
        True,
    )
    msgPrint("Total Balance:\t" + str(round(myTotalBalance, 2)) + " " + "USD",
             True)

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
        "Market is: *" + marketMove + mMove[idM] + "* \[" +
        str(round(nearByMAX, 2)) + " : " + str(round(nearByMIN, 2)) + "]",
        True,
    )

    sellPrice = round(maxPrice - maxPrice * margin, 2)
    buyPrice = round(minPrice + minPrice * margin, 2)

    if (sellPrice >
        (currentBid + (currentBid * margin))) and (buyPrice <
                                                   (currentBid -
                                                    (currentBid * margin))):
        msgPrint(
            "Recomended: Strategy 2 (small hall) SELL: " +
            str(round(sellPrice, 2)) + " BUY: " + str(round(buyPrice, 2)),
            True,
        )
    elif (byMAX) or (byMIN):
        sellPrice = round((currentBid * (1 + margin)), 2)
        buyPrice = round((currentBid - (currentBid * margin)), 2)
        msgPrint(
            "Recomended: Strategy 3 TRTTB (MAX: " + str(byMAX) + " | MIN: " +
            str(byMIN) + ") SELL: " + str(round(sellPrice, 2)) + " BUY: " +
            str(round(buyPrice, 2)),
            True,
        )
    else:
        sellPrice = round((maxPrice * (1 + margin)), 2)
        buyPrice = round((minPrice - (minPrice * margin)), 2)
        msgPrint(
            "Recomended: Strategy 1 (Big Hall). SELL: " +
            str(round(sellPrice, 2)) + " BUY: " + str(round(buyPrice, 2)),
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
                "\u203C" + "New Order [" + str(orderIDs) + "]: SELL on " +
                str(sellPrice) + " volume: " + str(volBTC),
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
                "\u203C" + "New Order [" + str(orderIDs) + "]: BUY on " +
                str(buyPrice) + " volume: " + str(lQuantity),
                True,
            )
    else:
        if oldOrd > 0:
            # rep = checkOldOrders(cfname, bot, openOrders)
            msgPrint(
                "Balance is not available to open orders. Check for old orders (older then "
                + str(oldOrd) + " days) to cleanup.",
                True,
            )
            # msgPrint(rep, True)

    if firstStart:
        firstStart = False
        strStart = ("Total start balance: " + str(round(myTotalBalance, 2)) +
                    " USD at price: " + str(round(currentBid, 2)))


def sprint(*args, end="\n", **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, end=end, file=open("result.txt", "a"))


def main():
    global currentBid
    saveBTCbal = balBTC
    saveUSDbal = balUSD
    # saveBTCvol = volBTC
    # saveUSDvol = volUSD
    tik = 0
    print("Start simulate of trading...")
    for nowt in df.index:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        ntcs = True
        start_date = nowt - timedelta(days=1)
        mask = (klines.index > start_date) & (klines.index <= nowt)
        checkOrders(nowt)
        # return 0
        tik = tik + 1
        if tik == (step * 60):
            per = klines.loc[mask]
            sys.stdout.write("\b")
            ntcs = False
            mainProc(nowt, per)
            tik = 0
        if ntcs:
            sys.stdout.write("\b")

    myOrderBalance = 0
    for j in range(0, len(orders)):
        if orders[j]["type"] == "BUY":
            myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) *
                                               orders[j]["price"])
        else:
            myOrderBalance = myOrderBalance + (float(orders[j]["vol"]) *
                                               currentBid)

    # sprint(orders)
    sprint(" -------------------NEW ANALYTIC RESULT FOR " + sy +
           "----------------------- ")
    sprint(
        "Settings:",
        "\nbalBTC=",
        saveBTCbal,
        "\nbalUSD=",
        saveUSDbal,
        "\noldOrder=",
        oldOrd,
        "\nmargin=",
        margin,
        "\nperiod=",
        step,
        "h",
        "\nklines=",
        per,
        # "min",
    )
    sprint(
        " --------------------------------------------------------------------- "
    )
    sprint(strStart)
    startBal = round((saveBTCbal * currentBid) + saveUSDbal, 2)
    sprint(
        " --------------------------------------------------------------------- "
    )
    sprint("Current Price:", round(currentBid, 2))
    sprint("balance BTC:", round(balBTC, 6), " in USD ",
           round(balBTC * currentBid, 2))
    sprint("balance USD:", round(balUSD, 2))
    sprint("balance Orders:", round(myOrderBalance, 2))
    finBal = round((balBTC * currentBid) + balUSD + myOrderBalance, 2)
    sprint("Start balance at current price:", startBal)
    sprint("Total finish Balance:", finBal)
    sprint("Total balance margin:", round((1 - (startBal / finBal)) * 100, 2),
           "%")

    cnx = mysql.connector.connect(
        user="dbuser",
        password="password",
        host="localhost",
        database="TradeBotDb",
    )
    cursor = cnx.cursor(buffered=True)
    query = (
        "UPDATE TableByMonths SET total_sum = %s, duration = %s, comb_status = %s "
        "where id = %s")
    # print(query)

    cursor.execute(
        query,
        (
            str(finBal),
            str(datetime.now() - start_time),
            "finished",
            id,
        ),
    )
    cnx.commit()
    cursor.close()
    cnx.close()


from crypto_settings_bma import *

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

selmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# selyear = [
#     "2014",
# ]
for sy in selyear:
    df0 = pd.read_pickle("./crypto_btcusdt" + sy + ".pkl")
    klines0 = pd.read_pickle("./crypto_btcusdt" + sy + "_" + per0 + ".pkl")
    for sm in selmonth:
        df = df0[df0.index.month == sm]
        klines = klines0[klines0.index.month == sm]
        startPrice = 0
        try:
            startPrice = (df.high.to_numpy()[0] + df.low.to_numpy()[0]) / 2
        except:
            print("ошибка!")
            continue
        for oldOrd in oldOrdArr:
            for margin in marginArr:
                for step in stepArr:
                    m = str(sm) + "*m*"
                    if m.__len__() < 5:
                        m = "0" + m
                    id = (str(sy) + "_" + m + "step" + str(step) + "oldord" +
                          str(oldOrd) + "margin" + str(margin) + "per" +
                          str(per0))
                    per = per0
                    balUSD = balOverall / 2
                    volUSD = balUSD / 20
                    balBTC = (balOverall - balUSD) / startPrice
                    volBTC = balBTC / 20

                    cnx = mysql.connector.connect(
                        user="dbuser",
                        password="password",
                        host="localhost",
                        database="TradeBotDb",
                    )
                    cursor = cnx.cursor(buffered=True)
                    query = "SELECT comb_status from TableByMonths where id = %s"
                    cursor.execute(
                        query,
                        (id, ),
                    )

                    nextCombination = False
                    for [comb_status] in cursor:
                        if comb_status == "processing" or comb_status == "finished":
                            nextCombination = True
                            break
                    cursor.close()
                    cnx.close()
                    if nextCombination:
                        continue

                    cnx = mysql.connector.connect(
                        user="dbuser",
                        password="password",
                        host="localhost",
                        database="TradeBotDb",
                    )
                    cursor = cnx.cursor(buffered=True)
                    query = ("INSERT INTO TableByMonths "
                             "(id, "
                             "sel_interval, "
                             "period, "
                             "step, "
                             "vol_btc, "
                             "vol_usd, "
                             "bal_btc, "
                             "bal_usd, "
                             "old_ord, "
                             "max_usage, "
                             "margin, "
                             "per, "
                             "total_sum, "
                             "duration, "
                             "comb_status) "
                             "VALUES "
                             "(%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s, "
                             "%s)")
                    cursor.execute(
                        query,
                        (
                            id,
                            str(sy) + "_" + m,
                            str(period),
                            str(step),
                            str(volBTC),
                            str(volUSD),
                            str(balBTC),
                            str(balUSD),
                            str(oldOrd),
                            str(maxUsage),
                            str(margin),
                            str(per),
                            "",
                            "",
                            "processing",
                        ),
                    )
                    cnx.commit()
                    cursor.close()
                    cnx.close()

                    spinner = spinning_cursor()

                    start_time = datetime.now()

                    orders = []
                    complete = []
                    orderIDs = 0
                    currentBid = 0.0
                    skipprt = 0
                    firstStart = True
                    strStart = ""

                    order = {
                        "type":
                        "BUY",
                        "date":
                        pd.Timestamp(
                            date(int(sy), sm, 1).__add__(timedelta(days=1))),
                        "id":
                        0,
                        "vol":
                        0.0,
                        "price":
                        0.0,
                    }

                    main()

                    end_time = datetime.now()
                    sprint("Duration: {}".format(end_time - start_time))
