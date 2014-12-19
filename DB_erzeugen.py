#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3, random

# Existenz feststellen
#if os.path.exists("Gaszaehler.db"):
#    print "File already exist!"
#    sys.exit(0)

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

# Tabelle erzeugen
#sql = "CREATE TABLE gascounter(delta INTEGER, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);"
sql = "CREATE TABLE gascounter (delta INTEGER, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"
cursor.execute(sql)

# und Testwerte eintragen
for i in range(30):
    make_entry('gascounter', 'delta')

# Tabelle erzeugen
sql = "CREATE TABLE dailyamount(amount FLOAT, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)"
cursor.execute(sql)

# und Testwerte eintragen
for i in range(30):
    make_entry('dailyamount', 'amount')

# never forget this, if you want the changes to be saved
connection.commit()
# Verbindung beenden
connection.close()
