sudo apt update -y && sudo apt upgrade -y

sudo apt install python3-pip mariadb-server -y

pip3 install --upgrade setuptools adafruit-python-shell schedule python-crontab adafruit-circuitpython-pn532 sh keyboard mysql-connector-python mariadb

clear
echo "Creating service"

sudo cp -v scanIn.service /etc/systemd/system/ && sudo systemctl start scanIn.service && sudo systemctl enable scanIn.service
