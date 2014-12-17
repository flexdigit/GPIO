#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, sqlite3

# Existenz feststellen
if os.path.exists("Gaszaehler.db"):
    print "File already exist!"
    sys.exit(0)

# Verbindung zur Datenbank erzeugen
connection = sqlite3.connect("Gaszaehler.db")

# Datensatzcursor erzeugen
cursor = connection.cursor()

# Tabelle erzeugen
#sql = "CREATE TABLE gascounter(delta INTEGER, timestamp FLOAT)"
sql = "CREATE TABLE gascounter(delta INTEGER, time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL);"
cursor.execute(sql)

# Verbindung beenden
connection.close()
