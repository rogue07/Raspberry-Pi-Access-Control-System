import mysql.connector

# prompt user for password
password = input("Enter password for 'root' user: ")

# connect to MySQL server
cnx = mysql.connector.connect(user='root', password=password, host='localhost')
cursor = cnx.cursor()

# create database and select it
cursor.execute("CREATE DATABASE codedb")
cursor.execute("USE codedb")

# create table
cursor.execute("CREATE TABLE accessc(user_id INT AUTO_INCREMENT PRIMARY KEY, first VARCHAR(20) NOT NULL, last VARCHAR(20) NOT NULL, card VARCHAR(32) NOT NULL, creation VARCHAR(25) NOT NULL, access VARCHAR(25) NOT NULL)")

password = input("Enter a password for the 'accessc' user: ")

# create user and grant privileges
cursor.execute("CREATE USER 'accessc'@'localhost' IDENTIFIED BY %s", (password,))
cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'accessc'@'localhost' IDENTIFIED BY %s", (password,))
cursor.execute("FLUSH PRIVILEGES")

# show granted privileges
cursor.execute("SHOW GRANTS FOR 'accessc'@'localhost'")
print("Privileges granted to 'accessc' user:")
for grant in cursor:
        print(grant[0])

# close cursor and connection
cursor.close()
cnx.close()
