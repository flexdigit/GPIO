#!/usr/bin/python

import sqlite3, time

# Verbindung, Cursor erzeugen
connection = sqlite3.connect("Gaszaehler.db")
cursor = connection.cursor()

# SQL-Abfrage
sql = "SELECT * FROM gascounter"
# Absenden der SQL-Abfrage
cursor.execute(sql)

# Ausgabe des Ergebnisses
# 'dsatz' entspricht den Spalten
print "Table: gascounter"
for dsatz in cursor:
    print dsatz[0], dsatz[1]
    #print dsatz[0], time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(dsatz[1]))

print
# Max aus dailyamount
sql = "SELECT MAX(delta) AS id FROM gascounter"    
cursor.execute(sql)
for dsatz in cursor:
    print "Max aus gascounter: %f" %dsatz[0]
print


# SQL-Abfrage
sql = "SELECT * FROM dailyamount"
# Absenden der SQL-Abfrage
cursor.execute(sql)

print "Table: dailyamount"
for dsatz in cursor:
    print dsatz[0], dsatz[1]
    
print
# Max aus dailyamount
sql = "SELECT MAX(amount) AS id FROM dailyamount"    
cursor.execute(sql)
for dsatz in cursor:
    print "Max aus dailyamount: %f" %dsatz[0]
print
# Verbindung beenden
connection.close()
