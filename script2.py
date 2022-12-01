import pandas as pd

import sys
from datetime import datetime, timedelta, date
import mysql.connector

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
# selyear = [
#     "2014",
# ]
per = "30"
for sy in selyear:
    for oldOrd in oldOrdArr:
        for margin in marginArr:
            for step in stepArr:
                cnx = mysql.connector.connect(
                    user="dbuser",
                    password="Qwerty_123",
                    host="localhost",
                    database="TradeBotDb",
                )
                cursor = cnx.cursor()
                query = ("UPDATE MainTable0 SET id = %s, duration = %s "
                         "where sel_interval = %s and "
                         "step = %s and "
                         "old_ord = %s and "
                         "margin = %s and "
                         "per = %s")

                cursor.execute(
                    query,
                    (
                        str(sy) + "step" + str(step) + "oldord" + str(oldOrd) +
                        "margin" + str(margin) + "per" + str(per),
                        "",
                        str(sy),
                        str(step),
                        str(oldOrd),
                        str(margin),
                        str(per),
                    ),
                )
                cnx.commit()
                cursor.close()
                cnx.close()
