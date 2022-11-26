'''
Ce programme affiche et envoie un message au serveur,
puis reçoit et affiche la réponse.
Lancement : python3 client.py
Fonctionne avec python 3 et ses modules de base.
'''

# le module de gestion des échanges
from comSockCli import *

# nom du serveur qui attend les messages.
# Ce nom doit pouvoir répondre à une commande "ping nom_serveur" 
host = 'monServeur'
# instantiation de la classe
maCom = ComSockCli(host)
# prépare un objet à transmettre, en l'occurrence une liste
msg = ['Salut les gars ! Tout va bien sur le serveur ?','On en attend un roman']
#
print(msg)
# transmet l'objet et reçoit la réponse
reponse = maCom.envoi(msg)
#
print(reponse)
