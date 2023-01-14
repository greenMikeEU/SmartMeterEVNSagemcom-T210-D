# Alle Infos zu diesem Projekt befinden sich auf meinem Blog
https://www.michaelreitbauer.at/smart-meter-monitoring/


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


### Unterstützung
Spendenlink: https://www.paypal.me/greenMikeEU

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details

## Benötigte Python Pakete

Unter Debian kann man die benötigten Python Pakete wie folgt installieren:
```shell
apt install python3-serial python3-pycryptodome python3-pip
```

Additionally you need unpackaged python packages:
```shell
pip install gurux_dlms
```
