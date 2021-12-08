import serial
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from binascii import unhexlify
import sys
import string
import paho.mqtt.client as mqtt
from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from bs4 import BeautifulSoup
from Cryptodome.Cipher import AES
from time import sleep
from gurux_dlms.TranslatorOutputType import TranslatorOutputType


# EVN Schlüssel als String eingeben also mit ""
evn_schluessel = "EVN Schlüssel"

#MQTT Verwenden (True | False)
useMQTT = True

#MQTT Broker IP adresse Eingeben ohne Port!
mqttBroker = "192.168.8.99"

#Comport Config/Init
comport = "/dev/ttyUSB0"

#Aktulle Werte auf Console ausgeben (True | False)
printValue = True


# Hohlt daten von Serieler Schnittstelle
def recv(serialIncoming):
    while True:
        data = serialIncoming.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.5)
    return data
    

#MQTT Init 
if useMQTT:
    try:
        client = mqtt.Client("SmartMeter")
        client.connect(mqttBroker)
    except:
        print("Die Ip Adresse des Brokers ist falsch!")
        sys.exit()

    
tr = GXDLMSTranslator(TranslatorOutputType.SIMPLE_XML)
serIn = serial.Serial( port=comport,
         baudrate=2400,
         bytesize=serial.EIGHTBITS,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE
)


while 1:
    sleep(4.7)
    #daten = ser.read(size=282).hex()
    daten = recv(serIn)
    if daten != '':
        daten = daten.hex()
    if (daten == '' or daten[0:8] != "68010168"):
        print ("Invalid Start Bytes... waiting")
        continue
    #print ("Daten: ", daten);
    systemTitel = daten[22:38]
    frameCounter = daten[44:52]
    frame = daten[52:560]
    #print("SystemTitle: ", systemTitel)
    #print("FrameCounter: ", frameCounter)
    

    frame = unhexlify(frame)
    encryption_key = unhexlify(evn_schluessel)
    init_vector = unhexlify(systemTitel + frameCounter)
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=init_vector)
    apdu = cipher.decrypt(frame).hex()
    #print("APDu: ", apdu)    

    try:
        xml = tr.pduToXml(apdu,)
        soup = BeautifulSoup(xml, 'lxml')
        results_32 = soup.find_all('uint32')
        results_16 = soup.find_all('uint16')
        results_int16 = soup.find_all('int16')

    except BaseException as err:
        print("Fehler: ", format(err))
        continue;
       

    try:
        #Wirkenergie A+ in Wattstunden
        WirkenergiePA = str(results_32[0])
        WirkenergieP = int(WirkenergiePA[WirkenergiePA.find('=')+2:WirkenergiePA.find('=')+10],16)

        #Wirkenergie A- in Wattstunden
        WirkenergieNA = str(results_32[1])
        WirkenergieN = int(WirkenergieNA[WirkenergiePA.find('=')+2:WirkenergiePA.find('=')+10],16)
        
        #Momentanleistung P+ in Watt
        MomentanleistungPA = str(results_32[2])
        MomentanleistungP = int(MomentanleistungPA[MomentanleistungPA.find('=')+2:MomentanleistungPA.find('=')+10],16)

        #Momentanleistung P- in Watt
        MomentanleistungNA = str(results_32[3])
        MomentanleistungN = int(MomentanleistungNA[MomentanleistungNA.find('=')+2:MomentanleistungNA.find('=')+10],16)
        
        #Spannung L1
        SpannungL1A = str(results_16[0])
        SpannungL1 = int(SpannungL1A[SpannungL1A.find('=')+2:SpannungL1A.find('=')+6],16)*0.1
        
        #Spannung L2
        SpannungL2A = str(results_16[1])
        SpannungL2 = int(SpannungL2A[SpannungL2A.find('=')+2:SpannungL2A.find('=')+6],16)*0.1
        
        #Spannung L3
        SpannungL3A = str(results_16[2])
        SpannungL3 = int(SpannungL3A[SpannungL3A.find('=')+2:SpannungL3A.find('=')+6],16)*0.1
        
        #Strom L1
        StromL1A = str(results_16[3])
        StromL1 = int(StromL1A[StromL1A.find('=')+2:StromL1A.find('=')+6],16)*0.01
        
        #Strom L2
        StromL2A = str(results_16[4])
        StromL2 = int(StromL2A[StromL2A.find('=')+2:StromL2A.find('=')+6],16)*0.01
        
        #Strom L3
        StromL3A = str(results_16[5])
        StromL3 = int(StromL3A[StromL3A.find('=')+2:StromL3A.find('=')+6],16)*0.01
        
        #Leistungsfaktor
        LeistungsfaktorA = str(results_int16[0])
        Leistungsfaktor = int(LeistungsfaktorA[LeistungsfaktorA.find('=')+2:LeistungsfaktorA.find('=')+6],16)*0.001
                        
        if printValue:
            print('Wirkenergie+: ' + str(WirkenergieP))
            print('Wirkenergie: ' + str(WirkenergieN))
            print('MomentanleistungP+: ' + str(MomentanleistungP))
            print('MomentanleistungP-: ' + str(MomentanleistungN))
            print('Spannung L1: ' + str(SpannungL1))
            print('Spannung L2: ' + str(SpannungL2))
            print('Spannung L3: ' + str(SpannungL3))
            print('Strom L1: ' + str(StromL1))
            print('Strom L2: ' + str(StromL2))
            print('Strom L3: ' + str(StromL3))
            print('Leistungsfaktor: ' + str(Leistungsfaktor))
            print('Momentanleistung: ' + str(MomentanleistungP-MomentanleistungN))
            print()
            print()
        
        #MQTT
        if useMQTT:
            client.publish("Smartmeter/WirkenergieP",WirkenergieP)
            client.publish("Smartmeter/WirkenergieN",WirkenergieN)
            client.publish("Smartmeter/MomentanleistungP",MomentanleistungP)
            client.publish("Smartmeter/MomentanleistungN",MomentanleistungN)
            client.publish("Smartmeter/Momentanleistung",MomentanleistungP - MomentanleistungN)
            client.publish("Smartmeter/SpannungL1",SpannungL1)
            client.publish("Smartmeter/SpannungL2",SpannungL2)
            client.publish("Smartmeter/SpannungL3",SpannungL3)
            client.publish("Smartmeter/StromL1",StromL1)
            client.publish("Smartmeter/StromL2",StromL2)
            client.publish("Smartmeter/StromL3",StromL3)
            client.publish("Smartmeter/Leistungsfaktor",Leistungsfaktor)
    except BaseException as err:
        print("Fehler: ", format(err))
        continue;