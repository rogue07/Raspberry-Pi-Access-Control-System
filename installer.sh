#!/bin/bash

# Check if the username exists
if id "accessc" >/dev/null 2>&1; then
	echo "Username accessc exists."
	echo "Continuing installation."
else
	echo "Please create user 'accessc'."
	exit 1
fi

# Verify you're in the xorrect directory
if [ "$PWD" != "/home/accessc/Documents" ]; then
	echo "Error: Working directory is not /home/accessc/Documents."
	exit 1
fi


# Update and upgrade
sudo apt-get update -y
sudo apt-get upgrade -y

# Install these
sudo apt-get install -y build-essential python-dev libusb-1.0-0-dev libudev-dev
sudo apt-get install python3-pip -y
sudo apt install mariadb-server -y

# Installer for the rfid reader
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install

# pip install
pip3 install --upgrade setuptools
pip3 install --upgrade adafruit-python-shell
pip3 install schedule
pip3 install python-crontab
pip3 install adafruit-circuitpython-pn532
pip3 install sh
pip3 install keyboard
pip3 install mysql-connector-python
pip3 install mariadb
pip3 install adafruit-blinka

clear

# setup scanIn.service as a systemd process
sudo cp ~/Documents/scanIn.service /etc/systemd/system
sudo systemctl start scanIn.service
sudo systemctl enable scanIn.service

clear

# Set root passwird
echo "Enter root password:"
sudo passwd root

clear

# Setup mariadb
echo "mariadb secure installation:"
sudo mysql_secure_installation

echo "Install script is complete."
