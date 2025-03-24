import graphe as g
import util
import carte
import base
import pygame
from random import randint
BUILD = [[0,(0,2)], [1,(3,4)], [2,(0,4)]]

def generate_map()->g.Graphe:
    listeNoeud = []  
    for x in range(5):
        for y in range(5):
            if randint(0,10) > 4:
                f,i,o = util.distance((x,y),BUILD[0][1]), util.distance((x,y),BUILD[1][1]), util.distance((x,y),BUILD[2][1])
                if f < i and f < o:
                    char = BUILD[0][0]
                elif i < f and i < o:
                    char = BUILD[1][0]
                else:
                    char = BUILD[2][0]

                listeNoeud.append(g.Noeud(char,((x * 10 + randint(-4,4)) * 8, (y * 10 + randint(-4,4)) * 8)))

    for noeud in listeNoeud:
        for other_noeud in listeNoeud:
            if other_noeud != noeud:
                coords1 = noeud.coords
                coords2 = other_noeud.coords
                dist = util.distance(coords1, coords2)
                if dist < 60*8:
                    noeud.links += [[other_noeud, dist]]

    listeNoeud[0].value = 3
    return g.Graphe(listeNoeud[0])

#print(generate_map().parcours_largeur(func = lambda x, retval: retval + x.links, base_retval_value=[]))
def main():
    clock = pygame.time.Clock()
    fenetre = base.initialise_window("a")
    carte_graphe = carte.Carte(generate_map())
    eHndl = base.EventHandler( repeat = 800)

    loop = True
    while loop:

        if eHndl.update() == "QUIT":
            loop = False

        fenetre.fill((0,0,0))
        carte_graphe.render(fenetre)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()