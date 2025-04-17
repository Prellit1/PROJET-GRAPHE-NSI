# Fichier créé par Ethan CAPONE le 18/09

# Modèle''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""
Entrée:
Sortie:
Role:
Version : 1.0
"""
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import pygame
from pygame.draw import polygon, line
from pygame.locals import *
from math import sqrt

SCR_X = 768
SCR_Y = 512


class EventHandler:
    def __init__(self, repeat=0, repeatInterval=200):
        self.press_repeat = {}
        self.pressed = {}
        pygame.key.set_repeat(repeat, repeatInterval)
        self.mouse_down = False
        self.mouse_press_pos = (0, 0)
        self.mouse_pos = (0, 0)
        self.mouse_offs = (0, 0)
        
    def update(self):
        """
        Sortie: string
        Role: Mets a jour l'attribut pressed en fonction des evenement Pygame sur le clavier et renvoie un string correspondant a si l'utilisateur tente de quitter le programme ou non
        Version : 1.0
        """
        self.pressed = {}
        self.press_repeat = {}
        self.mouse_offs = (0, 0)
        retVal = "OK"

        self.pressed = pygame.key.get_pressed()

        for ev in pygame.event.get():
            if ev.type == QUIT:
                retVal = "QUIT"    
            elif ev.type == KEYDOWN:
                self.press_repeat[ev.key] = (True, ev.unicode)
            elif ev.type == MOUSEBUTTONDOWN:
                self.mouse_down = True
                self.mouse_press_pos = ev.pos
                self.mouse_pos = ev.pos
            elif ev.type == MOUSEBUTTONUP:
                self.mouse_down = False
                self.mouse_offs = (0, 0)
                self.mouse_pos = ev.pos
            elif ev.type == MOUSEMOTION:
                self.mouse_offs = (ev.pos[0] - self.mouse_pos[0],
                                   ev.pos[1] - self.mouse_pos[1])
                self.mouse_pos = ev.pos

        return retVal


def distance2(coords, coords2):
    """
    Entrée: coords et coords2 : 2 tuples de 2 nombres
    correspondant a des valeurs X et Y

    Sortie: nombre (distance au carré)

    Role: Renvoie un nombre correspondant à la distance au carré entre 2
    points représenté par les 2 tuples en paramètre

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
    return pygame.display.set_mode((SCR_X, SCR_Y))

def draw_arrow(surface, color, width, head_width, coords1, coords2):
    line(surface, color, coords1, coords2, width)
    vector = (coords2[0] - coords1[0], coords2[1] - coords1[1])
    vec_orth = (-vector[1], vector[0])
    dist = sqrt(distance2(coords1, coords2))
    vec_orth = (vec_orth[0] / dist, vec_orth[1] / dist)
    vector = (vector[0] / dist, vector[1] / dist)
    points = [coords2,
               (int(coords2[0] - 3 * head_width * vector[0] + head_width * vec_orth[0]),
                 int(coords2[1] - 3 * head_width * vector[1] + head_width * vec_orth[1])),
               (int(coords2[0] - 3 * head_width * vector[0] - head_width * vec_orth[0]),
                 int(coords2[1] - 3 * head_width * vector[1] - head_width * vec_orth[1]))
            ]
    polygon(surface, color, points)
