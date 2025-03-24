#Fichier créé par Ethan CAPONE le 18/09

#Modèle''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""
Entrée:
Sortie:
Role:
Version : 1.0
"""
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

import pygame
from pygame.locals import *

SCR_X = 768
SCR_Y = 512


class EventHandler:
    def __init__(self,repeat=0,repeatInterval=200):
        self.pressed = {}
        pygame.key.set_repeat(repeat,repeatInterval)
        
    def update(self):
        """
        Sortie: string
        Role: Mets a jour l'attribut pressed en fonction des evenement Pygame sur le clavier et renvoie un string correspondant a si l'utilisateur tente de quitter le programme ou non
        Version : 1.0
        """
        self.pressed = {}
        retVal = "OK"
        
        for ev in pygame.event.get():
            
            if ev.type == QUIT:
                retVal = "QUIT"
                
            elif ev.type == KEYDOWN:
                self.pressed[ev.key] = True
                
            
        #print(self.pressed, retVal)
        return retVal

def distance2(coords, coords2):
    """
    Entrée: coords et coords2 : 2 tuples de 2 nombres correspondant a des valeurs X et Y
    Sortie: nombre (distance au carré)
    Role: Renvoie un nombre correspondant à la distance au carré entre 2 points représenté par les 2 tuples en paramètre
    Version : 1.0
    """
    return (abs(coords[0]-coords2[0]))**2 + (abs(coords[1]-coords2[1]))**2

def sign(num):
    """
    Entrée: nombre
    Sortie: nombre (1 ou -1)
    Role: renvoie le nombre 1 avec le signe du nombre en parametre
    Version : 1.0
    """
    return num / abs(num)


def initialise_window(title: str):
    """
    Sortie: Fenètre
    Role: crée et renvoie la fenètre du programme
    Version : 1.0
    """
    
    pygame.init()
    pygame.display.set_caption(title)
    return pygame.display.set_mode( (SCR_X, SCR_Y) )