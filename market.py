try:
    import sys
    import random
    import json
    import collections
    import pygame
    from constants import *
    from utilities import *
    from ship import *
    from pool import *
    from overlay import *
    from player import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Market():
	def __init__(self, pool, player):
		self.player = player
		self.pool = pool
		self.tier = 0
		self.ships = []
		self.hold = False
		self.overlay = Overlay(self.pool)
		self.reinit()
		self.recycle_button_surf, self.recycle_button_rect = load_png('recycle.png', MARKET_ICON_SIZE)
		self.recycle_button_rect.move_ip(RECYCLE_ICON_POS)
		self.hold_button_surf, self.hold_button_rect = load_png('hold.png', MARKET_ICON_SIZE)
		self.hold_button_rect.move_ip(HOLD_ICON_POS)
		self.upgrade_tier_button_surf, self.upgrade_tier_button_rect = load_png('upgrade.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_rect.move_ip(UPGRADE_TIER_ICON_POS)
		self.reprocess_surf, self.reprocess_rect = load_png('reprocess.png', REPROCESS_SIZE)
		self.reprocess_rect.x = REPROCESS_POS[0]
		self.reprocess_rect.y = REPROCESS_POS[1]
		
	def recycle_ships(self):
		while self.ships:
			self.pool.return_ship(self.ships.pop())
		self.refill_ships()

	def toggle_hold_ships(self):
		self.hold = not self.hold

	def upgrade_tier(self):
		self.tier = min(self.tier + 1, N_TIERS - 1)

	def buy_ship(self, s):
		self.pool.remove_ship(s)
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
		
	def render(self, screen, dragging_ship, dragging_ship_offset, dragging_ship_correction, dropping_ship):
		mouse_pos = pygame.mouse.get_pos()
		ignore_s = None
		for i, s in enumerate(self.ships):
			if dropping_ship == s:
				for j, tile in enumerate(self.player.board):
					if tile.rect.collidepoint(mouse_pos):
						self.pool.ship_dict[s].rect.x = tile.rect.x
						self.pool.ship_dict[s].rect.y = tile.rect.y
						if self.player.ships[j] == None:
							self.player.ships[j] = self.buy_ship(s)
							ignore_s = s
			if s != dragging_ship and s != ignore_s:
				self.pool.ship_dict[s].rect.x = (i % N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + MARKET_OFFSET[0]
				self.pool.ship_dict[s].rect.y = (i // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) + MARKET_OFFSET[1]
				if self.pool.ship_dict[s].rect.collidepoint(mouse_pos):
					self.overlay.render(screen, s)
				screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)
			elif s != ignore_s:
				if not dragging_ship_offset:
					self.pool.ship_dict[s].rect.x = (i % N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + MARKET_OFFSET[0]
					self.pool.ship_dict[s].rect.y = (i // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) + MARKET_OFFSET[1]
				else:
					self.pool.ship_dict[s].rect.x = dragging_ship_offset[0] - dragging_ship_correction[0]
					self.pool.ship_dict[s].rect.y = dragging_ship_offset[1] - dragging_ship_correction[1]
				screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)

		screen.blit(self.recycle_button_surf, self.recycle_button_rect)
		screen.blit(self.hold_button_surf, self.hold_button_rect)
		screen.blit(self.upgrade_tier_button_surf, self.upgrade_tier_button_rect)
		screen.blit(self.reprocess_surf, self.reprocess_rect)

