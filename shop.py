"""Module ou se situe les fonctions et classes utile au magasin du jeu"""

from graphe_graphics import *
from base import SCR_X, SCR_Y
from pygame.font import Font
from pygame.display import flip as pygame_display_flip
from pygame import K_RETURN, K_ESCAPE, Surface, SRCALPHA
from tile import Tileset

NOT_BUYABLE, BUYABLE, BOUGHT = 0, 1, 2
SIZE_FONT = 12

class Noeud_Shop(Noeud_Screen):
    def __init__(self, value, desc, stats, cout, links=None, x=0, y=0):
        super().__init__(value, links, x, y)
        self.description = desc
        self.buy_status = NOT_BUYABLE
        self.stats = stats
        self.cout = cout
    
    def buy(self, player):
        """
        ENTREE  : L'objet, un joueur
        SORTIE  : ---
        ROLE    : modifie des attributs de joueur et de l'objet en fonction des attributs de l'objet
        Version : 2025APR_01 
        """
        self.buy_status = BOUGHT
        player.money -= self.cout
        player.gains += self.stats[0]
        player.max_endurance += self.stats[1]
        player.endurance = player.max_endurance
        for node, _ in self.links:
            node.buy_status = BUYABLE

    def render_desc(self, screen, font, mouse_coords):
        """
        ENTREE  : L'objet, une surface, une police d'ecriture, des coordonnées de souris en tuple
        SORTIE  : ---
        ROLE    : place sur une surface des textes venant des attributs du noeud en fonction d'un tuple 
        Version : 2025APR_01 
        """
        nom = font.render(self.value, False, (200, 200, 200))
        desc = font.render(self.description, False, (200, 200, 200))
        txt = ", "
        if self.stats[0]: txt += "+" + str(self.stats[0])  + " de gains, "
        if self.stats[1]: txt += "+" + str(self.stats[1])  + " d'endurance, "
        txt = txt[2:-2]
        stat = font.render(txt, False, (200, 200, 200))
        cout = font.render(str(self.cout) + "$", False, (200, 200, 200))
        x = mouse_coords[0]
        y = mouse_coords[1] - 4 * SIZE_FONT
        if y < SIZE_FONT // 2: y = SIZE_FONT // 2
        if y + 4 * SIZE_FONT + SIZE_FONT // 2 > SCR_Y: y -= (y + 4 * SIZE_FONT + SIZE_FONT // 2) - SCR_Y

        surfaces = [nom, desc, stat, cout]
        max_len = 0
        for surface in surfaces:
            if max_len < surface.get_rect().w:
                max_len = surface.get_rect().w
        
        if x < SIZE_FONT // 2: x = SIZE_FONT // 2
        if x + max_len + SIZE_FONT // 2 > SCR_X: x -= (x + max_len + SIZE_FONT // 2) - SCR_X

        overlay = Surface((max_len + SIZE_FONT, (len(surfaces) + 1) * SIZE_FONT), SRCALPHA)
        overlay.fill((0, 0, 0, 64))

        screen.blit(overlay, (x - SIZE_FONT // 2, y - SIZE_FONT // 2))
        for surfaceID in range(len(surfaces)):
            screen.blit(surfaces[surfaceID], (x, y + surfaceID * SIZE_FONT))

        
def shop_init():
    """
    ENTREE  : ---
    SORTIE  : ---
    ROLE    : Initialise dans une variable globale le graphe représentant le magasin
    VERSION : 2025APR_01
    """

    global SHOP_GRAPH
    item1 = Noeud_Shop("Vie + saine", "Kanamei mange et boit mieux.", (2, 10), 50, x=0, y=2)
    item2 = Noeud_Shop("Vie + belle", "Kanamei souris +.", (3, 0), 100, x=1, y=1)
    item3 = Noeud_Shop("Vie + sportive", "Kanamei fait un peu de sport.", (0, 15), 100, x=1, y=3)
    item4 = Noeud_Shop("Vie + saine encore", "Kanamei mange et boit encore mieux.", (2, 10), 150, x=2, y=0)
    item5 = Noeud_Shop("Vie + à la mode", "Kanamei fait un peu trop attention à sa tenue.", (4, 0), 150, x=2, y=2)
    item6 = Noeud_Shop("Vie + sportive encore", "Kanamei fait + de sport.", (0, 10), 150, x=2, y=4)
    item7 = Noeud_Shop("Vie la + saine", "Kanamei est au top.", (4, 20), 200, x=4, y=2)
    # Note de l'autrice, considérant que ce perso a été un moyen de me représenter, ce sont des scénarios irréalistes

    item1.buy_status = BUYABLE
    item1.links = [(item2, 0), (item3, 0)] # Je garde le meme format pour les liaison
    item2.links = [(item4, 0), (item5, 0)]
    item3.links = [(item6, 0)]
    item4.links = [(item7, 0)]
    item6.links = [(item7, 0)]

    SCALE_FACTOR = 96
    SHOP_GRAPH = Graphe_Screen(item1)
    for node in SHOP_GRAPH.liste_noeuds:
        node.x *= SCALE_FACTOR
        node.y *= SCALE_FACTOR
        node.x += (SCR_X - (4 * SCALE_FACTOR + 32)) // 2
        node.y += (SCR_Y - (4 * SCALE_FACTOR + 32)) // 2


def shop_mode(clock, screen, eHndl, player):
    loop = True
    msg = "Quit"
    font = Font("RG.ttf",size=SIZE_FONT)
    tileset = Tileset("graphics/mini_node.png")
    selected_node = None
    player.endurance = player.max_endurance
    while loop:
        msg_key = eHndl.update()
        if msg_key == "QUIT":
            loop = False

        screen.fill((24, 24, 24))
        SHOP_GRAPH.render(screen, tileset, 0, 0, None, lambda node, tileset: tileset.get_tile(0, 1) if node == selected_node else tileset.get_tile(0, 0) if node.buy_status == BUYABLE else tileset.get_tile(1, 0) if node.buy_status == BOUGHT else tileset.get_tile(1, 1))
        
        for node in SHOP_GRAPH.liste_noeuds:
            if node.check_hovered(eHndl, 0, 0):
                node.render_desc(screen, font, eHndl.mouse_pos)

            if node.check_clicked(eHndl, 0, 0) and node.buy_status == BUYABLE:
                selected_node = node if selected_node != node else None

        if eHndl.press_repeat.get(K_RETURN) and selected_node:
            if player.money >= selected_node.cout:
                selected_node.buy(player)
                selected_node = None

        if eHndl.press_repeat.get(K_ESCAPE):
            msg = "MAP"
            loop = False
        
        screen.blit(font.render("ENDURANCE : " + str(int(player.endurance)), False, (255, 255, 255)), (0,0))
        screen.blit(font.render("MONEY : " + str(int(player.money)), False, (255, 255, 255)), (0,12))
        screen.blit(font.render("SCORE : " + str(int(player.score)), False, (255, 255, 255)), (0,24))
        
        pygame_display_flip()
        clock.tick(60)
    return msg