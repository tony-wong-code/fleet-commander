try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
    from engine import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

def main():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    game = Engine(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
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


        game.render()
        pygame.display.flip()
        clock.tick(30)
        game.dropping_ship = None
        game.dropping_reprocessing_ship = None

if __name__ == '__main__':
    main()