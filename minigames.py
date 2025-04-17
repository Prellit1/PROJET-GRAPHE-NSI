from graphe import Noeud, Graphe
from random import randint
from base import SCR_X, SCR_Y, draw_arrow, distance2, same_values_between_2_lists
from pygame import K_BACKSPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, Rect, Surface, SRCALPHA
from math import sqrt
from tile import Tileset

def init_F_somme_ABR():
    abr = generate_AB_graphe()
    random_node = randint(0, len(abr.liste_noeuds) - 1)
    abr.liste_noeuds[random_node].selected_by_game = True
    return abr, ABR(abr.liste_noeuds[random_node])

def check_F_somme_ABR(_, add_data, answer):
    real_deal = add_data.parcours_largeur()
    if answer.isdigit():
        if int(answer) == real_deal:
            return True
    return False

def init_F_somme_GRP():
    grp = generate_graphe()
    random = randint(0, len(grp.liste_noeuds) - 1)
    node = grp.liste_noeuds[random]
    node.selected_by_game = True
    return grp, node

def check_F_somme_GRP(_, add_data, answer):
    sum = add_data.value
    for node_dist in add_data.links:
        sum += node_dist[0].value

    if answer.isdigit():
        if int(answer) == sum:
            return True
    return False
    
def init_B_insert_ABR():
    abr = generate_AB_graphe()
    leafs = []
    for node in abr.liste_noeuds:
        if not node.links:
            leafs.append(node)
    rand = randint(0, len(leafs) - 1)
    node = leafs[rand]
    node.value = "?"
    node.empty = True
    return abr, node

def check_B_insert_ABR(abr, add_data, answer):
    #answer = input("Valeur possible du noeud vide :")

    if answer.isdigit():
        abr.insert_into_abr(Noeud(int(answer)))
        if add_data.value != "?":
            return True
    return False

def init_B_dist_GRP():
    grp = generate_graphe()
    while len(grp.liste_noeuds) < 5:
        grp = generate_graphe()
    random = randint(0, len(grp.liste_noeuds) - 1)
    node = grp.liste_noeuds[random]
    node.selected_by_game = True

    random2 = randint(0, len(grp.liste_noeuds) - 1)
    while random2 == random:
        random2 = randint(0, len(grp.liste_noeuds) - 1)

    node2 = grp.liste_noeuds[random2]
    node2.selected_by_game = True
    return grp, (node, node2)

def check_B_dist_GRP(grp, add_data, _):
    selected_nodes = []
    for node in grp.liste_noeuds:
        if node.selected_by_player or node.selected_by_game:
            selected_nodes.append(node)

    # 1er noeud en point de départ et 2e en arrivé
    chemin = grp.dijkstra(add_data[0])[1][add_data[1]]
    win = same_values_between_2_lists(selected_nodes, chemin)

    # 2e noeud en point de départ et 1er en arrivé
    chemin_other = grp.dijkstra(add_data[1])[1][add_data[0]]
    win_other_way = same_values_between_2_lists(selected_nodes, chemin_other)

    return win or win_other_way


def init_U_root_ABR():
    abr = generate_AB_graphe()
    abr.racine.value = "?"
    abr.racine.empty = True
    saG, saD = abr.get_root_left_and_right()
    return abr, (saG, saD)

def check_U_root_ABR(_, add_data, answer):
    #answer = input("Valeur possible de la racine :")
    gMax = add_data[0].get_max()
    dMin = add_data[1].get_min()

    if answer.isdigit():
        if int(answer) <= dMin and int(answer) > gMax:
            return True
    return False

def init_U_cycle_GRP():
    grp = generate_graphe()
    return grp, None

def check_U_cycle_GRP(grp, _, answer):
    real_deal = grp.parcours_profondeur_cycle()
    if answer.isdigit():
        if int(answer) == real_deal:
            return True
    return False

class Graphe_Screen(Graphe):

    def render(self, screen, tileset, offsX, offsY, font):
        cmds = self.racine.parcours_largeur(func=lambda node, retval: retval + node.render_arrow_and_get_node_command(screen, tileset, offsX, offsY, font), base_retval_value=[])
        for cmd in cmds:
            screen.blit(*cmd)

