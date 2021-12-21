# SmartMeterEVN
Dieses Projekt ermöglicht es den Smartmeter der EVN (Netz Niederösterreich) über die Kundenschnittstelle auszulesen.
Smart Meter werden von der Netz NÖ GmbH eingebaut, auf Basis der gesetzlichen Forderungen.

## Getting Started
### Voraussetzungen Hardware


* Passwort für die Kundenschnittstelle
  * Alle folgenden Informationen sind aus dem Folder der EVN. (https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx)
  * Wenn bereits ein Smart Meter in der Kundenanlage eingebaut ist, kann hier das der Schlüssel angefordert werden: smartmeter@netz-noe.at
    * Kundennummer oder Vertragskontonummer
    * Zählernummer
    * Handynummer




### Zähler Hersteller
* Sagemcom Drehstromzähler T210-D

Die folgende Beschreibung bzw. das durchgeführte Projekt bezieht sich nur auf den angegebenen Zählertyp. Für weitere Zählertypen, welche vom Netzbetreiber eingebaut werden kann hier keine Garantie gegeben werde. Aufgrund der Angaben seitens dem Netzbetreiber, sollte die Anwendung möglich sein. Sollte es dazu Erfahrungen geben, können diese gerne an mich übermittelt werden.

### Voraussetzungen Software
* Raspbian
* Python3
* Libraries
    * gurux_dlms
    * beautifulsoup4
    * paho-mqtt

|Produkt                           |wird benötigt| Amazon                  | Aliexpress                               |
|----------------------------------|-------------|-------------------------|------------------------------------------|   
|Raspberry Pi 4                    |Ja           | https://amzn.to/3mpunAZ | --                                       |
|Raspberry Pi 4 Starter Set        |Ja           | https://amzn.to/3FoYX5q | --                                       |
|Raspberry Pi 4 Hutschienen Gehäuse|Nein         | https://amzn.to/3mnCcqG | --                                       |
|USB-zu-MBUS-Slave-Modul           |Ja           | https://amzn.to/33BnnKH | https://s.click.aliexpress.com/e/_9yVpxq |
|RJ-12 Kabel                       |Ja           | https://amzn.to/3FdCMyO |                                          |
|Schaltschrank Steckdose           |Nein         | https://amzn.to/3Eh1Kfi |                                          |

### Verkabelung des Mbus Adapter
Die beiden mittleren Kabel des RJ-12 Kabel müssen in die MBus Klemmen eingeklemmt werden. Dann muss der USB an den Raspberry angeschlossen werden.


### Installation der Libararies
```
sudo pip3 install gurux-dlms
sudo pip3 install beautifulsoup4
sudo pip3 install paho-mqtt
sudo pip3 install lxml
```
Für die Version EVNSmartmeterMQTT_V01.py wird eine weitere Libarariy benötogt.
```
sudo apt install python3-pycryptodome
```

### Anpassen des Pythonprogrammes & Einstellungen
Öffne die Python Datei (EvnSmartmeterMQTT.py) mit einem beliebigen Editor. Die Betreffenden Zeilen sind 12, 15, 18, 21 und 24. In Zeile 12 muss der Schlüssel eingetragen werden zwischen den "dein EVN Schlüssel". Ein Beispiel ist im Programm angeführt. In Zeile 15 kann man die Ausgabe über MQTT auswählen wenn diese auf True ist dann muss man eine gültige MQTT IP Adresse in Zeile eingeben.Es reicht nur die IP Adresse zb: "192.168.1.99". Die Datei speichern. In Zeile 24 kann noch der Comport eingestellt werden. 

### Starten des Pythonprogrammes
Wenn das Programm am Desktop liegt kann es mit dem nächsten Befehl gestartet werden, sonst muss der Pfad geändert werden.
```
sudo python3 /home/pi/Desktop/EvnSmartmeterMQTT.py
```

### Fehlermeldungen des Pythonprogrammes
Es sind bis jetzt nur zwei Fehlermeldungen implementiert!
* Wenn keine Verbindung zum Broker aufgebaut werden kann dann wird der Fehler "Die Ip Adresse des Brokers ist falsch!" ausgegeben. Zur Fehlerbehebung muss die richtige IP Adresse angegeben werden.
* Wenn der Fehler "Fehler beim Synchronisieren. Programm bitte ein weiteres Mal Starten." Kommt, muss man ca. drei Sekunden warten. Nach ein paar Versuchen sollte es problemlos starten.

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

Die Einheiten sind auf die Grundeinheit bezogen worden nicht wie im Folder des Netzbetreiber!
### Bugs
* Wenn eine PV-Anlage vorhanden ist und diese mehr produziert als unmittelbar verbraucht wird, erhählt man einen cos phi von ca. 60. Dieser hat physikalisch keine Bedeutung für mich. Im Normalfall ist dieser zwischen 0 - 1.

### Versionsunterschied
Es sind 2 Python Programme beide machen grundsätzlich dasselbe nur die Synchronisierung ist unterschiedlich. Es funktionieren beide aber sie wurden noch nicht im Dauereinsatz getestet. Jenes Programm, welches sich als stabiler herausstellt wird auf Dauer bleiben und das andere entfernt.

EvnSmartmeterMQTT.py
* Wenn es startet sollte es alle 5 Sekunden ohne Unterbrechung Werte senden.
* Der längste Dauertest war 14 Tage und dann ist es abgestürzt. (Fehler muss nicht im Skript sein kann ein Absturz vom Broker oder Pi selber gewesen sein)

EVNSmartmeterMQTT_V01.py
* Bei diesem Programm ist mir selber schon aufgefallen dass nicht alle 5 Sekunden Werte kommen aber dafür Syncronisiert es sich selber und stürtz nicht ab.
* Testzeitraum war ca. 24 Stunden.


### Roadmap (Updates)
Es soll eine Version mit einem ESP32 kommen, dieser liest die Daten ein und schickt sie auf einen bestehenden Server weiter. Um sich den Kabelweg zu sparen oder den Raspberry.
Wenn ich es schaffe will ich ein eigenes Modul auf den Markt bringen, dass Plug and Play funktioniert und nur einen Bruchteil eines Raspberry´s kostet.

### Hinweis
Alle Links zu Produkten sind Affiliate Links. Somit unterstützt ihr diese und weitere Projekte von mir.

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details