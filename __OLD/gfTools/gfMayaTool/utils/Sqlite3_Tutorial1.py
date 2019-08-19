import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')

conn = sqlite3.connect('tutorial.db') # or (':memory:') to store in RAM
c = conn.cursor()


def createTable():
    c.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT NOCASE, keyword TEXT, value REAL NOT NULL)")
    # TEXT COLLATE NOCASE = convert to lowercase
    # TEXT COLLATE BINARY = compared using exact same characters
    # TEXT COLLATE RTRIM = same as binary plus ignoring white spaces
    # INTEGER PRIMARY KEY = auto increment and remains unique
    # INTEGER NOT NULL DEFAULT '0' = if is blank
    # INTEGER UNIQUE CHECK(comic_issn>0)= this number must be unique
    # FOREIGN KEY(character_id) REFERENCES identity(id) = reference primary key in another table


def dataEntry():
    c.execute("INSERT INTO stuffToPlot VALUES(12345, '2016-01-01', 'Python', 5)")
    conn.commit()
    c.close()
    conn.close()


def dynamicDataEntry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0, 10)
    # c.execute("INSERT INTO stuffToPlot VALUES (:unix, :datestamp, :keyword, :value)",
    #     {'unix': unix, 'datestamp': date, 'keyword': keyword, 'value': value})
    c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()
    with conn:
        c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
                  (unix, date, keyword, value))


def readFromDb():
    # c.execute("SELECT * FROM stuffToPlot")
    # c.execute("SELECT * FROM stuffToPlot WHERE value=3 AND keyword='Python'")
    # c.execute("SELECT * FROM stuffToPlot WHERE unix > 1525800242.298191")
    c.execute("SELECT keyword, unix, value, datestamp FROM stuffToPlot WHERE unix > 1525800242.298191")
    # data = c.fetchall() # or c.fetchone() or c.fetchmany()
    # print(data)
    for row in c.fetchall():
        print(row[3])


def graphData():
    c.execute("SELECT unix, value FROM stuffToPlot")
    dates = []
    values = []
    for row in c.fetchall():
        # print(row[0])
        # print(datetime.datetime.fromtimestamp(row[0]))
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])
    plt.plot_date(dates, values, '-')
    plt.show()


def deleteAndUpdate():
    c.execute("SELECT * FROM stuffToPlot")
    [print(row) for row in c.fetchall()]
    # print("\n")
    # c.execute("UPDATE stuffToPlot SET value = 99 WHERE value = 8")
    # conn.commit()
    # c.execute("SELECT * FROM stuffToPlot")
    # [print(row) for row in c.fetchall()]
    c.execute("DELETE FROM stuffToPlot WHERE value = 99")
    conn.commit()
    print(60*'#')
    c.execute("SELECT * FROM stuffToPlot")
    [print(row) for row in c.fetchall()]


# createTable()
# dataEntry()
# for i in range(10):
#     dynamicDataEntry()
#     time.sleep(1)
# readFromDb()
# graphData()
deleteAndUpdate()
c.close()
conn.close()
