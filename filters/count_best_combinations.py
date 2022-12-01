import mysql.connector

intervals = {
    'неделя': '%*w*',
    'месяц': '%*m*',
    'квартал': '%*q*',
    'полугодие': '%*hy*',
    'год': '%*y*'
}

for interval in intervals:
    with open('./filters/%s.csv' % (interval), 'a', encoding="UTF-8") as f:
        print("interval,step,old_ord,margin,per,count", file=f)  # Python 3.x

    combSet = dict()

    cnx = mysql.connector.connect(
        user="dbuser",
        password="password",
        host="localhost",
        database="TradeBotDb",
    )
    cursor = cnx.cursor(buffered=True)
    query = "SELECT step, old_ord, margin, per from Results where sel_interval like %s"
    cursor.execute(
        query,
        (intervals[interval], ),
    )
    for (
            step,
            old_ord,
            margin,
            per,
    ) in cursor:
        comb = str(step) + ";" + str(old_ord) + ";" + str(margin) + ";" + str(
            per)
        if combSet.__contains__(comb) == False:
            combSet[comb] = 1
        else:
            combSet[comb] = combSet[comb] + 1
    cursor.close()
    cnx.close()

    for comb in combSet:
        params = comb.split(";")
        with open('./filters/%s.csv' % (interval), 'a', encoding="UTF-8") as f:
            print("%s,%s,%s,%s,%s,%s" % (interval, params[0], params[1],
                                         params[2], params[3], combSet[comb]),
                  file=f)  # Python 3.x
