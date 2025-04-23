from graphe import Noeud
from graphe_graphics import Noeud_Screen, Graphe_Screen
from random import randint
from base import SCR_X, SCR_Y, same_values_between_2_lists
from pygame import K_BACKSPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, Surface, SRCALPHA, display
from pygame.font import Font
from carte import generate_graphe
from tile import Tileset

FONTSIZE = 12

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
    grp = generate_graphe_minijeu()
    #print(grp.liste_noeuds)
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
    grp = generate_graphe_minijeu()
    while len(grp.liste_noeuds) < 5:
        grp = generate_graphe_minijeu()
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
    chemin = grp.dijkstra(add_data[0])[1].get(add_data[1])
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
    grp = generate_graphe_minijeu()
    return grp, None

def check_U_cycle_GRP(grp, _, answer):
    real_deal = grp.parcours_profondeur_cycle()
    if answer.isdigit():
        if int(answer) == real_deal:
            return True
    return False

class Noeud_Minijeu(Noeud_Screen):
    def __init__(self, value, links=None, x=0, y=0):
        super().__init__(value, links, x, y)
        self.selected_by_player = False
        self.selected_by_game = False
        self.empty = False

class Mini_Jeux:
    def __init__(self, tileset, func_init, func_check, 
                 qst="", is_tree=False):
                     
        self.is_tree = is_tree
        self.tileset = tileset
        self.question = qst
        self.func_init = func_init
        self.func_check = func_check
        self.screen_offs = [0,0]

    def set_AB_xy(self):
        """
        ENTREE  : l'objet
        SORTIE  : ---
        ROLE    : definis les coordonnées des noeuds composant l'arbre du minijeux 
        Version : 2025APR_01 
        """
        height = self.graphe.get_height()
        width = 2**height
        width_center = [(SCR_X - width*32) // 2, (SCR_X + width*32) // 2]
        height_max = 50*(height+1)
        start_height = abs(SCR_Y-height_max) // 2
        self.graphe.set_abr_xy_coords(width_center, start_height)
    
    def render(self, screen, font):
        self.graphe.render(screen, self.tileset, *self.screen_offs, font, lambda node, tileset: tileset.get_tile(1, 1) if node.empty else tileset.get_tile(0, 1) if node.selected_by_player else tileset.get_tile(1,0) if node.selected_by_game else tileset.get_tile(0,0) ) 

    def handle_move_command(self, eHndl):
        """
        ENTREE  : l'objet, gestionnaire d'evenement
        SORTIE  : une chaine de caractere
        ROLE    : modifie des attributs et renvoie un message en fonction des evenements clavier et souris
        Version : 2025APR_01 
        """
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

    def mini_game_loop(self, clock, screen, eHndl, player):
        msg = "Quit"
        self.graphe, self.additional_data = self.func_init()
        self.screen_offs = [0, 0]
        loop = True
        win = False
        is_answering = False
        font = Font("RG.ttf",size=FONTSIZE)
        answer = ""
        if self.is_tree:
            self.set_AB_xy()

        while loop:
            msg_key = eHndl.update()
            for node in self.graphe.liste_noeuds:
                if node.check_clicked(eHndl, *self.screen_offs):
                    node.selected_by_player = not node.selected_by_player

            if msg_key == "QUIT":
                loop = False

            msg_ans = self.handle_move_command(eHndl)
            screen.fill((0, 0, 0))
            self.render(screen, font)
            screen.blit(font.render("Taille : "+ str(self.graphe.taille()), False, (255, 255, 255)), (0, 0))
            if self.is_tree:
                screen.blit(font.render("Hauteur : "+ str(self.graphe.get_height()), False, (255, 255, 255)), (0, FONTSIZE))
            
            if is_answering:
                surf = Surface((SCR_X, SCR_Y), SRCALPHA)
                surf.fill((11, 11, 11, 200))
                screen.blit(surf, (0, 300))

                if eHndl.press_repeat.get(K_RETURN):
                    win = self.func_check(self.graphe, self.additional_data, answer)
                    msg = "MAP"
                    loop = False
                    
                elif eHndl.press_repeat.get(K_BACKSPACE):
                    if len(answer):
                        answer = answer[:-1]
                else:
                    for key in eHndl.press_repeat.keys():
                        if key != K_ESCAPE:
                            answer += eHndl.press_repeat[key][1]
                txt_render = font.render(answer, False, (255, 255, 255))
                screen.blit(txt_render, (abs(txt_render.get_rect().w - SCR_X) // 2, abs(txt_render.get_rect().h - abs(300 - SCR_Y)) // 2 + 300))
                qst_render = font.render(self.question, False, (255, 255, 255))
                screen.blit(qst_render, (abs(qst_render.get_rect().w - SCR_X) // 2, 300))
                    

            if msg_ans == "ANSWER" and not is_answering:
                is_answering = True

            elif is_answering and msg_ans == "CANCEL_ANSWER":
                is_answering = False

            display.flip()
            clock.tick(60)
        if win:
            player.get_pay()
        return msg

        
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

    def get_height(self):
        """
        ENTREE  : L'objet
        SORTIE  : une valeur
        ROLE    : renvoie la hauteur de l'arbre
        Version : 2025APR_01 
        """
        self.__init__(self.racine)
        arbreG, arbreD = self.get_root_left_and_right()
        valueG, valueD = -1, -1
        if arbreG:
            valueG = arbreG.get_height()  #
        if arbreD:
            valueD = arbreD.get_height()  # si ya pas de fils alors fin de recu
        return 1 + max(valueG, valueD)

    def insert_into_abr(self, noeud):
        """
        ENTREE  : L'objet, un noeud
        SORTIE  : ---
        ROLE    : insere un noeud dans l'ABR en fonction de sa valeur
        Version : 2025APR_01 
        """

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

        self.__init__(self.racine) # reinitialise l'arbre

    def set_abr_xy_coords(self, width_range, height):
        """
        ENTREE  : L'objet, un tuple, une hauteur
        SORTIE  : ---
        ROLE    : détermine les coordonnées des noeuds de l'arbre en fonction d'un interval horizontal et de la hauteur
        Version : 2025APR_01 
        """
        x = (width_range[0] + width_range[1]) // 2

        abrG, abrD = self.get_root_left_and_right()

        if abrG:
            abrG.set_abr_xy_coords([width_range[0], x], height + 50)

        if abrD:
            abrD.set_abr_xy_coords([x, width_range[1]], height + 50)

        self.racine.x = x
        self.racine.y = height

    def parcours_infixe(self, func = lambda node, retval: retval + [node], base_return_val = []):
        """
        ENTREE  : L'objet, une fonction forme (Noeud, valeur retourné), une valeur
        SORTIE  : une valeur
        ROLE    : Pratique un parcours infixe en appliquant une fonction sur des noeuds et en retournant le resultat de cette fonction
        Version : 2025APR_01 
        """
        abrG, abrD = self.get_root_left_and_right()
        retval = base_return_val
        if abrG:
            retval = abrG.parcours_infixe(func, retval)
        
        retval = func(self.racine, retval)

        if abrD:
            retval = abrD.parcours_infixe(func, retval)
        
        return retval


def generate_AB_graphe(ranges=(0, 50)):
    """
    ENTREE  : un tuple
    SORTIE  : un ABR
    ROLE    : renvoie un abre de 8 a 10 noeuds avec des valeur entre les valeurs du tuple
    Version : 2025APR_01 
    """
    noeud = Noeud_Minijeu((ranges[1] - ranges[0]) // 2)
    abr = ABR(noeud)
    for _ in range(randint(8, 12)):
        abr.insert_into_abr(Noeud_Minijeu(randint(*ranges)))

    print(abr.parcours_infixe())
    return abr

def generate_graphe_minijeu(ranges=(0, 50)):
    """
    ENTREE  : un tuple
    SORTIE  : un graphe_écran
    ROLE    : crée un graphe affichable avec des noeuds contenant des valeurs entre celles du tuple
    Version : 2025APR_01 
    """
    graphe = generate_graphe(Noeud_Minijeu, max_link_dist=148)
    for node in graphe.liste_noeuds:
        node.value = randint(*ranges)
    return graphe


MINIGAMES = {"F": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_GRP, check_F_somme_GRP, "Quelle est la somme des valeurs du noeud sélectionnée et de ses voisins ?", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_F_somme_ABR, check_F_somme_ABR, "Quelle est la somme des valeurs des noeuds du sous-arbre dont la racine est sélectionnée ?", True)],
             "B": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_B_dist_GRP, check_B_dist_GRP, "Choisissez avec la souris les noeuds du chemin le plus court entre les 2 noeuds selectionnés.", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_B_insert_ABR, check_B_insert_ABR, "Que pourrait être la valeur du noeud vide ?", True)],
             "U": [Mini_Jeux(Tileset("graphics/mini_node.png"), init_U_cycle_GRP, check_U_cycle_GRP, "Combien y a-t-il de cycle dans ce graphe ?", False), Mini_Jeux(Tileset("graphics/mini_node.png"), init_U_root_ABR, check_U_root_ABR, "Que pourrait être la valeur de la racine ?", True)]}
