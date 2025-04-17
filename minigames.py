from graphe import Noeud, Graphe
from random import randint
from base import SCR_X, SCR_Y, draw_arrow
from pygame import K_BACKSPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, Rect, Surface, SRCALPHA
from pygame.key import stop_text_input, start_text_input, set_text_input_rect
from tile import Tileset

def init_F_somme_ABR():
    abr = generate_AB_graphe()
    random_node = randint(0, len(abr.liste_noeuds) - 1)
    abr.liste_noeuds[random_node].selected_by_game = True
    return abr, ABR(abr.liste_noeuds[random_node])

def check_F_somme_ABR(_, add_data, answer):
    #answer = input("Somme des valeurs des noeuds du sous arbre du noeud choisi :")
    real_deal = add_data.parcours_largeur()
    #print(real_deal, answer)
    if answer.isdigit():
        if int(answer) == real_deal:
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

class Graphe_Screen(Graphe):

    def render(self, screen, tileset, offsX, offsY, font):
        self.racine.parcours_largeur(func=lambda node, _: node.render(screen, tileset, offsX, offsY, font))


class Noeud_Minijeu(Noeud):
    def __init__(self, value, links=None):
        super().__init__(value, links)
        self.selected_by_player = False
        self.selected_by_game = False
        self.empty = False
        self.x = 0
        self.y = 0

    def render(self, screen, tileset, offsX, offsY, font):

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

        screen.blit(tile, (self.x + offsX, self.y + offsY))
        screen.blit(font.render(str(self.value), False, (0, 0, 0)), (self.x + offsX + 8, self.y + offsY + 8))


class Mini_Jeux:
    def __init__(self, tileset, func_init, func_check, 
                 func_additional_render=None, qst="", is_tree=False):
                     
        self.is_tree = is_tree
        self.tileset = tileset
        self.graphe, self.additional_data = func_init()
        self.question = qst
        self.func_check = func_check
        self.func_additional_render = func_additional_render
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
        self.set_AB_xy()
        while loop:
        
            msg_key = eHndl.update()

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
    for i in range(randint(8, 12)):
        abr.insert_into_abr(Noeud_Minijeu(randint(*ranges)))
    return abr



MINIGAMES = {"F": ["Somme voisin", Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_ABR, check_F_somme_ABR, qst="Quelle est la somme des valeurs des noeuds du sous-arbre dont la racine est sélectionnée ?")],
             "B": ["Chemin court", Mini_Jeux(Tileset("graphics/mini_node.png"), init_B_insert_ABR, check_B_insert_ABR, qst="Que pourrait être la valeur du noeud vide ?")],
             "U": ["Cycle", Mini_Jeux(Tileset("graphics/mini_node.png"), init_U_root_ABR, check_U_root_ABR, qst="Que pourrait être la valeur de la racine ?")]}


if __name__ == "__main__":
    import pygame
    import base

    abr = generate_AB_graphe()

    clock = pygame.time.Clock()
    fenetre = base.initialise_window("a")
    eHndl = base.EventHandler(400, 50)

    mini = MINIGAMES["B"][1]
    
    print(mini.mini_game_loop(fenetre, clock, eHndl))
