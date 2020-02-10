try:
    import sys
    import pygame
    from pygame.locals import *

    from constants import *
    from utilities import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Menu():
	def __init__(self, screen, clock):
		self.screen = screen
		self.clock = clock
		self.surf, self.rect = load_png('menu.png', RESOLUTION)
		self.title_text = pygame.font.Font(FONT, TITLE_FONT_SIZE)
		self.title_text_surf = self.title_text.render('FLEET COMMANDER', AA, WHITE)
		self.title_text_rect = self.title_text_surf.get_rect()
		self.title_text_rect.center = TITLE_POS

		self.selection = 0
		self.select = list()

		self.start_game_text = pygame.font.Font(FONT, MENU_FONT_SIZE)
		self.start_game_text_surf = self.start_game_text.render('Start', AA, WHITE)
		self.start_game_text_rect = self.start_game_text_surf.get_rect()
		self.start_game_text_rect.center = MENU_0_POS
		self.select.append(self.start_game_text_rect)

		self.stats_text = pygame.font.Font(FONT, MENU_FONT_SIZE)
		self.stats_text_surf = self.stats_text.render('Stats', AA, WHITE)
		self.stats_text_rect = self.stats_text_surf.get_rect()
		self.stats_text_rect.center = MENU_1_POS
		self.select.append(self.stats_text_rect)

		self.tutorial_text = pygame.font.Font(FONT, MENU_FONT_SIZE)
		self.tutorial_text_surf = self.tutorial_text.render('Tutorial', AA, WHITE)
		self.tutorial_text_rect = self.tutorial_text_surf.get_rect()
		self.tutorial_text_rect.center = MENU_2_POS
		self.select.append(self.tutorial_text_rect)

		self.exit_text = pygame.font.Font(FONT, MENU_FONT_SIZE)
		self.exit_text_surf = self.exit_text.render('Exit', AA, WHITE)
		self.exit_text_rect = self.exit_text_surf.get_rect()
		self.exit_text_rect.center = MENU_3_POS
		self.select.append(self.exit_text_rect)

	def render(self):
		self.screen.blit(self.surf, self.rect)

		mouse_pos = pygame.mouse.get_pos()
		self.selection = len(self.select)
		for i, r in enumerate(self.select):
			if r.collidepoint(mouse_pos):
				self.selection = i
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.selection == EXIT:
						sys.exit(0)
					elif self.selection == START_GAME:
						return GAME
			elif event.type == QUIT:
				sys.exit(0)

		if self.selection < len(self.select):
			selection_surf = pygame.Surface(self.select[self.selection].size)
			selection_surf.fill(YELLOW)
			selection_surf.set_alpha(100)
			self.screen.blit(selection_surf,self.select[self.selection])

		self.screen.blit(self.title_text_surf, self.title_text_rect)
		self.screen.blit(self.start_game_text_surf, self.start_game_text_rect)
		self.screen.blit(self.stats_text_surf, self.stats_text_rect)
		self.screen.blit(self.tutorial_text_surf, self.tutorial_text_rect)
		self.screen.blit(self.exit_text_surf, self.exit_text_rect)
		pygame.display.flip()
		self.clock.tick(30)
		return MENU