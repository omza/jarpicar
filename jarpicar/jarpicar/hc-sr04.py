#!/usr/bin/python
# -*- coding: utf-8 -*-

# credits
# --------------------------------------------------------------
# https://pymotw.com/2/threading/
# https://docs.python.org/2/library/threading.html




# imports, globals
# --------------------------------------------------------------

import time
import threading

#logging
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

# gpio
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

# Using a dictionary as a lookup table to give a name to gpio_function() return code  
pin_use = {0:"GPIO.OUT", 1:"GPIO.IN", 40:"GPIO.SERIAL", 41:"GPIO.SPI", 42:"GPIO.I2C", 43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"} 

# user exeptions
# --------------------------------------------------------------


# classes, modules
# --------------------------------------------------------------

class DistanceSensor(threading.Thread):

    # methods
    def pincheck(self):
        bRet = True
        dummy = gpio.gpio_function(self.PinTrigger)
        if dummy not in [-1,1.0]: 
            self.Log = ('PinIn1: %s!') % pin_use[dummy]
            bRet = False
        dummy = gpio.gpio_function(self.PinEcho)
        if dummy not in [-1,1]: 
           self.Log = ('PinIn2: %s!') % pin_use[dummy]
           bRet = False
        return bRet

    def distance(self):
        # start measure with trigger
        gpio.output(self.PinTrigger, True)
	    time.sleep(0.00001)
	    gpio.output(self.PinTrigger, False)

	    StartZeit = time.time()
	    StopZeit = time.time()

	    # speichere Startzeit
	    while gpio.input(self.PinEcho) == 0:
		    StartZeit = time.time()

	    # speichere Ankunftszeit
	    while gpio.input(self.PinEcho) == 1:
		    StopZeit = time.time()

	    # Zeit Differenz zwischen Start und Ankunft
	    TimeElapsed = StopZeit - StartZeit
	    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
	    # und durch 2 teilen, da hin und zurueck
	    distance = (TimeElapsed * 34300) / 2

	    return distance

    # constructur/destructor
    def __init__(self, PinTrigger, PinEcho, SensorName=None, interval=1): 
        
        threading.Thread.__init__(self, group=None, target=None, name=SensorName, args=(), kwargs={})
        self.
        self.cancel = threading.Event()
        self.PinTrigger = PinTrigger
        self.PinEcho = PinEcho
        self.interval = interval
        self.Log = ('constructor: %s!') % self.Name
        self.Initialized = False
        
        # pins in use ?
        bCheck = self.pincheck()

        if bCheck:
            # gpio setup for pins
            gpio.setup(self.PinTrigger, GPIO.OUT)
            gpio.setup(self.PinEcho, GPIO.IN)  
            self.Initialized = True


    def __del__(self):
        print ('destructor: %s!') % self
        gpio.cleanup([self.PinIn1, self.PinIn2])

    # Start & Stop

    def run(self):
        while not self.cancel.is_set():

            self.cancel.wait(self.int)


    def stop(self):
        self.cancel.set()

# Main
# --------------------------------------------------------------

def main():
    print ('Hello World from Class module %s!') % __name__


    try:
       
        #GPIO Pins zuweisen
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24

        #Richtung der GPIO-Pins festlegen (IN / OUT)
      


    # ^C exit    
    except KeyboardInterrupt:
        print ('KeyboardInterrupt!')

    finally:
        print ('Good Bye!')



if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------
