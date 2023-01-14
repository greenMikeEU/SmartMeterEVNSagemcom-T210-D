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

## Als user systemd service laufen lassen

Man kann das script auch via ein user systemd service laufen lassen. Hierzu ist es notwedig, dem User als erstes das Ausführen von systemd services auch ohne Anmeldung zu gestatten (https://wiki.archlinux.org/title/Systemd/User#Automatic_start-up_of_systemd_user_instances):

```sh
sudo loginctl enable-linger username
```

Dann muss das notwendige Verzeichnis erstellt werden:
```sh
mkdir -p ~/.config/systemd/user/
```

Und die systemd service unit (evn_smartmeter.service):

```
[Unit]
Description=EVN SmartMonitor
Documentation=https://github.com/greenMikeEU/SmartMeterEVNSagemcom-T210-D
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/home/pkolmann/SmartMeterEVNSagemcom-T210-D
ExecStart=/usr/bin/python3 ./EVNSmartmeterMQTT_V01.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
```

Zum Abschluss muss der systemd daemon die neue config laden, enablen und starten:

```sh
systemctl --user daemon-reload
systemctl --user enable evn_smartmeter.service
systemctl --user start evn_smartmeter.service
```

Zur Kontrolle, ob das Service läuft kann man den Status abfragen:
```sh
systemctl --user status evn_smartmeter.service
```

bzw. das Journal ansehen:
```sh
journalctl --user-unit evn_smartmeter.service
```
