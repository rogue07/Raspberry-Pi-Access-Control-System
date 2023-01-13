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
#logging.basicConfig(filename="accessc.log", lvell=logging.INFO)
logging.basicConfig(filename="/home/accessc/Documents/accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')



now = datetime.now()
today = now.strftime("%d/%m/%Y %H:%M")
   
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!B7!v0??",
    database="codedb"
    )
mycursor = mydb.cursor()



spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

pn532.SAM_configuration()
print("Waiting for NFC card...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
    usercard = [hex(i) for i in uid]
   
    logging.info('Card was presented')
    time.sleep(5)

    mycursor.execute(f'SELECT EXISTS(SELECT * FROM accessc WHERE card = "{usercard}") as OUTPUT')
    myresult = mycursor.fetchone()
    print(myresult)
    mycursor.execute(f'SELECT last FROM accessc WHERE card = "{usercard}"')
    lname = mycursor.fetchone()
    mycursor.execute(f'SELECT first FROM accessc WHERE card = "{usercard}"')
    fname = mycursor.fetchone()
    print(fname, lname)

    time.sleep(5)
    

    if myresult != (1,):
        print("Access failed")
        logging.info('Failed access')
        time.sleep(2)
    else:
        print("Access successful")
        logging.info(f'{fname} {lname} successful access')
        time.sleep(2)
