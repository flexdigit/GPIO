#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3, random, time

# Verbindung zur Datenbank erzeugen
connection = sqlite3.connect("Gaszaehler.db")
cursor = connection.cursor()

# initialize random
random.seed()

try:
    while 1:
        # get random integer value between 1 and 1000
        x = random.randint(1,1000)
        print x
        
        sql = 'INSERT INTO gascounter (delta) VALUES (?)'
        args = (x,)
        cursor.execute(sql, args)
        #cursor.execute("INSERT INTO gascounter (delta) VALUES ("%i")", x)
        #cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
        
        time.sleep(0.5)

except KeyboardInterrupt:
    # never forget this, if you want the changes to be saved
    connection.commit()

    # Verbindung beenden
    connection.close()

    print "\nstopped"
    
