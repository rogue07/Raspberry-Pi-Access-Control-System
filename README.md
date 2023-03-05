# Raspberry-Pi-Access-Control-System
Pi powered Access Control
Built on: Raspbian GNU/Linux 11
Using: 32 bit
RFID Reader: Adafruit pn532


The wiring diagram is included, wiring_diagram.jpg


The system uses GPIO 12 for relay control. The wiring diagram I went with is for SPI.
https://learn.adafruit.com/adafruit-pn532-rfid-nfc/python-circuitpython


All files are in the accessc.zip.


1. Make sure the OS has a user named "accessc" and unzip the files so it overrides the Documents folder.

2. Make sure in the accessc home directory:
    
     $ cd

3. Unzip file:
     
     $ unzip accessc.zip

4. From the command prompt in the Documents directory run the installer:
     
     $ ./installer.sh

It will update and upgrade the pi as well as install mariaDB, mysql-connector-python, adafruit tools and some other necessities. Lastly answer  the questions as follows:



Switch to unix_socket authentication [Y/n] y


Change the root password? [Y/n] y


Remove anonymous users? [Y/n] y


Disallow root login remotely? [Y/n] y


Remove test database and access to it? [Y/n] y


Reload privilege tables now? [Y/n] y



5. Now that the installer has completed let's setup the MariaDB database and table by running the following:
     
     $ python3 sqlSetup.py


6. Lastly let's run setPasswd.sh to change the default password in the scripts to the one that was set in the last step.
     
     $ ./sqlPasswd.sh


7. To start the program run:
     
     $ python3 accessc.py
