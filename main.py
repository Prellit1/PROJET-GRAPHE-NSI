import graphe as g
import util
import carte
import base
import pygame
from random import randint
BUILD = [[0,(0,2)], [1,(3,4)], [2,(0,4)]]

def generate_map()->g.Graphe:
    listeNoeud = []  
    while len(listeNoeud) < 6 or len(listeNoeud) > 12:
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

                    listeNoeud.append(carte.Noeud_Carte(char,((x * 10 + randint(-3,3)) * 8, (y * 10 + randint(-3,3)) * 8)))

    for noeud in listeNoeud:
        coords1 = noeud.coords

        for other_noeud in listeNoeud:
            if other_noeud != noeud:
                already_connected_to_a_neighbour = False
                for n in noeud.links:
                    for linkID in range(len(n[0].links)):
                        if other_noeud in n[0].links[linkID]:
                            already_connected_to_a_neighbour= True
                
                coords2 = other_noeud.coords
                dist2 = util.distance(coords1, coords2)

                if dist2 < 200**2 and not already_connected_to_a_neighbour:
                    noeud.links += [(other_noeud, dist2)]
                

    racineID = randint(0, len(listeNoeud)-1)
    #print(len(listeNoeud))
    #print(listeNoeud[racineID].links)
    listeNoeud[racineID].value = 3
    return g.Graphe(listeNoeud[racineID])

#print(generate_map().parcours_largeur(func = lambda x, retval: retval + x.links, base_retval_value=[]))
def main():
    clock = pygame.time.Clock()
    fenetre = base.initialise_window("a")
    graphe = generate_map()
    carte_graphe = carte.Carte(graphe)
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