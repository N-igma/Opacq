# Bluetooth: Eloan 
#hciconfig  = pour récup l'adresse mac

import socket

serverMACAddress = '1c:1b:b5:4b:de:fc'
Port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,Port))
while 1:
    texte = input()
    if texte == "quitter":
        break
    s.send(bytes(texte, 'UTF-8'))
s.close()
