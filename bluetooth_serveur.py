
importation prise

hostMACAddress = '1C:1B:B5:4B:DE:FC ' # L'adresse MAC d'un adaptateur Bluetooth sur le serveur. Le serveur peut avoir plusieurs adaptateurs Bluetooth.
Port = 3 # 3 est un choix arbitraire. Cependant, il doit correspondre au port utilisé par le client.
arriéré = 1
Taille = 1024
s = prise.prise(prise.AF_BLUETOOTH, prise.SOCK_STREAM, prise.BTPROTO_RFCOMM)
s.lier((hostMACAddress,Port))
s.écoute(arriéré)
essayer:
    client, adresse = s.Acceptez()
    tandis que 1:
        Les données = client.recv(Taille)
        si Les données:
            impression(Les données)
            client.envoyer(Les données)
sauf:	
    impression("Prise de fermeture")	
    client.proche()
    s.proche()
