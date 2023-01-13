import RPi.GPIO as GPIO
import time
import logging
import subprocess


logfile = "/home/accessc/Documents/accessc.log"
#logging.basicConfig(filename="accessc.log", levell=logging.INFO)
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
 


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
#GPIO.output(12, GPIO.HIGH)
#print("Lock is open")
GPIO.output(12, GPIO.LOW)
GPIO.cleanup()

logging.info('Unlocked via pulse test')
print("Lock is scheduled to unlock")
