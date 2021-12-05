import serial

#from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QMessageBox
#from encrypter_decrypter_ui_new import Ui_MainWindow
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from binascii import unhexlify
import sys
import os
import string
import paho.mqtt.client as mqtt


from gurux_dlms.GXDLMSTranslator import GXDLMSTranslator
from bs4 import BeautifulSoup


# Check if i have HEX string
def check_input(stringa_input):

        if stringa_input.isalnum():

            return unhexlify(stringa_input)

        if stringa_input == "-1":

            return False  # Questo if mi serve per evitare di mostrare una doppia MSGbox

        else:

            # Creo la messagebox di errore
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong data!")
            msg.setWindowTitle("Error!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_() #Serve per visualizzare la messagebox

            return False



comport = "/dev/ttyUSB0"
key = "016F76543557DE95260DA068B9C640A9"
security_control_byte = ["30", "10"]
tr = GXDLMSTranslator()
ser = serial.Serial( port=comport,
         baudrate=2400,
         bytesize=serial.EIGHTBITS,
         parity=serial.PARITY_NONE,                   
)

#MQTT Init
mqttBroker = "192.168.1.99"
client = mqtt.Client("SmartMeter")
client.connect(mqttBroker)
while 1:
    daten = ser.read(size=282).hex()
    systemTitel = daten[22:38]
    frameCounter = daten[44:52]
    frame = daten[52:560]
    
    cipher_apdu = frame  # Remove newline and space

    string_chiper_apdu = check_input(cipher_apdu)


    encryption_key = check_input(key)

    aad = check_input(security_control_byte[0])

    init_vector = check_input(systemTitel + frameCounter)


    aesgcm = AESGCM(encryption_key)
    apdu = aesgcm.encrypt(init_vector, string_chiper_apdu, aad)
    apdu_to_string = apdu.hex()
    

    xml = tr.pduToXml(apdu_to_string[:-32],)


    soup = BeautifulSoup(xml, 'lxml')
    results_32 = soup.find_all('uint32')
    results_16 = soup.find_all('uint16')
    results_int16 = soup.find_all('int16')


    #Wirkenergie A+ in Wattstunden
    WirkenergiePA = str(results_32[0])
    WirkenergieP = int(WirkenergiePA[WirkenergiePA.find('=')+2:WirkenergiePA.find('=')+10],16)
    print('Wirkenergie+: ' + str(WirkenergieP))

    #Wirkenergie A- in Wattstunden
    WirkenergieNA = str(results_32[1])
    WirkenergieN = int(WirkenergieNA[WirkenergiePA.find('=')+2:WirkenergiePA.find('=')+10],16)
    print('Wirkenergie: ' + str(WirkenergieN))

    #Momentanleistung P+ in Watt
    MomentanleistungPA = str(results_32[2])
    MomentanleistungP = int(MomentanleistungPA[MomentanleistungPA.find('=')+2:MomentanleistungPA.find('=')+10],16)
    print('MomentanleistungP+: ' + str(MomentanleistungP))

    #Momentanleistung P- in Watt
    MomentanleistungNA = str(results_32[3])
    MomentanleistungN = int(MomentanleistungNA[MomentanleistungNA.find('=')+2:MomentanleistungNA.find('=')+10],16)
    print('MomentanleistungP-: ' + str(MomentanleistungN))

    #Spannung L1
    SpannungL1A = str(results_16[0])
    SpannungL1 = int(SpannungL1A[SpannungL1A.find('=')+2:SpannungL1A.find('=')+6],16)*0.1
    print('Spannung L1: ' + str(SpannungL1))

    #Spannung L2
    SpannungL2A = str(results_16[1])
    SpannungL2 = int(SpannungL2A[SpannungL2A.find('=')+2:SpannungL2A.find('=')+6],16)*0.1
    print('Spannung L2: ' + str(SpannungL2))

    #Spannung L3
    SpannungL3A = str(results_16[2])
    SpannungL3 = int(SpannungL3A[SpannungL3A.find('=')+2:SpannungL3A.find('=')+6],16)*0.1
    print('Spannung L3: ' + str(SpannungL3))

    #Strom L1
    StromL1A = str(results_16[3])
    StromL1 = int(StromL1A[StromL1A.find('=')+2:StromL1A.find('=')+6],16)*0.01
    print('Strom L1: ' + str(StromL1))

    #Strom L2
    StromL2A = str(results_16[4])
    StromL2 = int(StromL2A[StromL2A.find('=')+2:StromL2A.find('=')+6],16)*0.01
    print('Strom L2: ' + str(StromL2))

    #Strom L3
    StromL3A = str(results_16[5])
    StromL3 = int(StromL3A[StromL3A.find('=')+2:StromL3A.find('=')+6],16)*0.01
    print('Strom L3: ' + str(StromL3))

    #Leistungsfaktor
    LeistungsfaktorA = str(results_int16[0])
    Leistungsfaktor = int(LeistungsfaktorA[LeistungsfaktorA.find('=')+2:LeistungsfaktorA.find('=')+6],16)*0.001
    print('Leistungsfaktor: ' + str(Leistungsfaktor))
    print()
    print()
    
    
    #MQTT
    client.publish("Smartmeter/WirkenergieP",WirkenergieP)
    client.publish("Smartmeter/WirkenergieN",WirkenergieN)
    client.publish("Smartmeter/MomentanleistungP",MomentanleistungP)
    client.publish("Smartmeter/SpannungL1",SpannungL1)
    client.publish("Smartmeter/SpannungL2",SpannungL2)
    client.publish("Smartmeter/StromL1",StromL1)
    client.publish("Smartmeter/StromL2",StromL2)
    client.publish("Smartmeter/StromL3",StromL3)
    client.publish("Smartmeter/Leistungsfaktor",Leistungsfaktor)