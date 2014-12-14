#!/usr/bin/python

import sqlite3, time

# Verbindung, Cursor erzeugen
connection = sqlite3.connect("Gaszaehler.db")
cursor = connection.cursor()

# SQL-Abfrage
sql = "SELECT * FROM gascounter"

# Absenden der SQL-Abfrage und
# Empfang des Ergebnisses
cursor.execute(sql)

# Ausgabe des Ergebnisses
# 'dsatz' entspricht den Spalten
for dsatz in cursor:
    #print dsatz[0], dsatz[1]
    print dsatz[0], time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(dsatz[1]))

# Verbindung beenden
connection.close()

