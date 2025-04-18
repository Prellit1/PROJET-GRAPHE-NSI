from base import SCR_X, SCR_Y
from tile import Tileset
from math import sqrt
from graphe_graphics import *
from random import randint
from base import distance2

SCALE_FACTOR = 80
OFFSX = (SCR_X - (5 * SCALE_FACTOR + SCALE_FACTOR // 2 + 32)) // 2
OFFSY = (SCR_Y - (5 * SCALE_FACTOR + SCALE_FACTOR // 2 + 32)) // 2
TILESET = Tileset("./graphics/builds.png")
BUILD = [[0, (0 + OFFSX, 2 * 96 + OFFSY)], [1, (3 * 96 + OFFSX, 5 * 96 + OFFSY)], [2, (0 + OFFSX, 5 * 96 + OFFSY)]]

        
def generate_graphe(type_of_node=Noeud_Screen, range_node=(10, 15), max_links=3, max_link_dist=128):
    nodes = []
    for _ in range(randint(*range_node)):
        loop = True
        while loop:
            # Evite d'avoir 2 noeuds de meme coordonnées
            coords = (randint(0, 5), randint(0, 5))
            leave = True
            for noeud in nodes:
                if noeud.x == coords[0] and noeud.y == coords[1]:
                    leave = False
            if leave:
                loop = False
        nodes.append(type_of_node(None, x=coords[0], y=coords[1]))

    for node in nodes:
        #Scaling and centering on the base screen
        node.x *= SCALE_FACTOR
        node.x += randint(0, 40)
        node.y *= SCALE_FACTOR
        node.y += randint(0, 40) 

        node.x += OFFSX
        node.y += OFFSY

    for node in nodes:
        for potential_neigh in nodes:
            if potential_neigh != node and distance2((node.x, node.y), (potential_neigh.x, potential_neigh.y)) < (max_link_dist ** 2):
                
                dist = sqrt(distance2((node.x, node.y), (potential_neigh.x, potential_neigh.y)))
                
                if not node.node_linked(potential_neigh) and len(node.links) < max_links:
                    node.links.append((potential_neigh, dist))
                if not potential_neigh.node_linked(node) and len(potential_neigh.links) < 3:
                    potential_neigh.links.append((node, dist))
                    
    return Graphe_Screen(nodes[0])

def generate_carte():
    graphe = generate_graphe(range_node=(12,18))
    while len(graphe.liste_noeuds) < 12:
        graphe = generate_graphe(range_node=(12,18))
    
    for node in graphe.liste_noeuds:
        f, i, o = distance2((node.x, node.y), BUILD[0][1]), distance2((node.x, node.y), BUILD[1][1]), distance2((node.x, node.y), BUILD[2][1])
        if f < i and f < o:
            value = BUILD[0][0]
        elif i < f and i < o:
            value = BUILD[1][0]
        else:
            value = BUILD[2][0]
        node.value = value
    graphe.liste_noeuds[0].value = 3
    return graphe