# Raspberry-Pi-Access-Control-System
Pi powered Access Control
Built on: Raspbian GNU/Linux 11
Using: 32 bit
RFID Reader: Adafruit pn532


The wiring diagram is the .jpg file.


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


Answer as follows:
> Switch to unix_socket authentication [Y/n] y

> Change the root password? [Y/n] n

> Remove anonymous users? [Y/n] y

> Disallow root login remotely? [Y/n] y

> Remove test database and access to it? [Y/n] y

> Reload privilege tables now? [Y/n] y

5. From the command prompt run:
     $ sudo mysql -u root -p

Run the following commands:
> CREATE DATABASE codedb;

> show databases;

> USE codedb;

> CREATE TABLE accessc(user_id INT AUTO_INCREMENT PRIMARY KEY, first VARCHAR(20) NOT NULL, last VARCHAR(20) NOT NULL, card VARCHAR(32) NOT NULL, creation VARCHAR(25) NOT NULL, access VARCHAR(25) NOT NULL);

* Replace PASSWORD with a password of your choice.
> CREATE USER 'accessc'@'localhost' IDENTIFIED BY 'PASSWORD';

> GRANT ALL ON codedb.* To 'accessc'@'localhost' WITH GRANT OPTION;

> FLUSH PRIVILEGES;

> EXIT;


6. To run:
     $ python3 accessc.py
