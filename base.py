"""Module contenant certaine fonctions primordiales ainsi qu'un gestionnaire d'evenement pour des programmes Pygame"""

# Modèle''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""
ENTREE  :
SORTIE  :
ROLE    :
VERSION : [ANNEE][MOIS]_[ITERATION EN 2 CHIFFRES] # ex : 2025APR_01
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
        self.mouse_press = False
        self.mouse_held = False
        self.mouse_press_pos = (0, 0)
        self.mouse_pos = (0, 0)
        self.mouse_offs = (0, 0)
        
    def update(self):
        """
        Sortie: string
        Role: Mets a jour l'attribut pressed en fonction des evenement Pygame sur le clavier et la souris et renvoie un string correspondant a si l'utilisateur tente de quitter le programme ou non
        Version : 2025APR_01
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

        if self.mouse_down:
            if not self.mouse_press and not self.mouse_held:
                self.mouse_press = True
            else:
                self.mouse_press = False
                self.mouse_held = True
        else:
            self.mouse_press = False
            self.mouse_held = False

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
    """
    ENTREE  : Surface, valeur représentant une couleur, un réel, un autre, 2 tuple représentant les coordonnées d'un point A et un point B
    SORTIE  : ----
    ROLE    : Place sur une surface une fleche allant d'un point A a un point B avec une couleur précise, une épaisseur précise et une taille de la pointe precise
    VERSION : 2025APR_01
    """
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

def same_values_between_2_lists(l1, l2):
    """
    ENTREE  : 2 listes
    SORTIE  : boolean
    ROLE    : permet de savoir si 2 liste ont les memes élément (DOUBLONS POSSIBLE)
    VERSION : 2025APR_01
    """
    for elem in l1:
        if elem not in l2:
            return False
    for elem in l2:
        if elem not in l1:
            return False
    return True

def loadBG(file):
    """
    Entrée: String representant un fichier image
    Sortie: Surface contenant une image
    Role: renvoie une surface contenant l'arrière plan du menu contenant l'image File
    Version : 1.0
    """
    return pygame.image.load(file)

def center_text_surface(txt_surf, TLC, BRC):
    """
    ENTREE  : Surface, tuple de 2 valeur représentant les coordonnées du coins superieur gauche et un autre du coin inférieur droit
    SORTIE  : Tuple de 2 valeur représentant des coordonnés 
    ROLE    : Permet d'obtenir des coordonnées permettant le centrage d'une surface dans un rectangle déterminer par son coin sup gauche et son coins inf droite
    VERSION : 2025APR_01
    """
    width = BRC[0] - TLC[0]
    height = BRC[1] - TLC[1] 
    return (TLC[0] + (width - txt_surf.get_rect().w) // 2, TLC[1] + (height - txt_surf.get_rect().h) // 2)

        
