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
sudo apt update -y
sudo apt upgrade -y



# Some tools
sudo apt install vim screen -y

A
# Install apache2 
sudo apt install apache2 -y
sudo usermod -a -G www-data accessc
sudo chown -R -f www-data:www-data /var/www/html
sudo apt install php7.4 libapache2-mod-php7.4 php7.4-mbstring php7.4-mysql php7.4-curl php7.4-gd php7.4-zip -y


# Install packages
sudo apt install -y build-essential python-dev libusb-1.0-0-dev libudev-dev python3-pip mariadb-server -y

# Start mariaDB
sudo systemctl start mariadb

# Install Python packages
sudo pip3 install --upgrade setuptools adafruit-python-shell schedule python-crontab adafruit-circuitpython-pn532 sh keyboard mysql-connector-python mariadb adafruit-blinka

# Install the RFID reader
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install

# Setup systemd service
sudo cp ~/Documents/scanIn.service /etc/systemd/system
sudo systemctl start scanIn.service
sudo systemctl enable scanIn.service

# Setup mariadb
echo "mariadb secure installation:"
sudo mysql_secure_installation


# Set crontab entry for log cleanup
#!/bin/bash

# Use crontab to schedule the command to run every Friday at 11pm
(crontab -l 2>/dev/null; echo "0 23 * * 5 ~/Documents/accessc/cleanupLog.sh") | crontab -

# Give root permission to use spi
#sudo adduser root spi
#sudo adduser root gpio
#sudo adduser www-data spi
#sudo adduser www-data gpio

#sudo usermod -a -G spi <username>
# To remove a user from a group
#sudo gpasswd -d <username> spi

# Adding accessc to the group www-data
sudo usermod -a -G www-data accessc
sudo chgrp www-data /home/accessc/Documents/
sudo chmod g+rwxs /home/accessc/Documents/



echo "Install script is complete."
