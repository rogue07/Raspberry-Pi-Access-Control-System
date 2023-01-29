# Raspberry-Pi-Access-Control-System
Pi powered Access Control


1. Make sure the OS has a user named:
     accessc

2. Copy all the files into the Documents directory.

3. From the command prompt in the Documents directory run the installer:
     ./installer.sh

4. Let's install and create the database and table. From the command prompt run the following:
$ sudo mysql_secure_installation

Answer no:
Switch to unix_socket authentication [Y/n] n
Change the root password? [Y/n] n

Answer yes:
Remove anonymous users? [Y/n] y
Disallow root login remotely? [Y/n] y
Remove test database and access to it? [Y/n] y
Reload privilege tables now? [Y/n] y


From the prompt run:
$ sudo mysql -u root -p

Run the following commands:
> CREATE DATABASE codedb;
> show databases;
> USE codedb;
> CREATE USER 'accessc'@'localhost' IDENTIFIED BY '?Ac0ntr0l.';
> GRANT ALL ON codedb.* To 'accessc'@'localhost' WITH GRANT OPTION;
> CREATE TABLE accessc(user_id INT AUTO_INCREMENT PRIMARY KEY, first VARCHAR(32) NOT NULL, last VARCHAR(32) NOT NULL, card VARCHAR(32) NOT NULL, creation DATE NOT NULL, access DATE NOT NULL);
> DESC accessc;
> exit;
