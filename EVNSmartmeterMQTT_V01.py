from random import random
import serial
from binascii import unhexlify
import sys
import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
from Cryptodome.Cipher import AES
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from time import sleep
from gurux_dlms.TranslatorOutputType import TranslatorOutputType


# EVN Schlüssel eingeben zB. "36C66639E48A8CA4D6BC8B282A793BBB"
evn_schluessel = "EVN Schlüssel"

#MQTT Verwenden (True | False)
useMQTT = True

#MQTT Broker IP adresse Eingeben ohne Port!
mqttBroker = "192.168.1.10"
mqttuser =""
mqttpasswort = ""
mqttport = 1883

#Comport Config/Init
comport = "/dev/ttyUSB0"

#Aktulle Werte auf Console ausgeben (True | False)
printValue = True


# Holt Daten von serieller Schnittstelle
def recv(serialIncoming):
    while True:
        data = serialIncoming.read_all()
        if data == '':
            continue
        else:
            break
    return data

# Konvertiert Signed Ints
def s16(value):
    val = int(value, 16)
    return -(val & 0x8000) | (val & 0x7fff)

def s8(value):
    val = int(value, 16)
    return -(val & 0x80) | (val & 0x7f)

# DLMS Blue Book Page 52
# https://www.dlms.com/files/Blue_Book_Edition_13-Excerpt.pdf
units = {
            27: "W", # 0x1b
            30: "Wh", # 0x1e
            33: "A", #0x21
            35: "V", #0x23
            255: "" # 0xff: no unit, unitless
}


#MQTT Init
if useMQTT:
    try:
        client = mqtt.Client("SmartMeter")
        client.username_pw_set(mqttuser, mqttpasswort)
        client.connect(mqttBroker, mqttport)
    except Exception as e:
        print("Die IP-Adresse des Brokers ist falsch!")
        sys.exit()

    
tr = GXDLMSTranslator(TranslatorOutputType.SIMPLE_XML)
serIn = serial.Serial( port=comport,
         baudrate=2400,
         bytesize=serial.EIGHTBITS,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE
)

octet_string_values = {
    '0100010800FF': 'WirkenergieP',
    '0100020800FF': 'WirkenergieN',
    '0100010700FF': 'MomentanleistungP',
    '0100020700FF': 'MomentanleistungN',
    '0100200700FF': 'SpannungL1',
    '0100340700FF': 'SpannungL2',
    '0100480700FF': 'SpannungL3',
    '01001F0700FF': 'StromL1',
    '0100330700FF': 'StromL2',
    '0100470700FF': 'StromL3',
    '01000D0700FF': 'Leistungsfaktor'
}


while 1:
    sleep(4.7)
    daten = recv(serIn)

    if daten != '':
        daten = daten.hex()

    if daten == '' or daten[0:8] != "68fafa68":
        print ("Invalid Start Bytes... waiting")
        continue

    systemTitel = daten[22:38]
    frameCounter = daten[44:52]
    frame = daten[52:512]

    frame = unhexlify(frame)
    encryption_key = unhexlify(evn_schluessel)
    init_vector = unhexlify(systemTitel + frameCounter)
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=init_vector)
    apdu = cipher.decrypt(frame).hex()

    #MQTT
    if useMQTT:
        connected = False
        while not connected:
            try:
                client.reconnect()
                connected = True
            except Exception as e:
                print("MQTT-Verbindung verloren: Warte 2 Sekunden...")
                sleep(2)

    #MQTT
    if useMQTT:
        connected = False
        while not connected:
            try:
                client.reconnect()
                connected = True
            except:
                print("Lost Connection to MQTT...Trying to reconnect in 2 Seconds")
                time.sleep(2)

    try:
        xml = tr.pduToXml(apdu, )
        root = ET.fromstring(xml)
        found_lines = {}

        items = list(root.iter())
        for i, child in enumerate(items):
            if child.tag == 'OctetString' and 'Value' in child.attrib:
                value = child.attrib['Value']
                if value in octet_string_values.keys():
                    if 'Value' in items[i + 1].attrib:
                        found_lines[octet_string_values[value]] = int(items[i+1].attrib['Value'], 16)

    except Exception as err:
        print("Synchronisierungsfehler PDU: Warte auf neue Daten...")
        print()
        print("Fehler: ", format(err))
        serIn.flushOutput()
        serIn.close()
        serIn.open()
        sleep(1 + random())
        continue

    try:
        if {'MomentanleistungP', 'MomentanleistungN'}.issubset(found_lines.keys()):
            found_lines['Momentanleistung'] = found_lines['MomentanleistungP'] - found_lines['MomentanleistungN']

        for key, value in found_lines.items():
            if printValue:
                print(key, ':', found_lines[key])
            if useMQTT:
                client.publish("Smartmeter/" + key, found_lines['WirkenergieP'])

        print()

    except BaseException as err:
        print("Fehler: ", format(err))
        continue

