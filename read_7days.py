#!/usr/bin/python

import sqlite3, time

# Verbindung, Cursor erzeugen
connection = sqlite3.connect("Gasmeter.db")
cursor = connection.cursor()

# SQL-Abfrage
sql = """SELECT tstamp,
    CASE CAST (strftime('%w', tstamp) as integer)
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
        WHEN 0 THEN 'Sunday'
        ELSE 'fehler' END,
    SUM(tick)
    FROM gascounter WHERE tstamp BETWEEN DATE('now', '-7 days') AND DATE('now', '+1 days')
    GROUP BY strftime('%w', tstamp)
    ORDER BY tstamp"""

# Absenden der SQL-Abfrage
cursor.execute(sql)

# Ausgabe des Ergebnisses ('dsatz' entspricht den Spalten)
print
for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    print tmp[1], dsatz[1], "\t", dsatz[2]

# Verbindung beenden
connection.close()

