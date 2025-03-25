import tile
from base import SCR_X, SCR_Y
from pygame.draw import line
OFFSX = (SCR_X - (4 * 10 * 8)) // 2 - 16
OFFSY = (SCR_Y - (4 * 10 * 8)) // 2 - 16
class Carte:
    def __init__(self, graphe):
        self.tileset = tile.Tileset("./graphics/builds.png")
        self.graphe = graphe
        
    def render(self, screen):
        for noeud in self.graphe.liste_noeuds:
            for neighbor_dist in noeud.links:
                neigh_node = neighbor_dist[0]
                vector = (noeud.coords[0] - neigh_node.coords[0], noeud.coords[1] - neigh_node.coords[1])
                offs = 3 if vector[1] > 0 or vector[1] == 0 and vector[0] > 0 else -3
                line(screen, 0x888888, ((noeud.coords[0] + (SCR_X - (4 * 10 * 8)) // 2), (noeud.coords[1] + (SCR_Y - (4 * 10 * 8)) // 2) + offs), ((neigh_node.coords[0] + (SCR_X - (4 * 10 * 8)) // 2), (neigh_node.coords[1] + (SCR_Y - (4 * 10 * 8)) // 2) + offs))
            
            noeud.render(screen, self.tileset.get_tile(noeud.value % 2, noeud.value // 2), OFFSX, OFFSY)
              

            