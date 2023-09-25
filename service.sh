#!/bin/bash
dateipfad=$(cd `dirname $0` && pwd)
echo $dateipfad
filename="/etc/systemd/system/smartmeter.service"
[ -e $filename ] && sudo rm $filename

echo "[Unit]" >> "$filename"
echo "Description=SmartMeterData Script" >> "$filename"
echo "After=multi-user.target" >> "$filename"
echo "Wants=network-online.target" >> "$filename"
echo "" >> "$filename"

echo "[Service]" >> "$filename"
echo "Type=notify" >> "$filename"
echo "Environment=PYTHONUNBUFFERED=true" >> "$filename"
echo "Restart=always" >> "$filename"
echo "#Script wird wiederartet wenn abstür" >> "$filename"
echo "ExecStart=/usr/bin/python3 $dateipfad/AusleseSkript.py" >> "$filename"
echo "WatchdogSec=60" >> "$filename"
echo "RestartSec=20" >> "$filename"

echo "" >> "$filename"
echo "[Install]" >> "$filename"
echo "WantedBy=multi-user.target" >> "$filename"
echo "File $filename created."
sudo systemctl daemon-reload 
sudo systemctl enable smartmeter.service
sudo systemctl start smartmeter.service

# [Unit]
# Description=SmartMeterData Script
# After=multi-user.target
# Wants=network-online.target

# [Service]
# Type=notify
# Environment=PYTHONUNBUFFERED=true
# Restart=always
# ExecStart=/usr/bin/python3 /home/smartmeter/SmartMeterEVNSagemcom-T210-D/AusleseSkript.py
# WatchdogSec=60
# RestartSec=20

# [Install]
# WantedBy=multi-user.target