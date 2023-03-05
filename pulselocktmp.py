import RPi.GPIO as GPIO
import time
import logging
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
print("Lock is open")
time.sleep(5)
GPIO.output(12, GPIO.LOW)
print("Lock is closed")
time.sleep(3)
GPIO.cleanup()
