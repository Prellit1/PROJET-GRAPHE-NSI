import carte
import base
import pygame
import player
import game_state
from minigames import MINIGAMES
from random import randint

MAP = carte.generate_carte()

def map_state(clock:pygame.time.Clock, screen:pygame.Surface, eHndl:base.EventHandler, player:player.Player):
    font = pygame.font.Font("RG.ttf",size=12)
    msg = "Quit"
    loop = True

    while loop:
        if eHndl.update() == "QUIT":
            loop = False

        for node in MAP.liste_noeuds:
            if node.check_clicked(eHndl, 0, 0):
                if node != player.current_node:
                    player.move(node, MAP)
                else:
                    loop = False
                    msg = player.get_node_type()
                    # temp VVVV
                    if msg == "H":
                        msg = "F"

        if eHndl.press_repeat.get(pygame.K_RETURN):
            loop = False
            msg = player.get_node_type()
            # temp VVVV
            if msg == "H":
                msg = "F"

        screen.fill((0, 64, 0))
        
        screen.blit(font.render("ENDURANCE : " + str(int(player.endurance)), False, (255, 255, 255)), (0,0))
        screen.blit(font.render("MONEY : " + str(int(player.money)), False, (255, 255, 255)), (0,12))
        screen.blit(font.render("SCORE : " + str(int(player.score)), False, (255, 255, 255)), (0,24))
        MAP.render(screen, carte.TILESET, 0, 0, None, lambda node, tileset: tileset.get_tile(node.value % 2, node.value // 2))
        player.render(screen)

        pygame.display.flip()
        clock.tick(60)

    return msg


STATES = game_state.State(("MAP", map_state),
                          ("F", lambda clk, scr, eH, pl: MINIGAMES["F"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          ("B", lambda clk, scr, eH, pl: MINIGAMES["B"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          ("U", lambda clk, scr, eH, pl: MINIGAMES["U"][randint(0,1)].mini_game_loop(clk, scr, eH, pl)),
                          )


def main():
    clock = pygame.time.Clock()
    fenetre = base.initialise_window("Node Gaming")
    
    gamer = player.Player(MAP.racine)
    eHndl = base.EventHandler(400, 50)

    loop = True
    msg = "MAP"
    while loop:
        msg = STATES.get_state(msg)(clock, fenetre, eHndl, gamer)
        if msg == "Quit":
            loop = False
            pygame.quit()

if __name__ == "__main__":
    main()