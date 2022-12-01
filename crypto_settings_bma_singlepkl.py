#!/usr/bin/python3
import pandas as pd
from datetime import datetime, timedelta, date

# per = '30'
# step = 3
# period = 1440
# volBTC = 0.0015
# volUSD = 40.0
# balBTC = 0.03
# balUSD = 250.0
# oldOrd = 25
# maxUsage = 70
# margin = 0.015

startPoint = date(2015, 1, 1)
# finishPoint = date(2022, 7, 26)
finishPoint = date(2015, 1, 2)

period = 1440
balOverall = 500
maxUsage = 70
oldOrdArr = [25, 12, 5, 1]
marginArr = [0.01, 0.015, 0.02, 0.025]
stepArr = [1, 3, 5, 7]
per0 = "30"

dbName = "MainTab"
