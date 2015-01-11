#!/usr/bin/python

import sqlite3, datetime, time, os

# If already exist, rename it
if os.path.exists("Gasmeter.db"):
    print "File already exist! Change name to Gasmeter.db_OLD"
    os.rename("Gasmeter.db", "Gasmeter.db_OLD")

#--------------------------------------------------------------------
# New database Gasmeter.db should contain two tables with the following
# columns:
#   - dailyamount     (amount, tstamp)
#   - gascounter      (tick, tstamp)
#--------------------------------------------------------------------

# Startwert
Startwert = 12345.67890

#--------------------------------------------------------------------
# Calculate yesterday
#
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')

# connect database and create record cursor
connection = sqlite3.connect("Gasmeter.db")
cursor = connection.cursor()

#--------------------------------------------------------------------
# create table gascounter and put two test values into
#
sql = """CREATE TABLE gascounter (tick INTEGER,
                                  tstamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"""
cursor.execute(sql)

sql = 'INSERT INTO gascounter (tick,tstamp) VALUES(?,?)'
args = (666,time.strftime("%Y-%m-%d %H:%M:%S"))
cursor.execute(sql, args)
sql = 'INSERT INTO gascounter (tick,tstamp) VALUES(?,?)'
args = (777,time.strftime("%Y-%m-%d %H:%M:%S"))
cursor.execute(sql, args)

#--------------------------------------------------------------------
# create table dailyamount and put two test values into
#
sql = """CREATE TABLE dailyamount(amount FLOAT,
                                  tstamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"""
cursor.execute(sql)

sql = 'INSERT INTO dailyamount (amount,tstamp) VALUES(?,?)'
args = (888,time.strftime("%Y-%m-%d %H:%M:%S"))
cursor.execute(sql, args)
sql = 'INSERT INTO dailyamount (amount,tstamp) VALUES(?,?)'
args = (999,time.strftime("%Y-%m-%d %H:%M:%S"))
cursor.execute(sql, args)

#--------------------------------------------------------------------
# Wert setzen und Datum von gestern eintragen
#
#sql = 'INSERT INTO dailyamount (amount, time) VALUES(?,?)'
#args = ('99099',yesterday)
#cursor.execute(sql, args)


# never forget this, if you want the changes to be saved
connection.commit()
# Verbindung beenden
connection.close()
