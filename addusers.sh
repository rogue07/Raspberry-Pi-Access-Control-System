#!/bin/bash
# Script: addusers.sh

# Accessing variables from command line arguments
fname=$1
lname=$2

# Connect to the database
mariadb() {
    mysql -h localhost -u accessc -pPASSWORD -D codedb
}

# Add user and associate a card with them
user_add() {
    echo ""
    echo ""
    # Prompt user to enter first name
    read -p "Enter First name: " fname
    if [ -z "$fname" ]
    then
        echo "Name can not be blank"
        return
    else
        echo $fname
    fi

    # Prompt user to enter last name
    read -p "Enter last name: " lname
    if [ -z "$lname" ]
    then
        echo "Name can not be blank"
        sleep 1
    else
        echo $lname
    fi

    # Check if user already exists in the database
    result=$(mariadb -se "SELECT * FROM accessc WHERE first='$fname' AND last='$lname'")
    if [ -z "$result" ]
    then
        echo "User's name is unique"
        sleep 1
    else
        echo "User already exists!"
        sleep 2
        clear
        user_add
    fi

    # Wait for NFC card to be detected
    echo "Waiting for NFC card..."
    sleep 1
    uid=$(python - <<EOF
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()
print("Waiting for NFC card...")
while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is not None:
        print("Found card with UID:", [hex(i) for i in uid])
        break
EOF
)

    # Associate the new card with the user
    now=$(date +"%d/%m/%Y %H:%M")
    result=$(mariadb -se "SELECT EXISTS(SELECT * FROM accessc WHERE card = '$uid') as OUTPUT")
    if [ "$result" -eq "1" ]
    then
        echo "Card has already been issued"
        sleep 2
        clear
        return
    else
        sql="INSERT INTO accessc (first, last, card, creation, access) VALUES ('$fname', '$lname', '$uid', '$now', '$now')"
        mariadb -e "$sql"
        sleep 2
    fi

    # Log the user and card details in a file
    echo "$fname $lname and card have been written to database." >> addusers.log
    sleep 2
    clear
}

# Call the user_add function
user_add
