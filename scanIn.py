#/usr/bin/python3

# ram persaud
# 14 jan, 2023
# scanIn.py should be running as a systemd service


import os
import mysql.connector
import logging
import board
import busio
import time
from digitalio import DigitalInOut
from datetime import datetime
from adafruit_pn532.spi import PN532_SPI


# log to accessc.log
logfile = "/home/accessc/Documents/accessc.log"
logging.basicConfig(filename="/home/accessc/Documents/accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


# set some variables

now = datetime.now()
today = now.strftime("%d/%m/%Y %H:%M")
#today = now.strftime("%d/%m/%Y")
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

# mariadb login
mydb = mysql.connector.connect(
    host="localhost",
    user="accessc",
    password="PASSWORD",
    database="codedb"
    )
mycursor = mydb.cursor()


# main
pn532.SAM_configuration()
print("Waiting for NFC card...")

while True:
    time.sleep(1.5)
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
    usercard = [hex(i) for i in uid]
   
    logging.info('Card was presented')

    mycursor.execute(f'SELECT * FROM accessc WHERE card = "{usercard}"')
    myresult = mycursor.fetchone()
    
    mycursor.execute(f'SELECT first, last FROM accessc WHERE card = "{usercard}"')
    name = mycursor.fetchone()
    
    print(bool(myresult))
    x = bool(myresult)
    print(name)
    time.sleep(1)
    if x == True:
        print("Access successful")
        now = datetime.now()
        today = now.strftime("%d/%m/%Y %H:%M")        
        mycursor.execute(f'UPDATE accessc SET access = "{today}" WHERE CARD = "{usercard}"')

        mydb.commit()
        logging.info(f'{name} Access successful')
    else:
        print("Failed access")
        logging.info('Failed access')
