#!/usr/bin/python3
import pandas as pd
import mysql.connector

per = "30"

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

selmonth = range(13)[1:]
# selyear = [
#     "2014",
# ]

optimalComb = list()
for sy in selyear:
    for sm in selmonth:

        m = str(sm) + "*m*"
        if m.__len__() < 5:
            m = "0" + m

        selInterval = str(sy) + "_" + m

        cnx = mysql.connector.connect(
            user="dbuser",
            password="password",
            host="localhost",
            database="TradeBotDb",
        )
        cursor = cnx.cursor(buffered=True)
        query = "SELECT id, sel_interval, period, step, vol_btc, vol_usd, bal_btc, bal_usd, old_ord, max_usage, margin, per, current_price, start_sum, total_sum, bal_margin, duration from TableByMonths where sel_interval = %s order by total_sum desc limit 0,1"
        cursor.execute(
            query,
            (selInterval, ),
        )
        for (
                id,
                sel_interval,
                period,
                step,
                vol_btc,
                vol_usd,
                bal_btc,
                bal_usd,
                old_ord,
                max_usage,
                margin,
                per,
                current_price,
                start_sum,
                total_sum,
                bal_margin,
                duration,
        ) in cursor:
            optimalComb.append([
                id,
                sel_interval,
                period,
                step,
                vol_btc,
                vol_usd,
                bal_btc,
                bal_usd,
                old_ord,
                max_usage,
                margin,
                per,
                current_price,
                start_sum,
                total_sum,
                bal_margin,
                duration,
            ])
        cursor.close()
        cnx.close()

for arr in optimalComb:
    found = False
    cnx = mysql.connector.connect(
        user="dbuser",
        password="password",
        host="localhost",
        database="TradeBotDb",
    )
    cursor = cnx.cursor(buffered=True)
    query = "SELECT id from Results where id = %s"
    cursor.execute(
        query,
        (arr[0], ),
    )
    for (id, ) in cursor:
        found = True
    cursor.close()
    cnx.close()
    if found:
        continue

    cnx = mysql.connector.connect(
        user="dbuser",
        password="password",
        host="localhost",
        database="TradeBotDb",
    )
    cursor = cnx.cursor(buffered=True)
    query = ("INSERT INTO Results "
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
             "current_price, "
             "start_sum, "
             "total_sum, "
             "bal_margin, "
             "duration) "
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
             "%s, "
             "%s, "
             "%s)")
    cursor.execute(
        query,
        (
            arr[0],
            arr[1],
            arr[2],
            arr[3],
            arr[4],
            arr[5],
            arr[6],
            arr[7],
            arr[8],
            arr[9],
            arr[10],
            arr[11],
            arr[12],
            arr[13],
            arr[14],
            arr[15],
            arr[16],
        ),
    )
    cnx.commit()
    cursor.close()
    cnx.close()
