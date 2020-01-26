try:
    import sys
    import random
    import json
    import collections
    import pygame
    from constants import *
    from ship import *
    from pool import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Market():
	def __init__(self, pool):
		self.pool = pool
		self.tier = 0
		self.ships = []
		self.hold = False
		self.reinit()
		self.recycle_button_surf, self.recycle_button_rect = load_png('recycle.png', MARKET_ICON_SIZE)
		self.recycle_button_rect.move_ip(RECYCLE_ICON_POS)
		self.hold_button_surf, self.hold_button_rect = load_png('hold.png', MARKET_ICON_SIZE)
		self.hold_button_rect.move_ip(HOLD_ICON_POS)
		self.upgrade_tier_button_surf, self.upgrade_tier_button_rect = load_png('upgrade.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_rect.move_ip(UPGRADE_TIER_ICON_POS)
	def recycle_ships(self):
		while self.ships:
			self.pool.return_ship(self.ships.pop())
		self.refill_ships()

	def toggle_hold_ships(self):
		self.hold = not self.hold

	def upgrade_tier(self):
		self.tier = min(self.tier + 1, N_TIERS - 1)

	def buy_ship(self, s):
		self.ships.remove(s)
		return s

	def sell_ship(self, s):
		self.pool.return_ship(s)

	def refill_ships(self):
		while len(self.ships) < N_MARKET_SHIPS_PER_TIER[self.tier]:
			self.ships.append(self.pool.get_ship(self.tier))

	def reinit(self):
		if not self.hold:
			self.recycle_ships()
		else:
			self.refill_ships()
		self.hold = False

	def render(self, screen):
		for i, s in enumerate(self.ships):
			self.pool.ship_dict[s].rect.x = (i % N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + MARKET_OFFSET[0]
			self.pool.ship_dict[s].rect.y = (i // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) + MARKET_OFFSET[1]
			screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)
		screen.blit(self.recycle_button_surf, self.recycle_button_rect)
		screen.blit(self.hold_button_surf, self.hold_button_rect)
		screen.blit(self.upgrade_tier_button_surf, self.upgrade_tier_button_rect)

