sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install python3-pip -y && sudo apt install mariadb-server -y
pip3 install --upgrade setuptools adafruit-python-shell schedule python-crontab adafruit-circuitpython-pn532 sh keyboard mysql-connector-python mysql.connector mariadb
sudo cp -v scanIn.service /etc/systemd/system/ && sudo systemctl start scanIn.service && sudo systemctl enable scanIn.service

