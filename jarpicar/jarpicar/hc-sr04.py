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
            logger.debug('PinTrigger in use: %s!', pin_use[dummy])
            self.flash = ('PinTrigger in use: %s!') % pin_use[dummy]
            bRet = False
        
        dummy = gpio.gpio_function(self.PinEcho)
        if dummy not in [-1,1]: 
            logger.debug('PinEcho in use: %s!', pin_use[dummy])
            self.flash = ('PinEcho in use: %s!') % pin_use[dummy]
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
        logger.info('constructor: %s!', SensorName)
        threading.Thread.__init__(self, group=None, target=None, name=SensorName, args=(), kwargs={})
        threading.Thread.setDaemon(self,True)
        self.cancel = threading.Event()
        self.PinTrigger = PinTrigger
        self.PinEcho = PinEcho
        self.interval = interval
        self.flash = ('constructor: %s!', SensorName)
        self.Initialized = False
        
        # pins in use ?
        bCheck = self.pincheck()

        if bCheck:
            # gpio setup for pins
            gpio.setup(self.PinTrigger, GPIO.OUT)
            gpio.setup(self.PinEcho, GPIO.IN)  
            self.Initialized = True


    def __del__(self):
        logger.info('destructor: %s!', threading.Thread.getName(self))
        gpio.cleanup([self.PinTrigger, self.PinEcho])

    # Start & Stop
    def run(self):
        while not self.cancel.is_set():
            actualDistance = self.distance()
            logger.info('Actual Distance is: %s!', actualDistance)
            self.cancel.wait(self.interval)


    def stop(self):
        self.cancel.set()

# Main
# --------------------------------------------------------------

def main():
    
    logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)
    logger = logging.getLogger(__name__)

    logger.info('Hello from main()')

    try:
        FrontDDC = DistanceSensor(PinTrigger=18, PinEcho=24, SensorName='FrontDDC', interval=0.1)
        FrontDDC.start()
        time.sleep(60)
        FrontDDC.stop()

    # ^C exit    
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt!')

    finally:
        logger.info('Good Bye!')

if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------