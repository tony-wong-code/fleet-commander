try:
    import sys
    import math
    import pygame
    from pygame.locals import *
    import pygame.gfxdraw

    from copy import copy
    from constants import *
    from utilities import *
    from pool import *
    from market import *
    from player import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Engine():
	def __init__(self, screen):
		self.screen = screen
		pygame.display.set_caption('F L E E T   C O M M A N D E R')
		self.bg_surf, self.bg_rect = load_png('background.png', RESOLUTION)

		self.pool = Pool()
		self.player = Player(HUMAN, self.pool)
		self.market = Market(self.pool, self.player)
		self.market.reinit()
		self.market_phase = True
		self.dragging_ship = None
		self.dragging_ship_offset = None
		self.dragging_rect_correction = [0, 0]
		self.dropping_ship = None

		self.dragging_reprocessing_ship = None
		self.dragging_reprocessing_ship_offset = None
		self.dragging_reprocessing_rect_correction = [0, 0]
		self.dropping_reprocessing_ship = None

		self.turn = 1
		
	def render(self, clock):
		self.screen.blit(self.bg_surf, self.bg_rect)
		if self.market_phase:
			self.market.render(self.screen, self.dragging_ship, self.dragging_ship_offset, self.dragging_rect_correction, self.dropping_ship)
			self.player.render(self.screen, self.market, self.dragging_reprocessing_ship, self.dragging_reprocessing_ship_offset, self.dragging_reprocessing_rect_correction, self.dropping_reprocessing_ship)
		else:
			self.battle(self.player, self.player)
	def update(self, mouse_pos):
		if self.market_phase:
			if self.market.recycle_button_rect.collidepoint(mouse_pos) and self.market.plex >= RECYCLE_COST:
				self.market.plex = max(self.market.plex - RECYCLE_COST, 0)
				self.market.recycle_ships()
			elif self.market.upgrade_tier_button_rect.collidepoint(mouse_pos) and self.market.plex >= self.market.current_upgrade_cost and self.market.tier != N_TIERS - 1:
				self.market.plex = max(self.market.plex - self.market.current_upgrade_cost, 0)
				self.market.upgrade_tier()
			elif self.market.end_turn_rect.collidepoint(mouse_pos):
				self.market_phase = False
			elif self.market.hold_button_rect.collidepoint(mouse_pos):
				self.market.toggle_hold_ships()
			else:
				if self.market.plex >= SHIP_COST:
					for i, s in enumerate(self.market.ships):
						rect = pygame.Rect(
							(
								(i % N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + MARKET_OFFSET[0],
								(i // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) + MARKET_OFFSET[1]
							),
							(SHIP_ICON_SIZE)
						)
						
						if rect.collidepoint(mouse_pos):
							self.dragging_ship = s
							self.dragging_rect_correction[0] = mouse_pos[0] - rect.x
							self.dragging_rect_correction[1] = mouse_pos[1] - rect.y

				for i, s in enumerate(self.player.ships):
					rect = pygame.Rect(
						(
							BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
							BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						),
						(TILE_SIZE)
					)

					if rect.collidepoint(mouse_pos):
						self.dragging_reprocessing_ship = s
						self.dragging_reprocessing_rect_correction[0] = mouse_pos[0] - rect.x
						self.dragging_reprocessing_rect_correction[1] = mouse_pos[1] - rect.y
		else:
			self.battle(self.player, self.player)

	def ships_remaining(self, ships):
		return len([s for s in ships if s])

	
	def draw_ship_status(self, s, pos_center):
		
		status_color = RED
		start_angle = START_ANGLE
		end_angle = END_ANGLE
		
		x, y = pos_center

		pygame.draw.circle(self.screen, BLACK, pos_center, STATUS_SHIELDS_RADIUS)
		for i in range(STATUS_INTERVALS):
			if s.shields == 0:
				status_color = RED
			elif (s.remaining_shields / s.shields) <= (i / STATUS_INTERVALS):
				status_color = RED
			else:
				status_color = WHITE
			
			x1 = x + int(STATUS_SHIELDS_RADIUS * math.cos(start_angle * math.pi / 180))
			y1 = y + int(STATUS_SHIELDS_RADIUS * math.sin(start_angle * math.pi / 180))
			x2 = x + int(STATUS_SHIELDS_RADIUS * math.cos((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			y2 = y + int(STATUS_SHIELDS_RADIUS * math.sin((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			pygame.gfxdraw.aatrigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			pygame.gfxdraw.filled_trigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			start_angle += EACH_ANGLE

		start_angle = START_ANGLE
		pygame.draw.circle(self.screen, BLACK, pos_center, STATUS_ARMOR_RADIUS)
		for i in range(STATUS_INTERVALS):
			if s.armor == 0:
				status_color = RED
			elif (s.remaining_armor / s.armor) <= (i / STATUS_INTERVALS):
				status_color = RED
			else:
				status_color = WHITE
			
			x1 = x + int(STATUS_ARMOR_RADIUS * math.cos(start_angle * math.pi / 180))
			y1 = y + int(STATUS_ARMOR_RADIUS * math.sin(start_angle * math.pi / 180))
			x2 = x + int(STATUS_ARMOR_RADIUS * math.cos((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			y2 = y + int(STATUS_ARMOR_RADIUS * math.sin((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			pygame.gfxdraw.aatrigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			pygame.gfxdraw.filled_trigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			start_angle += EACH_ANGLE

		start_angle = START_ANGLE
		pygame.draw.circle(self.screen, BLACK, pos_center, STATUS_HULL_RADIUS)
		for i in range(STATUS_INTERVALS):
			if s.hull == 0:
				status_color = RED
			elif (s.remaining_hull / s.hull) <= (i / STATUS_INTERVALS):
				status_color = RED
			else:
				status_color = WHITE
			
			x1 = x + int(STATUS_HULL_RADIUS * math.cos(start_angle * math.pi / 180))
			y1 = y + int(STATUS_HULL_RADIUS * math.sin(start_angle * math.pi / 180))
			x2 = x + int(STATUS_HULL_RADIUS * math.cos((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			y2 = y + int(STATUS_HULL_RADIUS * math.sin((start_angle + EACH_ANGLE - THICKNESS_BETWEEN_ANGLES) * math.pi / 180))
			pygame.gfxdraw.aatrigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			pygame.gfxdraw.filled_trigon(self.screen, x, y, x1, y1, x2, y2, status_color)
			start_angle += EACH_ANGLE
		pygame.draw.circle(self.screen, BLACK, pos_center, 50)


	def battle(self, p1, p2):
		p1_board = [None for _ in range(N_SHIPS_PER_PLAYER)]
		p1_ships = [None for _ in range(N_SHIPS_PER_PLAYER)]
		for i, s in enumerate(p1.ships):
			if s != None:
				p1_ships[i] = copy(self.pool.ship_dict[s])
				p1_ships[i].surf, p1_ships[i].rect = load_png(p1_ships[i].name.lower() + '.png', SHIP_ICON_SIZE)
		p1_board_tiles = pygame.sprite.Group()
		for i in range(N_SHIPS_PER_PLAYER):
			x = BATTLE_BOARD_OFFSET_P1[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + BATTLE_TILE_PADDING[0])
			y = BATTLE_BOARD_OFFSET_P1[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + BATTLE_TILE_PADDING[1])
			p1_board[i] = Tile('battle_tile.png', (x, y), i)
			p1_board_tiles.add(p1_board[i])
			if p1_ships[i] != None:
				p1_ships[i].rect.x = x
				p1_ships[i].rect.y = y
		
		p2_board = [None for _ in range(N_SHIPS_PER_PLAYER)]
		p2_ships = [None for _ in range(N_SHIPS_PER_PLAYER)]
		for i, s in enumerate(p2.ships):
			if s != None:
				p2_ships[i] = copy(self.pool.ship_dict[s])
				p2_ships[i].surf, p2_ships[i].rect = load_png(p2_ships[i].name.lower() + '.png', SHIP_ICON_SIZE)
		p2_board_tiles = pygame.sprite.Group()
		for i in range(N_SHIPS_PER_PLAYER):
			x = BATTLE_BOARD_OFFSET_P2[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + BATTLE_TILE_PADDING[0])
			y = BATTLE_BOARD_OFFSET_P2[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + BATTLE_TILE_PADDING[1])
			p2_board[i] = Tile('battle_tile_2.png', (x, y), i)
			p2_board_tiles.add(p2_board[i])
			if p2_ships[i] != None:
				p2_ships[i].rect.x = x
				p2_ships[i].rect.y = y

		while self.ships_remaining(p1_ships) != 0 and self.ships_remaining(p2_ships) != 0:
			for t in p1_board_tiles:
				self.screen.blit(t.surf, t.rect)
			for s in p1_ships:
				if s != None:
					self.draw_ship_status(s, s.rect.center)
					self.screen.blit(s.surf, s.rect)
			for t in p2_board_tiles:
				self.screen.blit(t.surf, t.rect)
			for s in p2_ships:
				if s != None:
					self.draw_ship_status(s, s.rect.center)
					self.screen.blit(s.surf, s.rect)
			pygame.display.flip()
			pygame.time.delay(10000)
			sys.exit(2)