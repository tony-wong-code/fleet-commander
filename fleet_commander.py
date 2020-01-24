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

        game.render()
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()