import carte
import base
import pygame
import player
import game_state
from minigames import MINIGAMES
from random import randint
from shop import shop_mode, shop_init

MAP = carte.generate_carte()

def map_state(clock:pygame.time.Clock, screen:pygame.Surface, eHndl:base.EventHandler, player:player.Player):
    font = pygame.font.Font("RG.ttf",size=12)
    msg = "Quit"
    loop = True

    while loop:
        if eHndl.update() == "QUIT":
            loop = False
        
        if player.status == "G_O":
            loop = False
            msg = "G_O"

        for node in MAP.liste_noeuds:
            if node.check_clicked(eHndl, 0, 0):
                if node != player.current_node:
                    player.move(node, MAP)
                else:
                    loop = False
                    msg = player.get_node_type()

        if eHndl.press_repeat.get(pygame.K_RETURN):
            loop = False
            msg = player.get_node_type()

        screen.fill((0, 64, 0))
        
        screen.blit(font.render("ENDURANCE : " + str(int(player.endurance)), False, (255, 255, 255)), (0,0))
        screen.blit(font.render("MONEY : " + str(int(player.money)), False, (255, 255, 255)), (0,12))
        screen.blit(font.render("SCORE : " + str(int(player.score)), False, (255, 255, 255)), (0,24))
        MAP.render(screen, carte.TILESET, 0, 0, None, lambda node, tileset: tileset.get_tile(node.value % 2, node.value // 2))
        player.render(screen)

        pygame.display.flip()
        clock.tick(60)

    return msg

def game_over(clock:pygame.time.Clock, screen:pygame.Surface, eHndl:base.EventHandler, player:player.Player):
    font = pygame.font.Font("RG.ttf",size=64)
    msg = "Quit"
    screen.fill((0, 0, 0))
    surface = font.render("SCORE : " + str(int(player.score)), False, (255, 255, 255)) 
    screen.blit(surface, base.center_text_surface(surface, (0, 0), (base.SCR_X, base.SCR_Y)))
    pygame.display.flip()

    loop = True
    while loop:
        if eHndl.update() == "QUIT":
            loop = False

        if eHndl.press_repeat.get(pygame.K_RETURN):
            loop = False
            msg = "RESET"

        elif eHndl.press_repeat.get(pygame.K_ESCAPE):
            loop = False
    
        clock.tick(60)
    return msg



STATES = game_state.State(("MAP", map_state),
                          ("F", lambda clk, scr, eH, pl: MINIGAMES["F"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          ("B", lambda clk, scr, eH, pl: MINIGAMES["B"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          ("U", lambda clk, scr, eH, pl: MINIGAMES["U"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          ("H", shop_mode),
                          ("G_O", game_over)
                          )


def main():
    global MAP
    shop_init()
    clock = pygame.time.Clock()
    fenetre = base.initialise_window("Node Gaming")
    
    gamer = player.Player(MAP.racine)
    eHndl = base.EventHandler(400, 200)

    loop = True
    msg = "MAP"
    while loop:
        msg = STATES.get_state(msg)(clock, fenetre, eHndl, gamer)
        if msg == "Quit":
            loop = False
            pygame.quit()

        if msg == "RESET":
            MAP = carte.generate_carte()
            shop_init()
            gamer = player.Player(MAP.racine)
            msg = "MAP"

if __name__ == "__main__":
    main()