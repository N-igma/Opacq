
import socket

hostMACAddress = '1C:1B:B5:4B:DE:FC ' # L'adresse MAC d'un adaptateur Bluetooth sur le serveur. Le serveur peut avoir plusieurs adaptateurs Bluetooth.
Port = 3 # 3 est un choix arbitraire. Cependant, il doit correspondre au port utilisé par le client.
arriéré = 1
Taille = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.lier((hostMACAddress,Port))
s.écoute(arriéré)
try:
    client, adresse = s.Acceptez()
    while 1:
        données = client.recv(Taille)
        if données:
            print(données)
            client.envoyer(données)
except:	
    print("socket de fermeture")	
    client.proche()
    s.proche()
