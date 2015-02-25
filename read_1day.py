#!/usr/bin/python

import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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
        sum(tick) from gascounter where date(tstamp) = date('now', '-9 days')
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
date_list        = []     # will be the list for the date
h_per_day_list   = []  # will be list for hours per day
Gas_consume_list = []  # will be list for Gas consume
daily_amount = 0

for dsatz in cursor:
    tmp = dsatz[0].split(" ")
    # tmp[0] is date
    # tmp[1] is time
    #print str(dsatz[0]) + " " + str(dsatz[1]) + " " + str(dsatz[2])
    #print str(tmp[0]) + " " + str(dsatz[1]) + " " + str(dsatz[2])
    date_list.append(tmp[0])
    h_per_day_list.append(dsatz[1])
    Gas_consume_list.append(dsatz[2])

#print max(dsatz_2_liste)

# close DB connection
connection.close()

print "\nDay: ",date_list[0]
#for i in range(len(date_list)):
for i in range(len(date_list)):
    print h_per_day_list[i], Gas_consume_list[i]/2.0
    daily_amount += Gas_consume_list[i]/2.0
    
print "\nticks:          ",daily_amount, "[ticks]"
daily_amount = daily_amount * 0.01

print "Tagesverbrauch: ",daily_amount, "[m^3]"

"""
plot a diagramm

"""
ind = np.arange(len(h_per_day_list))
x = h_per_day_list
y = Gas_consume_list
width = 0.8
p = plt.bar(ind, y, width, color='g')

plt.ylabel('Gas consumption [m^3]')
plt.title('Gas consumption per one day')
#plt.xticks(x)
#plt.legend( (p[0]), ('[m^3]') )

plt.show()

