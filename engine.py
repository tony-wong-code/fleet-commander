try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
    from pool import *
    from market import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Engine():
	def __init__(self, screen):
		self.screen = screen
		pygame.display.set_caption('F L E E T   C O M M A N D E R')
		self.bg_surf, self.bg_rect = load_png('background.png', RESOLUTION)

		self.pool = Pool()
		self.market = Market(self.pool)
		self.market.reinit()
		self.market_phase = True
		self.dragging_ship = None
		self.dragging_ship_offset = None
		self.dragging_rect_correction = [0, 0]
	def render(self):
		self.screen.blit(self.bg_surf, self.bg_rect)
		if self.market_phase:
			self.market.render(self.screen, self.dragging_ship, self.dragging_ship_offset, self.dragging_rect_correction)
	def update(self, mouse_pos):
		if self.market_phase:
			if self.market.recycle_button_rect.collidepoint(mouse_pos):
				self.market.recycle_ships()
			elif self.market.upgrade_tier_button_rect.collidepoint(mouse_pos):
				self.market.upgrade_tier()
			else:
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


		

