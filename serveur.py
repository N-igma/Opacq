'''
Ce programme attend des messages de clients et les traite,
Lancement : python3 serveur.py
Arrêt : ctrl-c
Fonctionne avec python 3 et ses modules de base.
'''

# le module de gestion des échanges
from comSockSrv import *

class MonServeur(ComSockSrv):
    '''Classe de gestion des messages côté serveur.
    Hérite des fonctions de gestion de ComSockSrv .
    Traite les commandes de service des clients, et renvoie les résultats.'''

    def traiteMsg(self,objet):
        '''Votre traitement ici.
        "objet" contient l'objet python envoyé par le client.
        Vous devez renvoyer un autre objet python lorsque votre
        traitement est terminé'''

        # cet exemple renvoie simplement une chaîne
        return 'Ouais, ici ça tourne ! On en dira pas plus...'

# instantiation de la classe
monService = MonServeur()
# démarre l'écoute, et donc les traitements associés
monService.run()
