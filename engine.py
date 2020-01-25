try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
    from pool import *
    from market import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Engine():
	def __init__(self, screen):
		self.screen = screen
		pygame.display.set_caption('F L E E T   C O M M A N D E R')
		self.bg_surf, self.bg_rect = load_png('background.png', RESOLUTION)

		self.pool = Pool()
		self.market = Market(self.pool)


	def render(self):
		self.screen.blit(self.bg_surf, self.bg_rect)