import graphe as g
import util
from random import randint
BUILD = [["F",(0,2)], ["I",(3,4)], ["O",(0,4)]]

def generate_map()->g.GrapheLs:
    graphe = g.GrapheLs()
    
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

                graphe.ajouter_noeud((char, (x, y)))

    for noeud in graphe.dict:
        for other_noeud in graphe.dict:
            coords1 = noeud[1]
            coords2 = other_noeud[1]
            dist = util.distance(coords1, coords2)
            if dist < 4:
                graphe.ajouter_arete(noeud, other_noeud, randint( int(dist+1), int(dist+3) ))
    
    return graphe

print(generate_map().dict)
