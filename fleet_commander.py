try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
    from engine import *
    from menu import *
    from game import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

def main():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()
    
    game_state = MENU
    menu = Menu(screen, clock)
    #game = Engine(screen)
    game = Game(screen, clock)
    pygame.display.set_caption('Fleet Commander')
    while True:
        while game_state == MENU:
            game_state = menu.render()

        while game_state == GAME:
            game_state = game.render()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

                ### START OF DEBUG
                if event.key == K_t:
                    game.player.print_ships()
                if event.key == K_p:
                    game.market.plex = 10
                ### END OF DEBUG 

            elif event.type == QUIT: 
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.update(pygame.mouse.get_pos())
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if game.dragging_ship != None:
                        game.dropping_ship = game.dragging_ship
                    game.dragging_ship = None
                    game.dragging_ship_offset = None
                    game.dragging_rect_correction = [0, 0]

                    if game.dragging_reprocessing_ship != None:
                        game.dropping_reprocessing_ship = game.dragging_reprocessing_ship
                    game.dragging_reprocessing_ship = None
                    game.dragging_reprocessing_ship_offset = None
                    game.dragging_reprocessing_rect_correction = [0, 0]
            elif event.type == MOUSEMOTION:
                if game.dragging_ship != None:
                    game.dragging_ship_offset = event.pos
                if game.dragging_reprocessing_ship != None:
                    game.dragging_reprocessing_ship_offset = event.pos


        game.render(clock)
        pygame.display.flip()
        clock.tick(30)
        game.dropping_ship = None
        game.dropping_reprocessing_ship = None

if __name__ == '__main__':
    main()