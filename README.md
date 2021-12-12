# SmartMeterEVN
Dieses Projekt ermöglicht es den Smartmeter der EVN (Netz Niederösterreich) über die Kundenschnittstelle auszulesen.


## Getting Started
### Voraussetzungen Hardware
* Passwort für die Kundenschnittstelle
  * Alle folgenden Informationen sind aus dem Folder der EVN. (https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx)
  * Kann hier angefordert werden. smartmeter@netz-noe.at
  * Kundennummer oder Vertragskontonummer
  * Zählernummer




### Zähler Hersteller
* Sagemcom Drehstromzähler T210-D

Bei den anderen Zählertypen von der EVN kann ich keine Auskunft geben ob diese Programm funktioniert. Die oben genannte Zählertypen sind getestet. Wenn es jemand testet bitte Bescheid, geben dann kann die Liste erweitert werden kann.

### Voraussetzungen Software
* Raspbian
* Python3
* Libraries
    * gurux_dlms
    * beautifulsoup4
    * paho-mqtt

|Produkt                           |wird benötigt| Amazon                  | Aliexpress                               |
|----------------------------------|-------------|-------------------------|------------------------------------------|   
|Raspberry Pi 4                    |Ja           | https://amzn.to/31HA7PC | --                                       |
|Raspberry Pi 4 Hutschienen Gehäuse|Nein         | https://amzn.to/3GyAY3I | --                                       |
|USB-zu-MBUS-Slave-Modul           |Ja           | https://amzn.to/3GA3HoW | https://s.click.aliexpress.com/e/_9yVpxq |
|RJ-12 Kabel                       |Ja           | https://amzn.to/3EIL55s |                                          |
|Schaltschrank Steckdose           |Nein         | https://amzn.to/3ygAImW |                                          |


### Installation der Libararies
```
sudo pip3 install gurux-dlms
sudo pip3 install beautifulsoup4
sudo pip3 install paho-mqtt
sudo pip3 install lxml
```
Für die Version EVNSmartmeterMQTT_V01.py wird eine weitere Libarariy benötogt
```
sudo apt install python3-pycryptodome
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
* Wenn keine Verbindung zum Broker aufgebaut werden kann dann wird der Fehler "Die Ip Adresse des Brokers ist falsch!" ausgegeben. Zur Fehlerbehebung muss die richtige IP Adresse angegeben werden.
* Wenn der Fehler "Fehler beim Synchronisieren. Programm bitte ein weiteres mal Starten." kommt, muss mann ca. drei Sekunden warten. Nach ein paar Versuchen sollte es problemlos starten.

### MQTT Topics
Diese können ab der Zeile 144 bis 155 verändert werden. Standardmäßig sind folgende eingestellt.
| Topic                         | Kommentar                                       | Einheit       |    
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
* Wenn eine PV-Anlage vorhanden ist und diese mehr produziert als unmittelbar verbraucht wird, erhählt man einen cos phi von ca. 60. Dieser hat physikalisch keine Bedeutung für mich. Im Normalfall ist dieser zwischen 0 - 1.

### Versionsunterschied
Es sind 2 Python Programme beide machen grundsäzlich das selbe nur die Synchronisierung ist unterschiedlich. Es funktionieren beide aber sie wurden noch nicht im Dauereinsatz getestet. Welches sich als stabiler herausstellt wird auf Dauer bleiben und das andere entfernt.

EvnSmartmeterMQTT.py
* wenn es startet sollte es alle 5 Sekunden Werte senden ohne Unterbrechung
* der längste Dauertest war 14 Tage und dann ist es Abgestürtz. (Fehler muss nicht im Skript sein kann ein Absturz vom Broker oder Pi selber gewesen sein)

EVNSmartmeterMQTT_V01.py
* bei diesem Programm ist mir selber schon aufgefallen dass nicht alle 5 Sekunden Werte kommen aber dafür Syncronisiert es sich selber und stürtz nicht ab.
* Testzeitraum war ca. Stunden.


### Roadmap (Updates)
Es soll eine Version mit einem ESP32 kommen, dieser liest die Daten ein und schickt sie auf einen bestehenden Server weiter. Um sich den Kabelweg zu sparen oder den Raspberry.
Wenn ich es schaffe will ich ein eigenes Modul auf den Markt bringen, dass Plug and Play funktioniert und nur einen Bruchteil eines Raspberry´s kostet.

### Hinweis
Alle Links zu Produkten sind Affiliate Links. Somit unterstützt ihr diese und weitere Projekte von mir.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details