#!/usr/bin/python

import sys, sqlite3, os, shutil, re

# Start value for Gasmeter
startvalue = 8568.555

# Connect DB create cursor
connection = sqlite3.connect("Gasmeter.db")
cursor = connection.cursor()

# SQL-Query
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

# dispatch the SQL-Query
cursor.execute(sql)

# Build together the string for the new Gasmeter table
# dsatz[0] is tstamp (date + time)
# dsatz[1] is day of the week
# dsatz[2] is sum of the ticks
hlptable = "\nGasmeter:\n\n<table border=1 frame=hsides rules=all>\n"
for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    # tmp[0] is date
    # tmp[1] is time
    hlptable += "<tr>" + "\n"
    hlptable += "<td>" + str(tmp[0]) + "</td>" + "<td>" + str(dsatz[1]) + "</td>" + "<td>" + str(dsatz[2]) + "</td>" + "\n"
    hlptable += "</tr>" + "\n"
   
hlptable += "</table>" + "\n"
#print hlptable

# close DB connection
connection.close()

# Open the index.htm
# 'close' will called autom. at the end of the with block.
try:
    with open("index.htm") as infile:
        all_lines = infile.readlines()
except:
    print("Couldn't find file index.htm")
    sys.exit(0)

pattern = "</table>"
strhlp = ""

# Iterate thru all_line of index.htm and check
# if match patern can be found
for line in all_lines:
    strhlp += line
    
    # Regex applied to each line 
    match = re.search(pattern, line)
    if match:
        strhlp += hlptable

# Here old index.htm delete/rename or what else
# to be able to write new content (with new Gasmeter
# table) into index.htm.
# Or just overwrite the old index.htm?

        
# write into new file
with open("new_index.htm", 'w') as f:
     # write the lines
     f.writelines(strhlp)

