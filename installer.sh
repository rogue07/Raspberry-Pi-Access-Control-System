#!/bin/bash

# Check if the username exists
if ! id "accessc" >/dev/null 2>&1; then
    echo "Please create user 'accessc'."
    exit 1
fi

# Verify you're in the correct directory
if [ "$PWD" != "/home/accessc/Documents" ]; then
    echo "Error: Working directory is not /home/accessc/Documents."
    exit 1
fi

# Update and upgrade
sudo apt-get update -y
sudo apt-get upgrade -y

# Install packages
sudo apt-get install -y build-essential python-dev libusb-1.0-0-dev libudev-dev python3-pip mariadb-server -y

# Start mariaDB
sudo systemctl start mariadb

# Install Python packages
pip3 install --upgrade setuptools adafruit-python-shell schedule python-crontab adafruit-circuitpython-pn532 sh keyboard mysql-connector-python mariadb adafruit-blinka

# Install the RFID reader
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install

# Setup systemd service
sudo cp ~/Documents/scanIn.service /etc/systemd/system
sudo systemctl start scanIn.service
sudo systemctl enable scanIn.service

# Set root password
#sudo passwd root

# Setup mariadb
echo "mariadb secure installation:"
sudo mysql_secure_installation

echo "Install script is complete."