class Noeud_Minijeu(Noeud):
    def __init__(self, value, links=None, x=0, y=0):
        super().__init__(value, links)
        self.selected_by_player = False
        self.selected_by_game = False
        self.empty = False
        self.x = x
        self.y = y

    def render_arrow_and_get_node_command(self, screen, tileset, offsX, offsY, font):
        node_commands = []

        tile = tileset.get_tile(0, 0)
        if self.selected_by_player:
            tile = tileset.get_tile(0, 1)
        elif self.selected_by_game:
            tile = tileset.get_tile(1, 0)
        elif self.empty:
            tile = tileset.get_tile(1, 1)

        for neighbour_dist in self.links:
            draw_arrow(screen, 0xAAAAAA, 3, 10, (self.x + 16 + offsX, self.y + 16 + offsY),
                       (neighbour_dist[0].x + 16  + offsX, neighbour_dist[0].y + 16 + offsY))

        node_commands.append((tile, (self.x + offsX, self.y + offsY)))
        node_commands.append((font.render(str(self.value), False, (0, 0, 0)), (self.x + offsX + 8, self.y + offsY + 8)))
        return node_commands
    
    def check_clicked(self, eHndl, offsX, offsY):
        click = False
        if eHndl.mouse_press:
            if not (eHndl.mouse_press_pos[0] < (self.x + offsX) or eHndl.mouse_press_pos[0] > (self.x + offsX + 32) or  eHndl.mouse_press_pos[1] < (self.y + offsY) or eHndl.mouse_press_pos[1] > (self.y + offsY + 32)):
                click = True
                self.selected_by_player = not self.selected_by_player
        return click

