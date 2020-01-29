try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
    from pool import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Tile():
	def __init__(self, pos):
		self.surf, self.rect = load_png('battle_tile.png', TILE_SIZE)
		self.rect.x = pos[0]
		self.rect.y = pos[1]

class Player():
	def __init__(self, who, pool):
		self.who = who
		self.pool = pool
		self.board = [None for _ in range(N_SHIPS_PER_PLAYER)]
		for i in range(N_SHIPS_PER_PLAYER):
			x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
			y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
			self.board[i] = Tile((x, y))
		self.station_health = STATION_HEALTH
		self.ships = [None for _ in range(N_SHIPS_PER_PLAYER)]

	def render(self, screen, market, dragging_reprocessing_ship, dragging_reprocessing_ship_offset, dragging_reprocessing_ship_correction, dropping_reprocessing_ship):
		mouse_pos = pygame.mouse.get_pos()
		ignore_s = None
		reprocessing_rect = pygame.Rect(REPROCESS_POS, REPROCESS_SIZE)
		for i, s in enumerate(self.ships):
			screen.blit(self.board[i].surf, self.board[i].rect)
			if not s:
				continue
			if dropping_reprocessing_ship == s:
				if reprocessing_rect.collidepoint(mouse_pos):
					market.sell_ship(s)
					self.ships[i] = None
					ignore_s = s
				else:
					self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
					self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
			if s != dragging_reprocessing_ship and s != ignore_s:
				screen.blit(self.pool.ship_dict[self.ships[i]].surf, self.pool.ship_dict[self.ships[i]].rect)
			elif s != ignore_s:
				if not dragging_reprocessing_ship_offset:
					self.pool.ship_dict[s].rect.x = BOARD_OFFSET[0] + (i % BOARD_SIZE[0])*(TILE_SIZE[0] + TILE_PADDING[0])
					self.pool.ship_dict[s].rect.y = BOARD_OFFSET[1] + (i // BOARD_SIZE[0])*(TILE_SIZE[1] + TILE_PADDING[1])
				else:
					self.pool.ship_dict[s].rect.x = dragging_reprocessing_ship_offset[0] - dragging_reprocessing_ship_correction[0]
					self.pool.ship_dict[s].rect.y = dragging_reprocessing_ship_offset[1] - dragging_reprocessing_ship_correction[1]
				screen.blit(self.pool.ship_dict[s].surf, self.pool.ship_dict[s].rect)