#!/usr/bin/python

import os, time, sqlite3, datetime, random

# find out what is "yesterday"
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')
#yesterday = yesterday.strftime('%Y-%m-%d')  # without time, only date

#--------------------------------------------------------------------
# Database Gaszahler.db contains three tables with the following
# columns:
#   - adjust          (counterstart, read, tstamp)
#   - dailyamount     (amount, tstamp)
#   - gascounter      (delta, tstamp)
#--------------------------------------------------------------------

# connect and create record cursor
connection = sqlite3.connect("/home/pi/GPIO/Gaszaehler.db")
cursor = connection.cursor()

# Query values from yesterday
# record von gestern, funzt so:
#sql = "SELECT * FROM gascounter WHERE tstamp >= date('now', '-1 days') AND tstamp <  date('now')"
sql = "SELECT SUM(delta) FROM gascounter WHERE tstamp >= date('now', '-1 days') AND tstamp <  date('now')"
cursor.execute(sql)

#i = 0                   # set control variable
#z = 0                   # set sum
for dsatz in cursor:    # summarize the found values from database
#    i+=1
#    z += dsatz[0]
#    print dsatz[1],"dsatz:",dsatz[0],"z:",z
    print "dsatz:",dsatz[0], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    
#print "\nFound",i,"items"
#print "\nSum:",z,"\n"


# write summarized values from yesterday into table "dailyamount"
sql = 'INSERT INTO dailyamount (amount,tstamp) VALUES(?,?)'
args = (dsatz[0],yesterday)
cursor.execute(sql, args)

# never forget this, if you want the changes to be saved
connection.commit()

# Verbindung beenden
connection.close()

