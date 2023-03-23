#!/bin/bash

# Stop MariaDB service
sudo systemctl stop mariadb.service

# Remove MariaDB package and its dependencies
sudo apt-get purge mariadb-server mariadb-client mariadb-common -y

# Remove data directory
sudo rm -rf /var/lib/mysql

# Remove configuration files
sudo rm /etc/mysql/my.cnf

# Clean up any remaining files
sudo apt-get autoremove -y
sudo apt-get autoclean -y

# Restart server
sudo shutdown -r now
