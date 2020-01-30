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
		self.upgrade_tier_button_surf_1, self.upgrade_tier_button_rect = load_png('upgrade_1.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_surf_2, self.upgrade_tier_button_rect = load_png('upgrade_2.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_surf_3, self.upgrade_tier_button_rect = load_png('upgrade_3.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_surf_4, self.upgrade_tier_button_rect = load_png('upgrade_4.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_surf_5, self.upgrade_tier_button_rect = load_png('upgrade_5.png', MARKET_ICON_SIZE)
		self.upgrade_tier_button_surf_6, self.upgrade_tier_button_rect = load_png('upgrade_6.png', MARKET_ICON_SIZE)
		self.upgrade_tier_surfs = [
			self.upgrade_tier_button_surf_1,
			self.upgrade_tier_button_surf_2,
			self.upgrade_tier_button_surf_3,
			self.upgrade_tier_button_surf_4,
			self.upgrade_tier_button_surf_5,
			self.upgrade_tier_button_surf_6
		]
		self.upgrade_tier_button_rect.move_ip(UPGRADE_TIER_ICON_POS)
		self.reprocess_surf, self.reprocess_rect = load_png('reprocess.png', REPROCESS_SIZE)
		self.reprocess_rect.x = REPROCESS_POS[0]
		self.reprocess_rect.y = REPROCESS_POS[1]

		self.end_turn_surf = pygame.Surface(END_TURN_SIZE)
		self.end_turn_surf.fill(END_TURN_COLOR)
		self.end_turn_surf.set_alpha(END_TURN_ALPHA)
		self.end_turn_rect = pygame.Rect(END_TURN_POS, END_TURN_SIZE)
		self.end_turn_text = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.end_turn_text_surf = self.end_turn_text.render(END_TURN_TEXT, END_TURN_FONT_ANTIALIASING, END_TURN_FONT_COLOR)
		self.end_turn_text_rect = self.end_turn_text_surf.get_rect()
		self.end_turn_text_rect.x = END_TURN_POS[0] + (self.end_turn_rect.w - self.end_turn_text_rect.w)//2
		self.end_turn_text_rect.y = END_TURN_POS[1] + (self.end_turn_rect.h - self.end_turn_text_rect.h)//2

		self.plex = STARTING_PLEX
		self.plex_on_surf, self.plex_on_rect = load_png('plex_on.png', PLEX_ICON_SIZE)
		self.plex_off_surf, self.plex_off_rect = load_png('plex_off.png', PLEX_ICON_SIZE)
		self.plex_display = []
		for i in range(MAX_PLEX):
			x = i*PLEX_ICON_SIZE[0] + PLEX_POS[0]
			y = PLEX_POS[1]
			self.plex_display.append(pygame.Rect((x, y), PLEX_ICON_SIZE))
		self.plex_text = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.plex_text_surf = self.plex_text.render(str(self.plex) + '/' + str(MAX_PLEX), PLEX_FONT_ANTIALIASING, PLEX_FONT_COLOR)
		self.plex_text_rect = self.plex_text_surf.get_rect()
		self.plex_text_rect.x = PLEX_TEXT_POS[0]
		self.plex_text_rect.y = PLEX_TEXT_POS[1]
		self.upgrade_plex_rect = pygame.Rect(UPGRADE_TIER_PLEX_ICON_POS, PLEX_ICON_SIZE)
		self.recycle_plex_rect = pygame.Rect(RECYCLE_PLEX_ICON_POS, PLEX_ICON_SIZE)
		self.current_upgrade_cost = UPGRADE_COST[0]
		self.upgrade_plex_text = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.upgrade_plex_text_surf = self.upgrade_plex_text.render(str(self.current_upgrade_cost), PLEX_FONT_ANTIALIASING, PLEX_FONT_COLOR)
		self.upgrade_plex_text_rect = self.upgrade_plex_text_surf.get_rect()
		self.upgrade_plex_text_rect.x = UPGRADE_TIER_PLEX_ICON_POS[0] + MISC_PLEX_TEXT_PADDING[0]
		self.upgrade_plex_text_rect.y = UPGRADE_TIER_PLEX_ICON_POS[1] + MISC_PLEX_TEXT_PADDING[1]
		self.recycle_plex_text = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.recycle_plex_text_surf = self.recycle_plex_text.render(str(RECYCLE_COST), PLEX_FONT_ANTIALIASING, PLEX_FONT_COLOR)
		self.recycle_plex_text_rect = self.recycle_plex_text_surf.get_rect()
		self.recycle_plex_text_rect.x = RECYCLE_PLEX_ICON_POS[0] + MISC_PLEX_TEXT_PADDING[0]
		self.recycle_plex_text_rect.y = RECYCLE_PLEX_ICON_POS[1] + MISC_PLEX_TEXT_PADDING[1]
		
	def recycle_ships(self):
		while self.ships:
			self.pool.return_ship(self.ships.pop())
		self.refill_ships()

	def toggle_hold_ships(self):
		self.hold = not self.hold

	def upgrade_tier(self):
		self.tier = min(self.tier + 1, N_TIERS - 1)

	def buy_ship(self, s):
		self.plex = max(self.plex - SHIP_COST, 0)
		self.pool.remove_ship(s)
		self.ships.remove(s)
		return s

	def sell_ship(self, s):
		self.plex = min(self.plex + SHIP_REPROCESS, 10)
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
				if self.hold:
					screen.blit(self.hold_button_surf, self.pool.ship_dict[s].rect)
			elif s != ignore_s:
				if not dragging_ship_offset:
					self.pool.ship_dict[s].rect.x = (i % N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + MARKET_OFFSET[0]
					self.pool.ship_dict[s].rect.y = (i // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) + MARKET_OFFSET[1]
				else:
					self.pool.ship_dict[s].rect.x = dragging_ship_offset[0] - dragging_ship_correction[0]
					self.pool.ship_dict[s].rect.y = dragging_ship_offset[1] - dragging_ship_correction[1]
				screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)


		screen.blit(self.recycle_button_surf, self.recycle_button_rect)
		tmp_surf = None
		if self.plex >= RECYCLE_COST:
			tmp_surf = self.plex_on_surf
		else:
			tmp_surf = self.plex_off_surf
		screen.blit(tmp_surf, self.recycle_plex_rect)
		screen.blit(self.hold_button_surf, self.hold_button_rect)
		screen.blit(self.upgrade_tier_surfs[self.tier], self.upgrade_tier_button_rect)
		if self.plex >= self.current_upgrade_cost:
			tmp_surf = self.plex_on_surf
		else:
			tmp_surf = self.plex_off_surf
		screen.blit(tmp_surf, self.upgrade_plex_rect)
		screen.blit(self.reprocess_surf, self.reprocess_rect)
		screen.blit(self.end_turn_surf, self.end_turn_rect)
		screen.blit(self.end_turn_text_surf, self.end_turn_text_rect)
		for i in range(MAX_PLEX):
			if i < self.plex:
				surf = self.plex_on_surf
			else:
				surf = self.plex_off_surf
			screen.blit(surf, self.plex_display[i])

		self.plex_text_surf = self.plex_text.render(str(self.plex) + '/' + str(MAX_PLEX), PLEX_FONT_ANTIALIASING, PLEX_FONT_COLOR)
		self.plex_text_rect = self.plex_text_surf.get_rect()
		self.plex_text_rect.x = PLEX_TEXT_POS[0]
		self.plex_text_rect.y = PLEX_TEXT_POS[1]
		screen.blit(self.plex_text_surf, self.plex_text_rect)

		screen.blit(self.upgrade_plex_text_surf, self.upgrade_plex_text_rect)
		screen.blit(self.recycle_plex_text_surf, self.recycle_plex_text_rect)

