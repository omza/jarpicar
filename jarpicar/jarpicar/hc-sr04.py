#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports, globals
# --------------------------------------------------------------

import time
import threading
import 
# gpio
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

# Using a dictionary as a lookup table to give a name to gpio_function() return code  
pin_use = {0:"GPIO.OUT", 1:"GPIO.IN", 40:"GPIO.SERIAL", 41:"GPIO.SPI", 42:"GPIO.I2C", 43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"} 

# user exeptions
# --------------------------------------------------------------


# classes, modules
# --------------------------------------------------------------

class DistanceSensor(threading._Timer):

    # methods
    def pincheck(self):
        bRet = True
        dummy = gpio.gpio_function(self.PinIn1)
        if dummy not in [-1,1]: 
            self.Log = ('PinIn1: %s!') % pin_use[dummy]
            bRet = False
        dummy = gpio.gpio_function(self.PinIn2)
        if dummy not in [-1,1]: 
           self.Log = ('PinIn2: %s!') % pin_use[dummy]
           bRet = False
        if self.PinEnable > 0:
            dummy = gpio.gpio_function(self.PinEnable)
            if dummy not in [-1,1]: 
                self.Log = ('PinEnable: %s!') % pin_use[dummy]
                bRet = False
        return bRet

    def distance(self):
        
        # start measure with trigger
        GPIO.output(self.PinTrigger, True)
	    time.sleep(0.00001)
	    GPIO.output(self.PinTrigger, False)

	    StartZeit = time.time()
	    StopZeit = time.time()

	    # speichere Startzeit
	    while GPIO.input(self.PinEcho) == 0:
		    StartZeit = time.time()

	    # speichere Ankunftszeit
	    while GPIO.input(self.PinEcho) == 1:
		    StopZeit = time.time()

	    # Zeit Differenz zwischen Start und Ankunft
	    TimeElapsed = StopZeit - StartZeit
	    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
	    # und durch 2 teilen, da hin und zurueck
	    distance = (TimeElapsed * 34300) / 2

	    return distance

    # constructur/destructor
    def __init__(self, PinTrigger, PinEcho, SensorName=None, Interval=None, function=None, args=None, kwargs=None): 
        
        threading._Timer.__init__(self, Interval=None, function=None, args=None, kwargs=None)
        threading._Timer.setName = SensorName
        self.Name = SensorName
        self.PinTrigger = PinTrigger
        self.PinEcho = PinEcho
        self.PinEnable = PinEnable
        self.Log = ('constructor: %s!') % self.Name
        self.Initialized = False
        
        # pins in use ?
        bCheck = self.pincheck()

        if bCheck:
            # gpio setup for pins
            gpio.setup(PinIn2, gpio.OUT, initial=0)
            gpio.setup(PinIn1, gpio.OUT, initial=0)
            if PinEnable > 0:
                gpio.setup(PinEnable, gpio.OUT, initial=0)
            self.Initialized = True


    def __del__(self):
        print ('destructor: %s!') % self.Name
        if self.PinEnable > 0:
            gpio.cleanup([self.PinIn1, self.PinIn2, self.PinEnable])
        else:
            gpio.cleanup([self.PinIn1, self.PinIn2])

# Main
# --------------------------------------------------------------

def main():
    print ('Hello World from Class module %s!') % __name__


    try:
       
        #GPIO Pins zuweisen
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24

        #Richtung der GPIO-Pins festlegen (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)        


    # ^C exit    
    except KeyboardInterrupt:
        print ('KeyboardInterrupt!')

    finally:
        print ('Good Bye!')



if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------