class Mini_Jeux:
    def __init__(self, tileset, func_init, func_check, 
                 qst="", is_tree=False):
                     
        self.is_tree = is_tree
        self.tileset = tileset
        self.graphe, self.additional_data = func_init()
        self.question = qst
        self.func_check = func_check
        self.screen_offs = [0,0]

    def set_AB_xy(self):
        height = self.graphe.get_height()
        width = 2**height
        width_center = [(SCR_X - width*32) // 2, (SCR_X + width*32) // 2]
        height_max = 50*(height+1)
        start_height = abs(SCR_Y-height_max) // 2
        self.graphe.set_abr_xy_coords(width_center, start_height)
    
    def render(self, screen, font):
        self.graphe.render(screen, self.tileset, *self.screen_offs, font)

    def handle_move_command(self, eHndl):
        MSG = "OK"
        if eHndl.pressed[K_RIGHT]:
            self.screen_offs[0] -= 4
        elif eHndl.pressed[K_LEFT]:
            self.screen_offs[0] += 4

        if eHndl.pressed[K_UP]:
            self.screen_offs[1] += 4
        elif eHndl.pressed[K_DOWN]:
            self.screen_offs[1] -= 4

        if eHndl.mouse_down:
            self.screen_offs[0] += eHndl.mouse_offs[0]
            self.screen_offs[1] += eHndl.mouse_offs[1]

        if eHndl.pressed[K_RETURN]:
            MSG = "ANSWER"
        elif eHndl.pressed[K_ESCAPE]:
            MSG = "CANCEL_ANSWER"
        return MSG

    def mini_game_loop(self, screen, clock, eHndl):
        loop = True
        win = False
        is_answering = False
        font = pygame.font.Font("RG.ttf",size=12)
        answer = ""
        if self.is_tree:
            self.set_AB_xy()
        while loop:
        
            msg_key = eHndl.update()
            for node in self.graphe.liste_noeuds:
                node.check_clicked(eHndl, *self.screen_offs)

            if msg_key == "QUIT":
                loop = False

            msg = self.handle_move_command(eHndl)
            screen.fill((0, 0, 0))
            self.render(screen, font)
            
            if is_answering:
                surf = Surface((SCR_X, SCR_Y), SRCALPHA)
                surf.fill((11, 11, 11, 200))
                screen.blit(surf, (0, 300))

                if eHndl.press_repeat.get(K_RETURN):
                    win = self.func_check(self.graphe, self.additional_data, answer)
                    loop = False
                elif eHndl.press_repeat.get(K_BACKSPACE):
                    if len(answer):
                        answer = answer[:-1]
                else:
                    for key in eHndl.press_repeat.keys():
                        answer += eHndl.press_repeat[key][1]
                txt_render = font.render(answer, False, (255, 255, 255))
                screen.blit(txt_render, (abs(txt_render.get_rect().w - SCR_X) // 2, abs(txt_render.get_rect().h - abs(300 - SCR_Y)) // 2 + 300))
                qst_render = font.render(self.question, False, (255, 255, 255))
                screen.blit(qst_render, (abs(qst_render.get_rect().w - SCR_X) // 2, 300))
                    

            if msg == "ANSWER" and not is_answering:
                is_answering = True

            elif is_answering and msg == "CANCEL_ANSWER":
                is_answering = False

            pygame.display.flip()
            clock.tick(60)
        return win

        
class ABR(Graphe_Screen):
    def get_minmax_value(self):
        min = self.get_min()
        max = self.get_max()
        return (min, max)
    
    def get_min(self):
        return self.racine.value if not self.get_root_left_and_right()[0] else self.get_root_left_and_right()[0].get_min()
    
    def get_max(self):
        return self.racine.value if not self.get_root_left_and_right()[1] else self.get_root_left_and_right()[1].get_max()

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
            arbreG.parcours_infixe()
        if arbreD:
            arbreD.parcours_infixe()

    def get_height(self):
        self.__init__(self.racine)
        arbreG, arbreD = self.get_root_left_and_right()
        valueG, valueD = -1, -1
        if arbreG:
            valueG = arbreG.get_height()  #
        if arbreD:
            valueD = arbreD.get_height()  # si ya pas de fils alors fin de recu
        return 1 + max(valueG, valueD)

    def insert_into_abr(self, noeud):
        self.__init__(self.racine)

        arbreG, arbreD = self.get_root_left_and_right()

        if self.racine.value == "?":
            self.racine.value = noeud.value

        elif noeud.value < self.racine.value:
            if arbreG:
                arbreG.insert_into_abr(noeud)
            else:
                self.racine.links.append((noeud, "gauche"))

        else:
            if arbreD:
                arbreD.insert_into_abr(noeud)
            else:
                self.racine.links.append((noeud, "droite"))

    def set_abr_xy_coords(self, width_range, height):
        x = (width_range[0] + width_range[1]) // 2

        abrG, abrD = self.get_root_left_and_right()

        if abrG:
            abrG.set_abr_xy_coords([width_range[0], x], height + 50)

        if abrD:
            abrD.set_abr_xy_coords([x, width_range[1]], height + 50)

        self.racine.x = x
        self.racine.y = height


def generate_AB_graphe(ranges=(0, 50)):
    noeud = Noeud_Minijeu((ranges[1] - ranges[0]) // 2)
    abr = ABR(noeud)
    for _ in range(randint(8, 12)):
        abr.insert_into_abr(Noeud_Minijeu(randint(*ranges)))
    return abr

def generate_graphe(ranges=(0, 50)):
    nodes = []
    for _ in range(randint(10, 15)):
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
        nodes.append(Noeud_Minijeu(randint(*ranges), x=coords[0], y=coords[1]))

    for node in nodes:
        #Scaling and centering on the base screen
        node.x *= 96
        node.x += randint(0, 48)
        node.y *= 96
        node.y += randint(0, 48) 

        node.x += (SCR_X - (5 * 96 + 48 + 32)) // 2
        node.y += (SCR_Y - (5 * 96 + 48 + 32)) // 2

    for node in nodes:
        for potential_neigh in nodes:
            if potential_neigh != node and distance2((node.x, node.y), (potential_neigh.x, potential_neigh.y)) < (148 ** 2):
                
                dist = sqrt(distance2((node.x, node.y), (potential_neigh.x, potential_neigh.y)))
                
                if not node.node_linked(potential_neigh) and len(node.links) < 3:
                    node.links.append((potential_neigh, dist))
                if not potential_neigh.node_linked(node) and len(potential_neigh.links) < 3:
                    potential_neigh.links.append((node, dist))
                    
    return Graphe_Screen(nodes[0])


MINIGAMES = {"F": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_GRP, check_F_somme_GRP, "Quelle est la somme des valeurs du noeud sélectionnée et de ses voisins ?", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_ABR, check_F_somme_ABR, "Quelle est la somme des valeurs des noeuds du sous-arbre dont la racine est sélectionnée ?", True)],
             "B": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_B_dist_GRP, check_B_dist_GRP, "Choisissez avec la souris les noeuds du chemin le plus court entre les 2 noeuds selectionnés.", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_B_insert_ABR, check_B_insert_ABR, "Que pourrait être la valeur du noeud vide ?", True)],
             "U": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_U_cycle_GRP, check_U_cycle_GRP, "Combien y a-t-il de cycle dans ce graphe ?", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_U_root_ABR, check_U_root_ABR, "Que pourrait être la valeur de la racine ?", True)]}


if __name__ == "__main__":
    import pygame
    import base

    abr = generate_AB_graphe()

    clock = pygame.time.Clock()
    fenetre = base.initialise_window("a")
    eHndl = base.EventHandler(400, 50)

    mini = MINIGAMES["U"][0]
    
    print(mini.mini_game_loop(fenetre, clock, eHndl))
