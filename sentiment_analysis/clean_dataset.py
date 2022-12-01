# Using readlines()
file = open("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets.csv",
            'r',
            encoding="UTF-8")


arr=file.split(",False\n'," 


lines = file.readlines()

lines[0] = "date" + (lines[0].replace(",user_verified,date",
                                      "Ǿ")).split("Ǿ")[1]

out = ""
count = 0
for line in lines:
    if (count > 0):
        try:
            tmpStr = line.replace(",False,202", "Ǿ").replace(",True,202", "Ǿ")
            line1 = "202" + tmpStr.split("Ǿ")[1]
            if (out == ""):
                out = line1
            else:
                out = out + "\n" + line1
        except Exception as e:
            print(e)

    count = count + 1

with open("./data/kaggle/bitcoin_tweets_v49/Bitcoin_tweets_new.csv",
          'a',
          encoding="UTF-8") as f:
    print(out, file=f)  # Python 3.x
