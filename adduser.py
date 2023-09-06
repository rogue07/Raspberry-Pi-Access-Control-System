#!/amon Persaud
#10 sep 2022
#My attempt at an access control system.

import pdb
import platform
import logging
import os 
import time
import sys
from adafruit_blinka.microcontroller.bcm283x import *
import board
import subprocess
import select
import keyboard
import mysql.connector
import RPi.GPIO as GPIO
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from sh import tail
from datetime import datetime
from crontab import CronTab
import os.path


if platform.system() == 'Linux' and platform.machine().startswith('arm'):
# Code for Raspberry Pi
    print("Is a pi")
    import RPi.GPIO as GPIO
    # rest of your code
else:
    quit()    

# Log to accessc.log
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

print("Connection to database")
print ("")
mydb = mysql.connector.connect(
    host="localhost",
    user="accessc",
    password="abcd",
    database="codedb"
)

print("Connected to database")

print("Taking fname & lname arguments")
print("")
# Get command line arguments
fname = sys.argv[1]
lname = sys.argv[2]
#fname = "bob"
#lname = "marley"

print("Arguments fname & lname have been ingested")

# Add user and associate a card with them

print("")
print("")

print("Enable spi")
spi = board.SPI()
print("Enable cs_pin")
cs_pin = DigitalInOut(board.D5)
print("Enable pn532")
exit()


pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()
print("Waiting for NFC card...")
time.sleep(1)

while True:
    time.sleep(1.2)
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue
    else:
        print("Found card with UID:", [hex(i) for i in uid])
        newCard = [hex(i) for i in uid]

    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M")

    mycursor = mydb.cursor()

    print("Connected")
    print(newCard)
    print(today)

    mycursor.execute(f'SELECT EXISTS(SELECT * FROM accessc WHERE card = "{newCard}") as OUTPUT')
    myresult = mycursor.fetchone()[0]
    if myresult == 1:
        print("Card has already been issued")
        time.sleep(2)
        os.system("clear")
    else:
        sql = f'INSERT INTO accessc (first, last, card, creation, access) VALUES ("{fname}", "{lname}", "{newCard}", "{today}", "{today}")'
        mycursor.execute(sql)
        time.sleep(2)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    logging.info(f'{fname}, {lname} and card have been written to database.')
    time.sleep(2)
    os.system('clear')
