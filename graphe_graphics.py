from graphe import *
from base import draw_arrow


class Graphe_Screen(Graphe):

    def render(self, screen, tileset, offsX, offsY, font, tile_determination_func):
        def render_node(node, retval):
            tile = tile_determination_func(node, tileset)
            return retval + node.render_arrow_and_get_node_command(screen, tile, offsX, offsY, font)
        
        cmds = self.racine.parcours_largeur(func=render_node, base_retval_value=[])
        for cmd in cmds:
            screen.blit(*cmd)

class Noeud_Screen(Noeud):
    def __init__(self, value, links=None, x=0, y=0):
        super().__init__(value, links)
        self.x = x
        self.y = y

    def render_arrow_and_get_node_command(self, screen, tile, offsX, offsY, font):
        node_commands = []

        for neighbour_dist in self.links:
            draw_arrow(screen, 0x888888, 3, 10, (self.x + 16 + offsX, self.y + 16 + offsY),
                       (neighbour_dist[0].x + 16  + offsX, neighbour_dist[0].y + 16 + offsY))

        
        node_commands.append((tile, (self.x + offsX, self.y + offsY)))
        if font:
            node_commands.append((font.render(str(self.value), False, (0, 0, 0)), (self.x + offsX + 8, self.y + offsY + 8)))
        return node_commands
    
    def check_clicked(self, eHndl, offsX, offsY):
        click = False
        if eHndl.mouse_press:
            if not (eHndl.mouse_press_pos[0] < (self.x + offsX) or eHndl.mouse_press_pos[0] > (self.x + offsX + 32) or  eHndl.mouse_press_pos[1] < (self.y + offsY) or eHndl.mouse_press_pos[1] > (self.y + offsY + 32)):
                click = True
        return click
