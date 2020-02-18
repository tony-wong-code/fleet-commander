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

class Tile(pygame.sprite.Sprite):
	def __init__(self, name, pos, i):
		super(Tile, self).__init__()
		self.surf, self.rect = load_png(name, TILE_SIZE)
		self.rect.center = pos
		self.i = i
		self.order_text = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.order_text_surf = self.order_text.render(str(i), ORDER_TEXT_FONT_ANTIALIASING, ORDER_TEXT_FONT_COLOR)
		self.order_text_rect = self.order_text_surf.get_rect()
		self.order_text_rect.center = self.rect.center

class Player():
	def __init__(self, who, pool, surf=None, rect=None):
		self.who = who
		self.surf = surf
		self.rect = rect
		self.pool = pool
		self.board = [None for _ in range(N_SHIPS_PER_PLAYER)]
		self.board_tiles = pygame.sprite.Group()
		for i in range(N_SHIPS_PER_PLAYER):
			x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
			y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
			self.board[i] = Tile('battle_tile.png', (x, y), i)
			self.board_tiles.add(self.board[i])
		self.station_health = STATION_HEALTH
		self.ships = [None for _ in range(N_SHIPS_PER_PLAYER)]
		self.tier = 0
		self.ships_in_market = []
		self.hold_ships = False

	def print_ships(self):
		print(self.ships)

	def render(self, screen, market, dragging_reprocessing_ship, dragging_reprocessing_ship_offset, dragging_reprocessing_ship_correction, dropping_reprocessing_ship):
		mouse_pos = pygame.mouse.get_pos()
		ignore_s = set()
		reprocessing_rect = pygame.Rect(REPROCESS_POS, REPROCESS_SIZE)
		for i, s in enumerate(self.ships):
			screen.blit(self.board[i].surf, self.board[i].rect)
			if s == None:
				screen.blit(self.board[i].order_text_surf, self.board[i].order_text_rect)
				continue
			if dropping_reprocessing_ship == s:
				if reprocessing_rect.collidepoint(mouse_pos):
					market.sell_ship(s)
					self.ships[i] = None
					ignore_s.add(s)
				elif pygame.sprite.spritecollideany(self.pool.ship_dict[s], self.board_tiles):
					tile_index = (pygame.sprite.spritecollide(self.pool.ship_dict[s], self.board_tiles, False)[0]).i
					# dragging a player ship to a valid empty board tile
					if self.ships[tile_index] == None:
						self.ships[tile_index] = s
						self.ships[i] = None
						#self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (tile_index % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
						#self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (tile_index // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						self.pool.ship_dict[s].rect.center = (
							BOARD_OFFSET[0] + (tile_index % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
							BOARD_OFFSET[1] + (tile_index // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						)
						ignore_s.add(s)
					# dragging a player ship onto another player ship
					else:
						s2 = self.ships[tile_index]
						ignore_s.add(s)
						ignore_s.add(s2)
						self.ships[tile_index], self.ships[i] = self.ships[i], self.ships[tile_index]
						#self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (tile_index % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
						#self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (tile_index // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						self.pool.ship_dict[s].rect.center = (
							BOARD_OFFSET[0] + (tile_index % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
							BOARD_OFFSET[1] + (tile_index // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						)
						#self.pool.ship_dict[s2].rect.x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
						#self.pool.ship_dict[s2].rect.y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						self.pool.ship_dict[s2].rect.center = (
							BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
							BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
						)
				else:
					#self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
					#self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
					self.pool.ship_dict[s].rect.center = (
						BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
						BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
					)
			if s != dragging_reprocessing_ship and s not in ignore_s:
				screen.blit(self.pool.ship_dict[self.ships[i]].surf, self.pool.ship_dict[self.ships[i]].rect)
			elif s not in ignore_s:
				if not dragging_reprocessing_ship_offset:
					#self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
					#self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
					self.pool.ship_dict[s].rect.center = (
						BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0]),
						BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
					)
				else:
					#self.pool.ship_dict[s].rect.x = dragging_reprocessing_ship_offset[0] - dragging_reprocessing_ship_correction[0]
					#self.pool.ship_dict[s].rect.y = dragging_reprocessing_ship_offset[1] - dragging_reprocessing_ship_correction[1]
					self.pool.ship_dict[s].rect.center = (
						dragging_reprocessing_ship_offset[0] - dragging_reprocessing_ship_correction[0],
						dragging_reprocessing_ship_offset[1] - dragging_reprocessing_ship_correction[1]
					)
				screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)