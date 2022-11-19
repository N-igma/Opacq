# Bluetooth: Eloan 
#hciconfig  = pour récup l'adresse mac

importation prise

serverMACAddress = '00: 1f: e1: dd: 08: 3d '
Port = 3
s = prise.prise(prise.AF_BLUETOOTH, prise.SOCK_STREAM, prise.BTPROTO_RFCOMM)
s.relier((serverMACAddress,Port))
tandis que 1:
    texte = contribution()
    si texte == "quitter":
        Pause
    s.envoyer(octets(texte, 'UTF-8'))
s.proche()
