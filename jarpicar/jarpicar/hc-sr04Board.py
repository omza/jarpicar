
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





# Main
#----------------------------------------------------------------
def main():
    logger.info('Hello from main()')
    try:
        logger.info('try')
    # ^C exit    
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt!')

    finally:
        logger.info('Good Bye!')    

if __name__ == "__main__":
    main()
