# setup service

sudo ./setup.sh


## operate
```bash
sudo systemctl daemon-reload
sudo systemctl restart smartmeter.service
sudo systemctl status smartmeter.service
```
## fix

sudo vi "/etc/systemd/system/smartmeter.service"

```bash
[Unit]
Description=SmartMeterData Script
After=multi-user.target
Wants=network-online.target

[Service]
Type=notify
Environment=PYTHONUNBUFFERED=true
Restart=always
ExecStart=/usr/bin/python3 /home/smartmeter/SmartMeterEVNSagemcom-T210-D/AusleseSkript.py
WatchdogSec=60
RestartSec=20

[Install]
WantedBy=multi-user.target
```
