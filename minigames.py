from graphe import Noeud, Graphe
from random import randint

class Noeud_Minijeu(Noeud):
    def __init__(self, value, links = None):
        super().__init__(value, links)
        self.selected_by_player = False
        self.selected_by_game = False

class Mini_Jeux:
    def __init__(self, tileset, is_tree = False):
        self.is_tree = is_tree
        self.tileset = tileset


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
            print("( ", end="")
            arbreG.parcours_infixe()
            print(")", end="")
            print(" / ", end="")
        print(self.racine, end="")
        if arbreD:
            print(" \\ ", end="")
            print("( ", end="")
            arbreD.parcours_infixe()
            print(")", end="")

    def insert_into_abr(self, noeud):
        self.__init__(self.racine)

        arbreG, arbreD = self.get_root_left_and_right()
        if noeud.value < self.racine.value:
            if arbreG: arbreG.insert_into_abr(noeud)
            else: self.racine.links.append( (noeud, "gauche") )

        else:
            if arbreD: arbreD.insert_into_abr(noeud)
            else: self.racine.links.append( (noeud, "droite") )
        
        



def generate_AB_graphe(ranges = (0,50)):
    return ABR()

if __name__ == "__main__":
    generate_AB_graphe_min_hauteur(1).parcours_infixe()

