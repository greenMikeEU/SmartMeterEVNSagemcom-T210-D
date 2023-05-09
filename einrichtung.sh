#!/bin/bash
echo "Einrichtung des Smart Meter bitte den Anweißungen folgen"
read -p "Bitte den Seriellen Port angeben (default:/dev/ttyUSB0): " port
read -p "Bitte die Baudrate eingeben (default:2400): " baudrate
read -p "Bitte geben Sie den Entschlüsselungs Code vom Netzbetreiber ein: " key
read -p "Sollen die Daten auf der Konsole ausgegeben werden ? (y/n): " userinput
printValue=false
if [[ $userinput =~ ^[yYnN][eE][sS]|[yY]$ ]]; then
	printValue=true
	echo Daten werden auf der Konsole ausgegeben.
fi
read -p "Sollen die Daten über MQTT ausgegeben werden? (y/n): " userinput
useMQTT=false
if [[ $userinput =~ ^[yYnN][eE][sS]|[yY]$ ]]; then
	useMQTT=true
	echo Daten werden auf der Konsole ausgegeben.
	read -p "Bitte IP-Adresse des Brokers eingeben: " mqttbrokerip
	read -p "Bitte den Port eingebn. (defaukt:1883): " mqttbrokerport
	read -p "Bitte den MQTT User eingeben. (Wenn keiner verwendet wird einfach leer lassen und mit Enter bestetigen): " mqttbrokeruser
	read -p "Bitte MQTT User Passwort eingeben. (Wenn kein Passwort verwendet wird einfach leer lassen und mit Enter bestetigen): " mqttbrokerpasswort
fi

read -p "Sollen die Daten in InfluxDB gespeichert werden (y/n): " userinput
useInfluxdb=false
if [[ $userinput =~ ^[yYnN][eE][sS]|[yY]$ ]]; then
	useInfluxdb=true
	read -p "Bitte IP-Adresse der Influxdb eingeben: " influxdbip
	read -p "Bitte den Port eingebn. (default:8086): " influxdbport
fi
sudo rm config.json
echo "{" >> config.json
echo "    \"port\": \"$port\"," >> config.json
echo "    \"baudrate\": $baudrate," >> config.json
echo "    \"key\": \"$key\"," >> config.json
echo "    \"printValue\": $printValue," >> config.json
echo "    \"useMQTT\": $useMQTT," >> config.json
if [ -z "$mqttbrokerport" ]; then
  echo "    \"mqttbrokerip\": \"\"," >> config.json
else
  echo "    \"mqttbrokerip\": \"$mqttbrokerip\"," >> config.json
fi
if [ -z "$mqttbrokerport" ]; then
  echo "    \"mqttbrokerport\": \"\"," >> config.json
else
  echo "    \"mqttbrokerport\": $mqttbrokerport," >> config.json
fi
echo "    \"mqttbrokeruser\": \"$mqttbrokeruser\"," >> config.json
echo "    \"mqttbrokerpasswort\": \"$mqttbrokerpasswort\"," >> config.json
echo "    \"useInfluxdb\": $useInfluxdb," >> config.json
if [ -z "$influxdbport" ]; then
  echo "    \"influxdbip\": \"\"," >> config.json
else
  echo "    \"influxdbip\": \"$influxdbip\"," >> config.json
fi
if [ -z "$influxdbport" ]; then
  echo "    \"influxdbport\": \"\"" >> config.json
else
  echo "    \"influxdbport\": $influxdbport" >> config.json
fi
echo "}" >> config.json