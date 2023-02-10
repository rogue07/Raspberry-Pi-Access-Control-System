# Raspberry-Pi-Access-Control-System
Pi powered Access Control
Built on: Raspbian GNU/Linux 11
Using: 32 bit
RFID Reader: Adafruit pn532


The system uses GPIO 12 for relay control. The wiring diagram I went with is for SPI.
https://learn.adafruit.com/adafruit-pn532-rfid-nfc/python-circuitpython


All files are in the .zip file.


1. Make sure the OS has a user named:
     accessc

2. Copy all the files into the Documents directory.

3. Set a root password. From the command prompt run:
     $ sudo passwd root

4. From the command prompt in the Documents directory run the installer:
     $ ./installer.sh

5. Let's install and create the database and table. From the command prompt run the following:
     $ sudo mysql_secure_installation

Answer yes to all:
> Switch to unix_socket authentication [Y/n] y

> Change the root password? [Y/n] y

> Remove anonymous users? [Y/n] y

> Disallow root login remotely? [Y/n] y

> Remove test database and access to it? [Y/n] y

> Reload privilege tables now? [Y/n] y

From the command prompt run:
$ sudo mysql -u root -p

Run the following commands:
> CREATE DATABASE codedb;

> show databases;

> USE codedb;

> CREATE TABLE accessc(user_id INT AUTO_INCREMENT PRIMARY KEY, first VARCHAR(20) NOT NULL, last VARCHAR(20) NOT NULL, card VARCHAR(32) NOT NULL, creation VARCHAR(25) NOT NULL, access VARCHAR(25) NOT NULL);

> CREATE USER 'accessc'@'localhost' IDENTIFIED BY 'PASSWORD';

> GRANT ALL ON codedb.* To 'accessc'@'localhost' WITH GRANT OPTION;

> FLUSH PRIVILEGES;

> EXIT;


6. To run:
     $ python3 accessc.py
