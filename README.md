# SmartMeterEVN
Dieses Projekt ermöglicht es den Smartmeter der EVN (Netz Niederösterreich) über die Kundenschnittstelle auszulesen.


## Getting Started
### Voraussetzungen Hardware
* Raspberry PI (getestet ist der Pi3 B+)
* RJ-12 Kabel
* MBus-Adapter auf USB (ich selber habe diesen https://amzn.to/3psoPqg)
* Passwort für die Kundenschnittstelle
  * Alle folgenden Inflormationen sind aus dem Folder der EVN. (https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx)
  * Kann hier Angefordert werden. smartmeter@netz-noe.at
  * Kundennummer oder Vertraskontonummer
  * Zählernummer


### Voraussetzungen Software
* Raspbian
* Python3
* Libraries
    * gurux_dlms
    * beautifulsoup4
    * paho-mqtt



### Installation der Libaararies
```
sudo pip3 install gurux-dlms
sudo pip3 install beautifulsoup4
sudo pip3 install paho-mqtt
```

### Anpassen des Pythonprogrammes
Öffne die Python Datei (EvnSmartmeterMQTT.py) mit einem beliebigen Editor. Die Betreffenden Zeilen sind 12 und 15. In Zeile 12 muss der EVN Schlüssel Eingetragen werden zwischen den "dein EVN Schlüssel".
Anschliesend Muss der mqttBroker in der Zeile 15 geändert werden. Es reicht nur die IP Adresse zb. "192.168.1.99". Die Datei speichern.

### Starten des Pythonprogrammes
Wenn das Programm am Desktop liegt musste der nächste Befehl passen. Sonst muss der Pfad geändert werden.
```
sudo python3 /home/pi/Desktop/EvnSmartmeterMQTT.py
```

### Fehler des Pythonprogrammes
Es sind bis jetzt nur zwei Fehler implementiert!
* Wenn keine Verbindung zum Broker aufgebaut werden kann dann wird der Fehler "Die Ip Adresse der Brokers ist falsch!" ausgegeben. Fehlerbehebung mann muss die richtige IP Adresse angeben.
* Wenn der Fehler "Fehler beim Synchronisieren. Programm bitte ein weiteres mal Starten." kommt muss mann ca 3 Sekunden warten und es Neustarten nach ein paar Versuchen sollte es starten.


### Bugs
* Wenn eine PV-Anlage vorhanden ist und diese mehr Produziert als unmittelbar verbraucht wird erhählt man einen cos phi von ca 60 dieser hat physikalisch keine Bedeutung für mich. Im normal Fall ist dieser kleiner Null.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details