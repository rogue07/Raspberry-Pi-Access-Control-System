#/usr/bin/python3

# ram persaud
# 14 jan, 2023
# This file should live in the Documents folder.


import RPi.GPIO as GPIO
import time
import logging
import subprocess


# set up some logging
logfile = "~/Documents/accessc.log"
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
print("Lock is scheduled to open")
logging.info('Locked via pulse test')
#time.sleep(5)
#GPIO.output(12, GPIO.LOW)
#print("Lock is closed")
#time.sleep(3)
#GPIO.cleanup()
