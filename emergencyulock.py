import RPi.GPIO as GPIO
import time
import logging
import subprocess


logfile = "/home/Documents/accessc.log"
#logging.basicConfig(filename="accessc.log", level=logging.INFO)
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
#GPIO.output(12, GPIO.HIGH)
#time.sleep(15)
print("gpio goes to low")
GPIO.output(12, GPIO.LOW)
logging.info('Lock via EMERGENCY')
GPIO.cleanup()
