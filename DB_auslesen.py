#!/usr/bin/python

import sqlite3

#--------------------------------------------------------------------
# New database Gasmeter.db should contain two tables with the following
# columns:
#   - dailyamount     (amount, tstamp)
#   - gascounter      (tick, tstamp)
#--------------------------------------------------------------------

# connect and create record cursor
connection = sqlite3.connect("Gasmeter.db")
cursor = connection.cursor()

#--------------------------------------------------------------------
print "check table dailyamount for values"
sql = "SELECT * FROM dailyamount"
cursor.execute(sql)
for dsatz in cursor:
    print dsatz[0], dsatz[1]
print
#--------------------------------------------------------------------
print "check table gascounter for values"
sql = "SELECT * FROM gascounter"
cursor.execute(sql)
for dsatz in cursor:
    print dsatz[0], dsatz[1]
print

# disconnect database
connection.close()


