
# hc-sr04Board.py
# --------------------------------------------------------------
# 


# credits & resources
# --------------------------------------------------------------
# https://pymotw.com/2/threading/
# https://docs.python.org/2/library/threading.html
# http://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
# https://pymotw.com/2/multiprocessing/basics.html
# https://docs.python.org/3/tutorial/errors.html
# https://de.wikipedia.org/wiki/Schallgeschwindigkeit


# imports, globals
# --------------------------------------------------------------
import time
import multiprocessing
import warnings

#logging
import logging
FORMAT = '%(asctime)s - %(processName)s - %(levelname)s - %(message)s'
log_level = logging.INFO

logFormat = logging.Formatter(FORMAT)
logHandler = logging.StreamHandler()
logHandler.setLevel(log_level)
logHandler.setFormatter(logFormat)

logger = multiprocessing.get_logger()
logger.setLevel(log_level)
logger.addHandler(logHandler)

# gpio
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

# User Exceptions
# --------------------------------------------------------------

class GpioPinUseError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        self.message = 'GPIO Warning: This Pin is already in use!'

# classes, modules
# --------------------------------------------------------------

class DistanceSensorProcess(multiprocessing.Process):
    
    #constructor
    def __init__(self, PinTrigger, PinEcho, Sensor=None, handler=None, *args,**kwargs):
        multiprocessing.Process.__init__(self, group=None, target=None, name=Sensor, *args,**kwargs)


    #destructor
    def __del__(self):
        pass


class DistanceSensor(object):
    
    #Sonic speed by tempetrature in cm/s
    tempsonicspeed = [[-25, 31591], [-20, 31909], [-15, 32223], [-10, 32535], [-5, 32844], [0, 33150], 
        [5, 33453], [10, 33754], [15, 34051], [20, 34346],  [25, 34639],  [30, 34929],  [35, 35217]]
    
    #measure of length
    measureoflength ={'m': 0.01, 'cm': 1, 'mm': 100}

    # gpio setup for HC-SR04 with warnings for pin use
    def _hcsr04_gpio_setup(self):
        
        # gpio Warnings Catch !!!
        # gpio setup for pins
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
           
            gpio.setup(self.PinTrigger, gpio.OUT)
            gpio.setup(self.PinEcho, gpio.IN)   
            
            for warning in w:
                 logger.warning(str(warning._category_name) + ': ' + str(warning.message))
                                  
                 if 'This channel is already in use' in str(warning.message):
                     raise GpioPinUseError
    

    # measure distance with HC-SR04 super sonic Board
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
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck            
        TimeElapsed = StopZeit - StartZeit
        distance = (TimeElapsed * 34300) / 2
        logger.debug('current distance is %3.2f', distance)
        return distance

    def warm_up(self):
        logger.info('Warm up Sensor...%s', self.SensorName)
        gpio.output(self.PinTrigger, False)
        time.sleep(2)

    def __init__(self, PinTrigger, PinEcho, Sensor=None, temp=20, measureoflenght='cm'):
        self.SensorName = Sensor
        self.PinTrigger = PinTrigger
        self.PinEcho = PinEcho

        self._hcsr04_gpio_setup()

        #calc distance temp and measurement factor
        
               
        logger.info('construct DistanceSensor %s.', self.SensorName)

    # destructor
    def __del__(self):
        gpio.cleanup([self.PinTrigger, self.PinEcho])
        logger.info('destruct DistanceSensor Instance %s.', self.SensorName)
    

# Main
#----------------------------------------------------------------

def main():
    logger.info('Hello from main()')

    # Handler
    def DDCHandler(DistanceSensor): 
        DistanceSensor.warm_up()
        while True:
            Distance = DistanceSensor.distance()
            if Distance < 5.0:
                logger.info('Dont you touch me! You are away %s cm in my %s!', Distance, DistanceSensor.SensorName)




         
    try:
        logger.info('Starting...')

        FrontSensor = DistanceSensor(PinTrigger=18,PinEcho=24,Sensor='jarpicar Frontsensor')
        FrontDDC = multiprocessing.Process(name='Front-DDC',target=DDCHandler, args=[FrontSensor])
        FrontDDC.daemon = True

        FrontDDC.start()       


        while True:
            pass

      
    except Exception as e:
        logger.exception(str(e.message))


    finally:
        logger.info('cleanup')

        FrontDDC.terminate()
        FrontDDC.join()
        del FrontSensor

        time.sleep(2)
        logger.info('Good Bye!')    

if __name__ == "__main__":
    main()



