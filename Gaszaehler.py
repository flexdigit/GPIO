#!/usr/bin/python

import RPi.GPIO as GPIO
import os, sys, sqlite3, time

GPIO.setmode(GPIO.BOARD)

# GPIO definieren
REED_gas    = 22    # pyhs. Pin 22 == GPIO 25
LED         = 18    # pyhs. Pin 18 == GPIO 24

# Variable Counter definieren
Counter = 0

# Pin 22 vom SoC als Input deklarieren und Pull-Up Widerstand aktivieren
GPIO.setup(REED_gas, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Pin 18 als Output deklarieren
GPIO.setup(LED, GPIO.OUT)
#GPIO.output(LED, 0)

localtime = time.asctime(time.localtime(time.time()))
print localtime

TagHeute=time.localtime()[2] # Tag des Monats
#print TagHeute
#MonatHeute=time.localtime()[1] # Monat des Jahres
#JahrHeute=time.localtime()[0] # Jahr

# define ISR which increments the counter only
def myInterrupt(channel):
    
    # access to globale variable
    global Counter

    # Counter um eins erhoehen
    Counter = Counter + 1
    #print "Counter " + str(Counter)
    
    # Switch LED on to see something happens here...
    GPIO.output(LED, 1)
    time.sleep(0.1)
    GPIO.output(LED, 0)
    
# Interrupt Event hinzufuegen.
# Pin 22, auf steigende Flanke reagieren und ISR "Interrupt" deklarieren
GPIO.add_event_detect(REED_gas, GPIO.RISING, callback = myInterrupt)

# Endlosschleife
try:
    while 1:
        time.sleep(300)
        #print "5 Sekunden sind abgelaufen. Ich schreibe in DB."
        
        # connect db
        connection = sqlite3.connect("Gaszaehler.db")
        # get the curser
        cursor = connection.cursor()
        # write data int DB
        timestamp = time.time()
        #print "Counter " + str(Counter), timestamp, time.ctime(timestamp)
        print "Counter " + str(Counter), time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(timestamp))
        
        cursor.execute("INSERT INTO gascounter(delta, timestamp) VALUES(%i, %f)"% (Counter, timestamp))
        connection.commit()
        # close DB connection
        connection.close()
        
        # reset Counter
        Counter = 0

except KeyboardInterrupt:
    print "\ndone"
    GPIO.cleanup()

