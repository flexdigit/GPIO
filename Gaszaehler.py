#!/usr/bin/python

import RPi.GPIO as GPIO
import os, sys, sqlite3, time

GPIO.setmode(GPIO.BOARD)

# define GPIOs
REED_gas    = 22    # pyhs. Pin 22 == GPIO 25
LED         = 18    # pyhs. Pin 18 == GPIO 24

# define Counter
Counter = 0
# define Merker
Merker = 0

# define Pin 22 as input and activate Pull-Up resistor
GPIO.setup(REED_gas, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# define Pin 18 as Output
GPIO.setup(LED, GPIO.OUT)
#GPIO.output(LED, 0)

localtime = time.asctime(time.localtime(time.time()))
print localtime

#------------------------------------------------------------
# define ISR which increments the counter only
def myInterrupt(channel):

    # access to globale variable
    global Counter

    # increase Counter by one
    Counter = Counter + 1
    #print "Counter " + str(Counter)

    # Switch LED on to see something happens here...
    GPIO.output(LED, 1)
    time.sleep(0.1)
    GPIO.output(LED, 0)

#------------------------------------------------------------
# add interrupt event on Pin 22
# react as rising edge, declare ISR "myInterrupt"
GPIO.add_event_detect(REED_gas, GPIO.RISING, callback = myInterrupt)

#--------------------------------------------------------------------
# Database Gaszahler.db contains three tables with the following
# columns:
#   - adjust          (counterstart, read, tstamp)
#   - dailyamount     (amount, tstamp)
#   - gascounter      (delta, tstamp)
#--------------------------------------------------------------------

try:
    # infinite loop
    while 1:
        #------------------------------------------------------------
        # Check flag (Merker) if after last 5 minutes the counter had
        # an uneven number the division by 2 lost one counter value.
        # Therefore we increase the counter by one.
        if Merker == 1:
            Counter += 1

        #------------------------------------------------------------
        # Hier vielleicht aus der Datenbank anfragen wie lange gewartet werden soll?
        # Extra Tabelle? "idle_t" mit Spalte "delay"
        #------------------------------------------------------------

        time.sleep(300) # wait for 5 minutes
        #print "5 Sekunden sind abgelaufen. Ich schreibe in DB."

        #------------------------------------------------------------
        # Reed contact counts 2 time per one rotation (at 1 and 9).
        # So we have to divide the Counter by 2.
        # But first we have to check if the Counter value is uneven. If so
        # we will lose one Counter-value thru division. Therefore we save this
        # in "Merker" with "= 1" for the next five minutes.
        if Counter%2 == 1:
            Merker = 1      # uneven
        else:
            Merker = 0      # even

        Counter = Counter/2

        # print Counter and timestamp to console
        print "Counter " + str(Counter), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        #------------------------------------------------------------
        # connect and create record cursor
        connection = sqlite3.connect("Gaszaehler.db")
        cursor = connection.cursor()

        # write Counter value + timestamp into table gascounter
        #cursor.execute("INSERT INTO gascounter(delta, tstamp) VALUES(%i, %s)"% (Counter, time.strftime("%Y-%m-%d %H:%M:%S")))
        #connection.commit()

        # different method to write values into a database
        sql = 'INSERT INTO gascounter (delta, tstamp) VALUES(?,?)'
        args = (Counter,time.strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(sql, args)
        connection.commit()
        connection.close()

        #------------------------------------------------------------
        # reset Counter for next 5 minutes
        Counter = 0

except KeyboardInterrupt:
    print "\nInterrupted by KeyboardInterrupt\n"
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()           # clean up GPIO on normal exit


