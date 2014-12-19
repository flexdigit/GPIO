#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3, random, datetime

# Existenz feststellen
#if os.path.exists("Gaszaehler.db"):
#    print "File already exist!"
#    sys.exit(0)

# Startwert
Startwert = 12345.67890

today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')

def make_entry(table, spalte):
    sql = 'INSERT INTO %s (%s) VALUES(?)'%(table, spalte)
    x = random.randint(1,500)
    args = (x,)
    cursor.execute(sql, args)

# initialize random
random.seed()

# Verbindung zur Datenbank erzeugen
connection = sqlite3.connect("Gaszaehler.db")

# Datensatzcursor erzeugen
cursor = connection.cursor()

# Tabelle erzeugen für Zählerstartwert eintragen
sql = "CREATE TABLE adjust (counterstart FLOAT)"
cursor.execute(sql)
sql = 'INSERT INTO adjust (counterstart) VALUES(?)'
args = (Startwert,)
cursor.execute(sql, args)

# Tabelle erzeugen
sql = "CREATE TABLE gascounter (delta INTEGER, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"
cursor.execute(sql)

# und Testwerte eintragen
for i in range(10):
    make_entry('gascounter', 'delta')

# Tabelle erzeugen
sql = "CREATE TABLE dailyamount(amount FLOAT, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"
cursor.execute(sql)

# und Testwerte eintragen
for i in range(10):
    make_entry('dailyamount', 'amount')

# Zählerstartwert setzen    
sql = 'INSERT INTO dailyamount (amount, time) VALUES(?,?)'
args = ('99099',yesterday)
cursor.execute(sql, args)

    
# never forget this, if you want the changes to be saved
connection.commit()
# Verbindung beenden
connection.close()
