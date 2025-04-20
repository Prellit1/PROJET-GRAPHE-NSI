"""Module utile pour la représentation de graphes sur un ecran"""

from graphe import *
from base import draw_arrow


class Graphe_Screen(Graphe):

    def render(self, screen, tileset, offsX, offsY, font, tile_determination_func):
        """
        ENTREE  : l'objet, Surface, Jeu de case, Entier, Entier, une police d'ecriture, une fonction
        SORTIE  : ---
        ROLE    : Permet de mettre sur une surface une représentation de l'objet décaler par les 2 entiers sur les 2 axes avec possibilité d'avoir la valeur des noeuds composant l'objet écrite dans eux. Ce qui représente les noeuds sont determiné par la fonction passé en parametre qui a pour entrée un noeud et un jeu de case.
        VERSION : 2025APR_01
        """
        def render_node(node, retval):
            tile = tile_determination_func(node, tileset)
            return retval + node.render_arrow_and_get_node_command(screen, tile, offsX, offsY, font)
        
        cmds = self.racine.parcours_largeur(func=render_node, base_retval_value=[])
        for cmd in cmds:
            screen.blit(*cmd)

class Noeud_Screen(Noeud):
    def __init__(self, value, links=None, x=0, y=0):
        super().__init__(value, links)
        self.x = x
        self.y = y

    def render_arrow_and_get_node_command(self, screen, tile, offsX, offsY, font):
        """
        ENTREE  : l'objet, Surface, une case graphique, deux entier, et potentiellement une police d'ecriture
        SORTIE  : Liste de tuple
        ROLE    : Place sur une surface des fleches représentant la liaison du noeud a d'autre noeuds et renvoie des tuples utilisables pour afficher sur une surface le noeud.
        VERSION : 2025APR_01
        """
        node_commands = []

        for neighbour_dist in self.links:
            draw_arrow(screen, 0x888888, 3, 10, (self.x + 16 + offsX, self.y + 16 + offsY),
                       (neighbour_dist[0].x + 16  + offsX, neighbour_dist[0].y + 16 + offsY))

        node_commands.append((tile, (self.x + offsX, self.y + offsY)))
        if font:
            node_commands.append((font.render(str(self.value), False, (0, 0, 0)), (self.x + offsX + 8, self.y + offsY + 8)))
        return node_commands
    
    def check_clicked(self, eHndl, offsX, offsY):
        """
        ENTREE  : l'objet, gestionnaire d'evenement, décalage X et Y du rendu du noeud en 2 entier
        SORTIE  : bool
        ROLE    : Vérifie si la représentation de l'objet sur l'ecran a été cliqué et renvoit vrai si oui
        VERSION : 2025APR_01
        """
        click = False
        if eHndl.mouse_press:
            if not (eHndl.mouse_press_pos[0] < (self.x + offsX) or eHndl.mouse_press_pos[0] > (self.x + offsX + 32) or  eHndl.mouse_press_pos[1] < (self.y + offsY) or eHndl.mouse_press_pos[1] > (self.y + offsY + 32)):
                click = True
        return click
    
    def check_hovered(self, eHndl, offsX, offsY):
        """
        ENTREE  : l'objet, gestionnaire d'evenement, décalage X et Y du rendu du noeud en 2 entier
        SORTIE  : bool
        ROLE    : Vérifie si la représentation de l'objet sur l'ecran est survolée et renvoit vrai si oui
        VERSION : 2025APR_01
        """
        hover = False
        if not (eHndl.mouse_pos[0] < (self.x + offsX) or eHndl.mouse_pos[0] > (self.x + offsX + 32) or  eHndl.mouse_pos[1] < (self.y + offsY) or eHndl.mouse_pos[1] > (self.y + offsY + 32)):
            hover = True
        return hover
