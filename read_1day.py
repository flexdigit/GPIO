#!/usr/bin/python

import sqlite3


# Connect DB create cursor
connection = sqlite3.connect("Gasmeter.db")
cursor = connection.cursor()

# SQL-Query
sql = """select tstamp, 
        case cast (strftime('%H', tstamp) as integer)
            when 00 then '0'
            when 01 then '1'
            when 02 then '2'
            when 03 then '3'
            when 04 then '4'
            when 05 then '5'
            when 06 then '6'
            when 07 then '7'
            when 08 then '8'
            when 09 then '9'
            when 10 then '10'
            when 11 then '11'
            when 12 then '12'
            when 13 then '13'
            when 14 then '14'
            when 15 then '15'
            when 16 then '16'
            when 17 then '17'
            when 18 then '18'
            when 19 then '19'
            when 20 then '20'
            when 21 then '21'
            when 22 then '22'
            when 23 then '23'
            when 24 then '24'
        else 'fehler' end,
        sum(tick) from gascounter where date(tstamp) = date('now', '-8 days')
        GROUP BY strftime('%H', tstamp)
        ORDER BY tstamp"""

# Values from today:
#select tstamp, sum(tick) from gascounter where date(tstamp) = date('now')

# from yesterday:
#select tstamp, sum(tick) from gascounter where date(tstamp) = date('now', '-1 days')


# dispatch the SQL-Query
cursor.execute(sql)

# dsatz[0] is tstamp (date + time)
# dsatz[1] is hour of the day (0, 1, 2,...)
# dsatz[2] is sum of the ticks
date_list = []     # will be the list for the date
dsatz_1_list = []  # will be list for hours per day
dsatz_2_list = []  # will be list for Gas consume
daily_amount = 0

for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    # tmp[0] is date
    # tmp[1] is time
    #print str(dsatz[0]) + " " + str(dsatz[1]) + " " + str(dsatz[2])
    #print str(tmp[0]) + " " + str(dsatz[1]) + " " + str(dsatz[2])
    date_list.append(tmp[0])
    dsatz_1_list.append(dsatz[1])
    dsatz_2_list.append(dsatz[2])

#print max(dsatz_2_liste)

# close DB connection
connection.close()

print "date     time ticks/h"
#for i in range(len(date_list)):
for i in range(len(date_list)):
    print date_list[i], dsatz_1_list[i], dsatz_2_list[i], dsatz_2_list[i]/2.0
    daily_amount += dsatz_2_list[i]/2.0
    

print "\nTagesverbrauch: ",daily_amount, "[* 0,01]"

# plot a diagramm
#hist(dsatz_1_liste, 23)
#show()


#sys.exit(0)

