try:
    import sys
    import pygame

    from utilities import *
    from constants import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Ship():
	def __init__(self, ship_info):
		self.name = ship_info['name']
		self.tier = ship_info['tier']
		self.surf, self.rect = load_png(self.name.lower() + '.png', SHIP_ICON_SIZE)
