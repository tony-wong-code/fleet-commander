try:
    import sys
    import pygame

    from utilities import *
    from constants import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Ship(pygame.sprite.Sprite):
	def __init__(self, ship_info):
		super(Ship, self).__init__()
		self.name = ship_info['name']
		self.tier = ship_info['tier']
		self.ship_class = ship_info['ship_class']
		self.attack = ship_info['attack']
		self.race = ship_info['race']
		self.shields = ship_info['shields']
		self.armor = ship_info['armor']
		self.hull = ship_info['hull']
		self.surf, self.rect = load_png(self.name.lower() + '.png', SHIP_ICON_SIZE)
		self.remaining_shields = self.shields
		self.remaining_armor = self.armor
		self.remaining_hull = self.hull
