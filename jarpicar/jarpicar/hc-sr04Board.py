
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
logger = logging.getLogger(__name__)

# gpio
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

# Using a dictionary as a lookup table to give a name to gpio_function() return code  
pin_use = {0:"GPIO.OUT", 1:"GPIO.IN", 40:"GPIO.SERIAL", 41:"GPIO.SPI", 42:"GPIO.I2C", 43:"GPIO.HARD_PWM", -1:"GPIO.UNKNOWN"} 


# classes, modules
# --------------------------------------------------------------

class DistanceSensor(threading.Thread):

    #measure distance with HC-SR04 super sonic Board
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
 

    #overload constructor
    def __init__(self, PinTrigger, PinEcho, interval=1, group=None, target=None, name=None, args=None, kwargs=None):
        
        logger.info('Construct DistanceSensor Instance %s!', name)
        threading.Thread.__init__(self, group=None, target=None, name=name, args=args, kwargs=kwargs)
        DistanceSensor.setDeamon = True
        self.cancel = threading.Event()
        self.PinTrigger = PinTrigger
        self.PinEcho = PinEcho
        self.interval = interval
        self.flash = ('constructor: %s!', name)

        # gpio setup for pins
        gpio.setup(self.PinTrigger, gpio.OUT)
        gpio.setup(self.PinEcho, gpio.IN)
 
    # overload destructor
    def __del__(self):
        logger.info('destruct DistanceSensor Instance')
        gpio.cleanup([self.PinTrigger, self.PinEcho])    

    # Start & Stop
    def run(self):
        logger.info('Warm up Sensor...' + DistanceSensor.getName(self))
        gpio.output(self.PinTrigger, False)
        time.sleep(2)
        while not self.cancel.is_set():
            actualDistance = self.distance()
            logger.debug('Actual Distance is: %s!', actualDistance)
            self.cancel.wait(self.interval)


    def stop(self):
        logger.info('Stop...')
        self.cancel.set()
 

# Main
#----------------------------------------------------------------
def main():
    logger.info('Hello from main()')
    try:
        logger.info('try')
        FrontDDC = DistanceSensor(PinTrigger=18, PinEcho=24, name='FrontDDC', interval=1)
        #BackDDC = DistanceSensor(PinTrigger=12, PinEcho=25, name='BackDDC', interval=1)
        
        #logger.info(FrontDDC.isDeamon())
        FrontDDC.start()
        #BackDDC.start()
        while True:
            pass
    
        logger.info('endtry')

    # ^C exit    
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt!')
        FrontDDC.stop()
        #BackDDC.stop()

    finally:
        logger.info('Good Bye!')    

if __name__ == "__main__":
    main()
