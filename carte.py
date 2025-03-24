import tile
from base import SCR_X, SCR_Y

class Carte:
    def __init__(self, graphe):
        self.tileset = tile.Tileset("./graphics/builds.png")
        self.graphe = graphe
        
    def render(self, screen):
        for noeud in self.graphe.liste_noeuds:
            screen.blit(self.tileset.get_tile(noeud.value % 2, noeud.value // 2), (noeud.coords[0] + (SCR_X - (4 * 10 * 8)) // 2, noeud.coords[1] + (SCR_Y - (4 * 10 * 8)) // 2))


            