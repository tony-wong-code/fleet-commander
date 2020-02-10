try:
    import sys
    import pygame

    from utilities import *
    from constants import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Commander(pygame.sprite.Sprite):
	def __init__(self, commander_info):
		super(Commander, self).__init__()

		self.name = commander_info['name']
		self.race = commander_info['race']
		self.bloodline = commander_info['bloodline']
		self.surf, self.rect = load_png(commander_info['image'], COMMANDER_SELECT_SIZE)
		self.bonus_description = commander_info['bonus']
		self.penalty_description = commander_info['penalty']
