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
hlptable = "\nGasmeter:\n\n<table border=2 frame=hsides rules=all>\n"
hlptable += "<tr>\n"
hlptable += """<td align="center">Date</td><td align="center">Day</td><td align="center">m&sup3;</td>"""
hlptable += "</tr>"

for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    # tmp[0] is date
    # tmp[1] is time
    print tmp[0], dsatz[1], dsatz[2]
    hlptable += "<tr>" + "\n"
    hlptable += "<td>" + str(tmp[0]) + "</td>" + "<td>" + str(dsatz[1]) + "</td>" + "<td>" + str(dsatz[2]) + "</td>" + "\n"
    hlptable += "</tr>" + "\n"
   
hlptable += "</table>\n\n\n"
hlptable += "</body>\n"
hlptable += "</html>\n"

#print hlptable

# close DB connection
connection.close()

# Open the index.htm
try:
    with open("index.htm") as infile:
        all_lines = infile.readlines()
except:
    print("Couldn't find file index.htm")
    sys.exit(1)

pattern = "</table>"
strhlp = ""

# Iterate thru all_line of index.htm and check
# if match pattern can be found
for line in all_lines:
    strhlp += line
    
    # Regex applied to each line 
    match = re.search(pattern, line)
    if match:
        strhlp += hlptable              # If found add new table to the string (contains entire file)
        break                           # and break for loop

# Backup existing index.htm in 2 steps
# 1. Delete already backuped file:
if os.path.exists("index_OLD.htm"):
    os.remove("index_OLD.htm")
# 2. Backup the index.htm file:
if os.path.exists("index.htm"):
    print "File already exist!"
    print "Will copy and renamed to index_OLD.htm"
    #os.rename("index.htm", "index_OLD.htm")        # not good...
    shutil.copy("index.htm", "index_OLD.htm")

# write into new file
#with open("new_index.htm", 'w') as f:
with open("index.htm", "w") as fh:
     # write the lines
     fh.writelines(strhlp)


#sys.exit(0)
