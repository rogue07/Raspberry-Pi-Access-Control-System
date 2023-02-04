sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt-get install -y build-essential python-dev libusb-1.0-0-dev libudev-dev

git clone https://github.com/adafruit/Adafruit_Python_PN532.git

cd Adafruit_Python_PN532

sudo python setup.py install

# add a udev rule for the PN532 device
#echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0424", ATTRS{idProduct}=="9514", GROUP="plugdev", MODE="0660"' | sudo tee /etc/udev/rules.d/42-pn532.rules

sudo apt-get install python3-pip -y

sudo apt install mariadb-server -y

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

sudo cp scanIn.service /etc/systemd/system/
sudo systemctl start scanIn.service
sudo systemctl enable scanIn.service

