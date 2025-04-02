from graphe import Noeud, Graphe
from random import randint
from base import SCR_X, SCR_Y
from pygame.draw import line

MINIGAMES = {"F" : ["Somme voisin", "Somme sous-arbre"],
             "B" : ["Chemin court", "Insertion noeud ABR"],
             "U" : ["Cycle", "Valeur racine ?"]}


def init_F_somme_ABR():
    abr = generate_AB_graphe()
    random_node = randint(0, len(abr.liste_noeuds) - 1)
    abr.liste_noeuds[random_node].selected_by_game = True
    return abr, None

def init_B_insert_ABR():
    abr = generate_AB_graphe()
    insertValue = randint(0,50)
    return abr, insertValue

def init_U_root_ABR():
    abr = generate_AB_graphe()
    abr.racine.value = "?"
    return abr, None



class Noeud_Minijeu(Noeud):
    def __init__(self, value, links = None):
        super().__init__(value, links)
        self.selected_by_player = False
        self.selected_by_game = False



class Mini_Jeux:
    def __init__(self, tileset, func_init, func_check, func_additional_render = None, qst = "", is_tree = False):
        self.is_tree = is_tree
        self.tileset = tileset
        self.graphe, self.additional_data = func_init()
        self.question = qst
        self.func_check = func_check
        self.func_additional_render = func_additional_render

    def render_AB(self, screen):
        height = self.graphe.get_height()
        width = 2**height
        width_center = [(SCR_X - width*32) // 2, (SCR_X + width*32) // 2]
        height_max = 50*(height+1)
        start_height = abs(SCR_Y-height_max) // 2
        self.graphe.render(screen, self.tileset, width_center, start_height, 0, 0)
        

class ABR(Graphe):
    def __init__(self, noeud):
        super().__init__(noeud)
    
    def get_root_left_and_right(self):
        arbreG = None
        arbreD = None
        for n in self.racine.links:
            if n[1] == "gauche":
                arbreG = ABR(n[0])
            elif n[1] == "droite":
                arbreD = ABR(n[0])
        return arbreG, arbreD

    def parcours_infixe(self):
        self.__init__(self.racine)

        arbreG, arbreD = self.get_root_left_and_right()
        
        if arbreG:
            #print("( ", end="")
            arbreG.parcours_infixe()
          #  print(")", end="")
         #   print(" / ", end="")
        #print(self.racine, end="")
        if arbreD:
           # print(" \\ ", end="")
            #print("( ", end="")
            arbreD.parcours_infixe()
            #print(")", end="")
    
    def get_height(self):
        self.__init__(self.racine)
        arbreG, arbreD = self.get_root_left_and_right()
        valueG, valueD = -1, -1
        if arbreG : valueG = arbreG.get_height() #
        if arbreD : valueD = arbreD.get_height() #-- si ya pas de fils alors fin de recur
        return 1 + max(valueG, valueD)


    def insert_into_abr(self, noeud):
        self.__init__(self.racine)

        arbreG, arbreD = self.get_root_left_and_right()
        if noeud.value < self.racine.value:
            if arbreG: arbreG.insert_into_abr(noeud)
            else: self.racine.links.append( (noeud, "gauche") )

        else:
            if arbreD: arbreD.insert_into_abr(noeud)
            else: self.racine.links.append( (noeud, "droite") )
    
    def render(self, screen, tileset, width_range, height, offsX, offsY):
        x = (width_range[0] + width_range[1]) // 2

        tile = tileset.get_tile(0,0)
        if self.racine.selected_by_player:
            tile = tileset.get_tile(1,0)
        elif self.racine.selected_by_player:
            tile = tileset.get_tile(0,1)

        abrG, abrD = self.get_root_left_and_right()
        if abrG:
            line(screen, 0xAAAAAA, (x + 16, height + 16), ((width_range[0] + x) // 2 + 16, height + 50 + 16), 3)
            abrG.render(screen, tileset, [width_range[0], x], height + 50, offsX, offsY)
        
        if abrD:
            line(screen, 0xAAAAAA, (x + 16, height + 16), ((width_range[1] + x) // 2 + 16, height + 50 + 16), 3)
            abrD.render(screen, tileset, [x, width_range[1]], height + 50, offsX, offsY)
        
        screen.blit(tile, (x + offsX, height + offsY))


def generate_AB_graphe(ranges = (0,50)):
    noeud =  Noeud_Minijeu((ranges[1] - ranges[0]) // 2)
    abr = ABR(noeud)
    for i in range(randint(8,12)):
        abr.insert_into_abr(Noeud_Minijeu(randint(*ranges)))
    return abr


if __name__ == "__main__":
    import pygame
    import base
    from tile import Tileset
    abr = generate_AB_graphe()
    abr.parcours_infixe()
    clock = pygame.time.Clock()
    fenetre = base.initialise_window("a")
    eHndl = base.EventHandler( repeat = 800)

    mini = Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_ABR, lambda: None)
    loop = True
    while loop:

        if eHndl.update() == "QUIT":
            loop = False
        
        fenetre.fill((0,0,0))
        mini.render_AB(fenetre)
        pygame.display.flip()
        clock.tick(60)

    
