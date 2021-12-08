# SmartMeterEVN
Dieses Projekt ermöglicht es den Smartmeter der EVN (Netz Niederösterreich) über die Kundenschnittstelle auszulesen.


## Getting Started
### Voraussetzungen Hardware
* Raspberry PI (getestet ist der Pi3 B+)
* RJ-12 Kabel
* MBus-Adapter auf USB (ich selber habe diesen https://amzn.to/3psoPqg)
* Passwort für die Kundenschnittstelle
  * Alle folgenden Informationen sind aus dem Folder der EVN. (https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx)
  * Kann hier Angefordert werden. smartmeter@netz-noe.at
  * Kundennummer oder Vertragskontonummer
  * Zählernummer
### Zähler Hersteller
* Sagemcom Drehstromzähler T210-D
Bei den anderen Zählertypen von der EVN kann ich keine Auskunft geben ob diese Programm funktioniert. Jeder oben genante ist getestet. Wenn es wer testet bitte bescheid geben dann kann die Liste erweitert werden.

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
sudo pip3 install lxml
```

### Anpassen des Pythonprogrammes & Einstellungen
Öffne die Python Datei (EvnSmartmeterMQTT.py) mit einem beliebigen Editor. Die Betreffenden Zeilen sind 12, 15, 18, 21 und 24. In Zeile 12 muss der EVN Schlüssel eingetragen werden zwischen den "dein EVN Schlüssel". In Zeile 15 kann man die Ausgabe über MQTT auswählen wenn diese auf True ist dann muss man eine gültige MQTT IP Adresse in Zeile eingeben.Es reicht nur die IP Adresse zb: "192.168.1.99". Die Datei speichern. In Zeile 24 kann noch der Comport eingestellt werden. 

### Starten des Pythonprogrammes
Wenn das Programm am Desktop liegt kann das Programm mit dem nächsten Befehl gestartet werden, sonst muss der Pfad geändert werden.
```
sudo python3 /home/pi/Desktop/EvnSmartmeterMQTT.py
```

### Fehlermeldungen des Pythonprogrammes
Es sind bis jetzt nur zwei Fehlermeldungen implementiert!
* Wenn keine Verbindung zum Broker aufgebaut werden kann dann wird der Fehler "Die Ip Adresse des Brokers ist falsch!" ausgegeben. Zur Fehlerbehebung muss die richtige IP Adresse angeben werden.
* Wenn der Fehler "Fehler beim Synchronisieren. Programm bitte ein weiteres mal Starten." kommt, muss mann ca. drei Sekunden warten. Nach ein paar Versuchen sollte es problemlos starten.

### MQTT Topics
Diese können ab der Zeile 144 bis 155 verändert werden. Standardmäßig sind folgende eingestellt.
| Topic                         | Kommentar                                       | Einheit   |    
| ------------------------------| -------------                                   |-------------  |
| Smartmeter/WirkenergieP       | bezogene Energie                                | Wh (keine kWh)|
| Smartmeter/WirkenergieN       | gelieferte Energie                              | Wh (keine kWh)|
| Smartmeter/MomentanleistungP  | Momentanleistung Bezug                          | W             |
| Smartmeter/MomentanleistungN  | Momentanleistung Lieferung                      | W             |
| Smartmeter/Momentanleistung   | Momentanleistung Summe aus Bezug und Lieferung  | W             |
| Smartmeter/SpannungL1         | Spannung an L1                                  | V             |
| Smartmeter/SpannungL2         | Spannung an L2                                  | V             |
| Smartmeter/SpannungL3         | Spannung an L3                                  | V             |
| Smartmeter/StromL1            | Strom an L1                                     | A             |
| Smartmeter/StromL2            | Strom an L2                                     | A             |
| Smartmeter/StromL3            | Strom an L3                                     | A             |
| Smartmeter/Leistungsfaktor    | Leistungsfaktor                                 |               |

Die Einheiten sind auf die Grundeinheit bezogen worden nicht wie im EVN-Folder!
### Bugs
* Wenn eine PV-Anlage vorhanden ist und diese mehr Produziert als unmittelbar verbraucht wird, erhählt man einen cos phi von ca. 60. Dieser hat physikalisch keine Bedeutung für mich. Im Normalfall ist dieser zwischen 0 - 1.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details