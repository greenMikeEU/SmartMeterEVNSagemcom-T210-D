#!/bin/bash
#Dieses Skript installier alle nötigen Pakete und Programme für das Smart Meter Monitoring
sudo apt-get update
sudo apt-get upgrade
# Installiert Influxdb
apt-get -y install influxdb
apt-get -y install influxdb-client
# Startet den Influxdb service
systemctl start influxdb
# Erstellen der Datenbank
influx -execute "create database SmartMeter"
# Installiert Grafana
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana
### Legt Grafana in den Autostart
sudo /bin/systemctl enable grafana-server
### Start Grafana Server
sudo /bin/systemctl start grafana-server
sudo apt-get update
# Installiert Python3
apt install python3 idle3
sudo apt-get install python3-pip
# Installation von Python Paketen
sudo pip3 install gurux-dlms --break-system-packages
sudo pip3 install beautifulsoup4 --break-system-packages
sudo pip3 install paho-mqtt==1.6.1 --break-system-packages
sudo apt-get install libxslt-dev --break-system-packages
sudo pip3 install pyserial --break-system-packages
sudo pip3 install cryptography --break-system-packages
sudo pip install influxdb --break-system-packages
sudo pip3 install html5lib --break-system-packages
sudo apt install python3-pycryptodome