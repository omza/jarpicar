#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports, globals
# --------------------------------------------------------------

#time
import time

# gpio
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

# Using a dictionary as a lookup table to give a name to gpio_function() return code  
pin_use = {0:"GPIO.OUT", 1:"GPIO.IN", 40:"GPIO.SERIAL", 41:"GPIO.SPI", 42:"GPIO.I2C", 43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"} 

# user exeptions
# --------------------------------------------------------------


# classes, modules
# --------------------------------------------------------------

class Motor:

    # methods
    
    # pins in use ?
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

    def forward(self):
        gpio.output(self.PinIn1, 1)
        gpio.output(self.PinIn2, 0)
        if self.PinEnable > 0:
            gpio.output(self.PinEnable, 1)
        self.Log = ('foreward: %s!') % self.Name

    def backward(self):
        self.Log = ('backwards: %s!') % self.Name
        gpio.output(self.PinIn1, 0)
        gpio.output(self.PinIn2, 1)
        if self.PinEnable > 0:
            gpio.output(self.PinEnable, 1)

    def stop(self):
        self.Log = ('break: %s!') % self.Name
        gpio.output(self.PinIn1, 0)
        gpio.output(self.PinIn2, 0)
        if self.PinEnable > 0:
            gpio.output(self.PinEnable, 0)

    # constructur/destructor
    def __init__(self, MotorName, PinIn1, PinIn2, PinEnable = 0): 
        # Name
        self.Name = MotorName
        self.PinIn1 = PinIn1
        self.PinIn2 = PinIn2
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



class PWMMotor(Motor):

    # names
    PwmMaxDutyCycle = 95.0

    # methods
    def fullspeed(self):
        self.PwmDutyCycle = self.PwmMaxDutyCycle
        self.MotorPwm.ChangeDutyCycle(self.PwmDutyCycle)
        self.Log = ('%s full speed by %s dutycycle!') % (self.Name, self.PwmDutyCycle)

    def halfspeed(self):
        self.PwmDutyCycle = self.PwmMaxDutyCycle / 2
        self.MotorPwm.ChangeDutyCycle(self.PwmDutyCycle)
        self.Log = ('%s half speed by %s dutycycle!') % (self.Name, self.PwmDutyCycle)

    def slowly(self):
        self.PwmDutyCycle = self.PwmMaxDutyCycle / 4
        self.MotorPwm.ChangeDutyCycle(self.PwmDutyCycle)
        self.Log = ('%s slowly by %s dutycycle!') % (self.Name, self.PwmDutyCycle)

    def accelerate(self):
        self.Log = ('%s accerlerate by %s dutycycle!') % (self.Name, self.PwmDutyCycle)
        if self.PwmDutyCycle < self.PwmMaxDutyCycle:
            self.PwmDutyCycle = self.PwmMaxDutyCycle/10 + self.PwmDutyCycle            
            if self.PwmDutyCycle > self.PwmMaxDutyCycle:
                self.PwmDutyCycle = self.PwmMaxDutyCycle
            elif self.PwmDutyCycle < self.PwmMaxDutyCycle / 4:
                self.PwmDutyCycle = self.PwmMaxDutyCycle / 4
            self.MotorPwm.ChangeDutyCycle(self.PwmDutyCycle)
            

    def slowdown(self):
        self.Log = ('%s break by %s dutycycle!') % (self.Name, self.PwmDutyCycle)
        if self.PwmDutyCycle > 0:
            self.PwmDutyCycle = self.PwmDutyCycle - self.PwmMaxDutyCycle/10             
            if self.PwmDutyCycle < 0:
                self.PwmDutyCycle = 0
            self.MotorPwm.ChangeDutyCycle(self.PwmDutyCycle)
            

    # constructur/destructor
    def __init__(self, MotorName, PinIn1, PinIn2, PinEnable, pwmFrequency): 
        
        # attributes
        self.Name = MotorName
        self.Log = ('constructor: %s!') % self.Name
        self.PinIn1 = PinIn1
        self.PinIn2 = PinIn2
        self.PinEnable = PinEnable
        self.PwmFrequency = pwmFrequency
        self.PwmDutyCycle = self.PwmMaxDutyCycle
        self.Initialized = False
        
        # pins in use ?
        bCheck = self.pincheck()

        if bCheck:
            # gpio setup for pins
            gpio.setup(self.PinIn2, gpio.OUT, initial=0)
            gpio.setup(self.PinIn1, gpio.OUT, initial=0)
            gpio.setup(self.PinEnable, gpio.OUT, initial=0)
        
            #gpio software pwm
            self.MotorPwm = gpio.PWM(self.PinEnable,self.PwmFrequency)
            self.MotorPwm.start(self.PwmDutyCycle)
            self.Initialized = True


  
    def __del__(self):
        print ('destructor: %s!') % self.Name
        #self.MotorPwm.stop()
        gpio.cleanup([self.PinIn1, self.PinIn2, self.PinEnable])



class Stepper:

    def __init__(self):
        print ("constructor")
 
    def __del__(self):
        print ("destructor")
        
           
class Servo:

    def __init__(self):
        print ("constructor")
 
    def __del__(self):
        print ("destructor")
    
# Main
# --------------------------------------------------------------

def main():
    print ('Hello World from Class module %s!') % __name__


    try:
        
        engine = PWMMotor("Engine",17,27,4,100)
        
        while(True):
        

            # Engine
            engine.slowly()
            engine.forward()
            time.sleep(2)

            engine.halfspeed()
            engine.forward()
            time.sleep(2)

            engine.fullspeed()
            engine.forward()
            time.sleep(2)
        
            engine.backward()
            time.sleep(2)

            engine.stop()
            time.sleep(1)

    # ^C exit    
    except KeyboardInterrupt:
        print ('KeyboardInterrupt!')

    finally:
        print ('Good Bye!')



if __name__ == "__main__":
    main()

# EOF
# --------------------------------------------------------------
