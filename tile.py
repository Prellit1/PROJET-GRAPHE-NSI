"""Module permettant d'obtenir des cases graphiques (tile) avec une image grace a la classe Tileset"""
from base import *

SIZE_TEX = 32


class Tileset:
    def __init__(self, image):
        self.tiles_surfaces = []
        img = pygame.image.load(image)

        # --------------- Découpe l'image original en plusieurs surfaces de 32 x 32 -----------------------
        for _ in range(img.get_rect().height // 32):
            self.tiles_surfaces.append([])
            
        self.y = img.get_rect().height // 32
        self.x = img.get_rect().width // 32

        for y in range(len(self.tiles_surfaces)):
            for x in range(img.get_rect().width // 32):
                tempSurf = pygame.surface.Surface((32, 32), pygame.SRCALPHA)
                
                tempSurf.blit(img, (x*-32, y*-32))
                self.tiles_surfaces[y].append(tempSurf.copy())
        # ------FIN------ Découpe l'image original en plusieurs surfaces de 32 x 32 -----------------------
    
    def get_tile(self, x, y):
        """
        Entrée: entier x et y

        Sortie: surface

        Role: renvoie la surface correspondant au coordonnée (x, y)
        dans l'attribut tiles_surfaces

        Version : 1.0
        """
        if x < 0 or y < 0 or x >= self.x or y >= self.y:
            return self.tiles_surfaces[0][0]
        return self.tiles_surfaces[y][x]
    

