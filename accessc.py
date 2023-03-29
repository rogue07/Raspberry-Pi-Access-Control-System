#!/usr/bin/python3

#Ramon Persaud
#10 sep 2022
#My attempt at an access control system.

import pdb
import logging
import os 
import time
import sys
import board
import busio
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

# Log to accessc.log
logging.basicConfig(filename="accessc.log", format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


# Displayed menu
def menu():
    print("")
    print("     Choose an option: ")
    print("     1. Add User & Cards")
    print("     2. Delete User & Card")
    print("     3. Test lock")
    print("     4. Schedules")
    print("     5. View Live Log")
    print("     6. Emergency")
    print("     7. View User Info")
    print("     8. Quit")




# loginto mariadb server
def mariadb():
    mydb = mysql.connector.connect(
    host="localhost",
    user="accessc",
    password="PASSWORD",
    database="codedb"
    )
#    mycursor = mydb.cursor()
    return mydb


# Add user and associate a card with them
def user_add():
    print("")
    print("")
    mydb = mariadb()
    mycursor = mydb.cursor()
    
    fname = input('Enter First name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        return
    else:
        print(fname)

    lname = input('Enter last name: ').lower()
    if fname == '':    
        print("Name can not be blank")
        time.sleep(1)
    else:
        print(lname)
        
    mycursor.execute(f'SELECT * FROM accessc WHERE first="{fname}" AND last="{lname}"')
    result = mycursor.fetchone()
    print(result)
    if not result:
        print("User's name is unique")
        logging.info(f'{fname, lname} was entered.')
        time.sleep(1)
    else:
        print("User already exists!")
        time.sleep(2)
        os.system('clear')
        user_add()

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
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

        mydb = mariadb()    
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
            return 
        else:
            sql = f'INSERT INTO accessc (first, last, card, creation, access) VALUES ("{fname}", "{lname}", "{newCard}", "{today}", "{today}")'
            mycursor.execute(sql)
            time.sleep(2) 
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        logging.info(f'{fname, lname} and card have been written to database.')
        time.sleep(2)
        os.system('clear')
        return
    
# delete user and card functiin
def delete():
    mydb = mysql.connector.connect(
        host="localhost",
        user="accessc",
        password="PASSWORD",
        database="codedb"
        )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY first) user_id, first, last FROM accessc")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    print()
    print("------------------")
    print("|   Delete user: |")
    print("------------------\n")

    fname = input("Enter first name> ")
    lname = input("Enter last name> ")
#mycursor.execute(f'SELECT * FROM accessc WHERE first "{fname}")'
    mycursor.execute(f'SELECT * FROM accessc WHERE first = "{fname}" AND last = "{lname}"')
    mycursor.fetchone()

    mycursor.execute(f'DELETE FROM accessc WHERE first = "{fname}" AND last = "{lname}"')
    mydb.commit()
    
    print(fname, lname, "has been deleted.")


# Toggling relay to open and close the lock manually
def lock():
    logging.info("Lock has been manually triggered.")
    os.system('python3 unlock.py')
    return


# Create a schedule using cron
def schedule():
    # whats the frequency kenneth
    note = input("Note ex.unlock schedule> ")
    utime = input("Unlock time ex.13:30> ")
    ltime = input("Lock time ex.9:15> ")

    #take users time input and split it
    htime,mtime = utime.split(':')
    Htime,Mtime = ltime.split(':')

    with CronTab(user='accessc') as cron:
        # pulse to unlock
        job = cron.new(command='python3 ~/Documents/pulseulock.py')
        job.set_comment(note)
        job.hour.on(htime)
        job.minute.on(mtime)
        # pulse to lock
        job = cron.new(command='python3 ~/Documents/pulselock.py')
        job.set_comment(note)
        job.hour.on(Htime)
        job.minute.on(Mtime)
    cron.write()
    print("Job has been scheduled")
    logging.info(f'{utime, ltime} unlock/lock schedule set.')
    time.sleep(3)


# Run the linux command tail on accessc.log
def log():
    try:
        while True:
            for line in tail("-f", "accessc.log", _iter=True):
                print(line)
    except KeyboardInterrupt:
        os.system('clear')
        return

# Emergency lockdown for the lock
def emergency():
    menu = input("Lock/Unlock L/U > ").lower()
    print(menu)
    time.sleep(1)
    if menu == "l":
        print("Locking all locks.")
        os.system('python3 emergencylock.py')
        time.sleep(1)
        return
    elif menu == "u":
        print("Returning to normal operation")  
        os.system('python3 emergencyulock.py')
        time.sleep(1)
        return


# view data in all tables
def viewUsers():
    mydb = mariadb()
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT * FROM accessc;')
    os.system('clear')
    for table in mycursor:
        print(table)
    time.sleep(5)
    return

def main():
    while True:
        os.system('clear')
        menu()
        number = input(">  ")
        if number == "1":
            os.system('clear')
            user_add()
            os.system('clear')
        elif number == "2":
            print("You choose to delete a user and card")
            time.sleep(2)
            os.system('clear')
            delete()
        elif number == "3":
            print("Test lock")
            time.sleep(2)
            os.system('clear')
            lock()
        elif number == "4":
            print("schedule")
            time.sleep(2)
            os.system('clear')
            schedule()
        elif number == "5":
            print("View live log")
            print("Ctl+c will exit live log")
            time.sleep(4)
            os.system('clear')
            log()
        elif number == "6":
            print("Emergency")
            os.system("clear")
            emergency()
        elif number == "7":
            print("View Users Info")
            os.system('clear')
            viewUsers()
        elif number == "8":
            print("Exiting")
            os.system('clear')
            quit()
        elif number == "_":
            print("Choose a correct number.")
            time.sleep(2)
            os.system('clear')

if __name__ == "__main__":
    main()
