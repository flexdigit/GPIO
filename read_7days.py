#!/usr/bin/python

import sys, sqlite3, os, shutil, re

# Start value for Gasmeter
startvalue = 8568.555

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
    FROM gascounter WHERE tstamp BETWEEN DATE('now', '-7 days') AND DATE('now')
    GROUP BY strftime('%w', tstamp)
    ORDER BY tstamp"""

# Absenden der SQL-Abfrage
cursor.execute(sql)

# Ausgabe des Ergebnisses ('dsatz' entspricht den Spalten)
#print
hlptable = "Gasmeter:\n\n"
for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    #print tmp[0], dsatz[1], "\t", dsatz[2]
    t_string =  str(tmp[0]) + " " + str(dsatz[1]) + " " + str(dsatz[2]) + "\n"
    hlptable += t_string
    
print hlptable

# Verbindung beenden
connection.close()

# open the index.htm in that way. 'close' will called autom. at the end of the block.
try:
    with open("index.htm") as infile:
        all_lines = infile.readlines()
except:
    print("Couldn't find file index.htm")
    sys.exit(0)

pattern = "</table>"
strhlp = ""

# Iterate each line
for line in all_lines:
    strhlp += line
    
    # Regex applied to each line 
    match = re.search(pattern, line)
    
    if match:
        # Make sure to add \n to display correctly when we write it back
        #new_line = match.group() + '\n'
        #new_line = match.group()
        #print line
        strhlp += hlptable
        #print strhlp

with open("new_index.htm", 'w') as f:
     # go to start of file
     f.seek(0)
     # actually write the lines
     f.writelines(strhlp)


#for zeile in strhlp:
    #print (zeile.replace("\n",""))
#    print (zeile)
    
    
    
    
