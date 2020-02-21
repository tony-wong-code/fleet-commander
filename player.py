try:
    import sys
    import pygame
    from pygame.locals import *
    import random

    from constants import *
    from utilities import *
    from pool import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Player():
	def __init__(self, who, pool, surf=None, rect=None):
		self.who = who
		self.surf = surf
		self.rect = rect
		self.pool = pool
		self.station_health = STATION_HEALTH
		self.ships = [None for _ in range(N_SHIPS_PER_PLAYER)]
		self.tier = 0
		self.ships_in_market = []
		self.hold_ships = False
		self.upgrade_cost = UPGRADE_COST[self.tier]
		self.plex = STARTING_PLEX
		self.salvaging = False
		self.is_alive = True
