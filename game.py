try:
    import sys
    import math
    import random
    import collections
    import pygame
    from pygame.locals import *
    import pygame.gfxdraw

    from copy import copy
    from constants import *
    from utilities import *
    from pool import *
    from market import *
    from player import *
    from commander import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Game():
	def __init__(self, screen, clock):
		self.screen = screen
		self.clock = clock
		self.render_state = COMMANDER_SELECT
		self.commander_bg_surf, self.commander_bg_rect = load_png('commander_bg.png', RESOLUTION)
		self.market_bg_surf, self.market_bg_rect = load_png('market_bg.png', RESOLUTION)
		self.battle_bg_surf, self.battle_bg_rect = load_png('battle_bg.png', RESOLUTION)

		with open('commanders.json') as json_file:
			data = json.load(json_file)
		commanders = data['commanders']
		self.commander_dict = collections.defaultdict()
		self.available_commanders = [_ for _ in range(len(commanders))]
		for i in range(len(commanders)):
			self.commander_dict[i] = Commander(commanders[i])
		self.choose_from_commanders = random.sample(self.available_commanders, N_COMMANDER_CHOICES)
		for i, choice in enumerate(self.choose_from_commanders):
			self.commander_dict[choice].rect.center = COMMANDER_SELECT_ICON_POS[i]

		self.commander_font_medium = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.commander_font_small = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.commander_font_mini = pygame.font.Font(FONT, MINI_FONT_SIZE)
		self.commander_name_surfs = []
		self.commander_name_rects = []
		self.commander_race_surfs = []
		self.commander_race_rects = []
		self.commander_bonus_surfs = []
		self.commander_bonus_rects = []
		self.commander_penalty_surfs = []
		self.commander_penalty_rects = []
		self.commander_info_surfs = []
		self.commander_info_rects = []
		self.commander_highlight_surf = pygame.Surface(COMMANDER_SELECT_HIGHLIGHT_RECT_SIZE)
		self.commander_highlight_surf.fill(YELLOW)
		self.commander_highlight_surf.set_alpha(100)
		self.commander_highlight_rect = self.commander_highlight_surf.get_rect()

		for i in range(N_COMMANDER_CHOICES):
			self.commander_name_surfs.append(self.commander_font_medium.render(self.commander_dict[self.choose_from_commanders[i]].name, AA, WHITE))
			self.commander_name_rects.append(self.commander_name_surfs[i].get_rect())
			self.commander_name_rects[-1].center = COMMANDER_NAME_POS[i]
			self.commander_race_surfs.append(self.commander_font_small.render(self.commander_dict[self.choose_from_commanders[i]].race, AA, WHITE))
			self.commander_race_rects.append(self.commander_race_surfs[i].get_rect())
			self.commander_race_rects[-1].center = COMMANDER_RACE_POS[i]
			self.commander_bonus_surfs.append(self.commander_font_mini.render(self.commander_dict[self.choose_from_commanders[i]].bonus_description, AA, WHITE))
			self.commander_bonus_rects.append(self.commander_bonus_surfs[i].get_rect())
			self.commander_bonus_rects[-1].left, self.commander_bonus_rects[-1].top = COMMANDER_BONUS_DESC_POS[i]
			self.commander_penalty_surfs.append(self.commander_font_mini.render(self.commander_dict[self.choose_from_commanders[i]].penalty_description, AA, WHITE))
			self.commander_penalty_rects.append(self.commander_penalty_surfs[i].get_rect())
			self.commander_penalty_rects[-1].left, self.commander_penalty_rects[-1].top = COMMANDER_PENALTY_DESC_POS[i]
			self.commander_info_surfs.append(pygame.Surface(COMMANDER_SELECT_INFO_RECT_SIZE))
			self.commander_info_surfs[-1].fill(GRAY)
			self.commander_info_surfs[-1].set_alpha(230)
			self.commander_info_rects.append(self.commander_info_surfs[-1].get_rect())
			self.commander_info_rects[-1].center = COMMANDER_SELECT_INFO_RECT_POS[i]

		self.commander = None


	def render(self):
		if self.render_state == COMMANDER_SELECT:
			return self.render_commander_select()
		elif self.render_state == MARKET:
			return self.render_market()
		elif self.render_state == BATTLE:
			return self.render_battle()
		else:
			sys.exit(2)

	def render_commander_select(self):
		mouse_pos = pygame.mouse.get_pos()
		self.commander = None
		self.screen.blit(self.commander_bg_surf, self.commander_bg_rect)

		for i, r in enumerate(self.commander_info_rects):
			if r.collidepoint(mouse_pos):
				self.commander_highlight_rect.center = r.center
				self.screen.blit(self.commander_highlight_surf, self.commander_highlight_rect)
				self.commander = self.choose_from_commanders[i]

		for i, c in enumerate(self.choose_from_commanders):
			self.screen.blit(self.commander_info_surfs[i], self.commander_info_rects[i])
			self.screen.blit(self.commander_dict[c].surf, self.commander_dict[c].rect)
			self.screen.blit(self.commander_name_surfs[i], self.commander_name_rects[i])
			self.screen.blit(self.commander_race_surfs[i], self.commander_race_rects[i])
			self.screen.blit(self.commander_bonus_surfs[i], self.commander_bonus_rects[i])
			self.screen.blit(self.commander_penalty_surfs[i], self.commander_penalty_rects[i])


		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and self.commander != None:
					self.render_state = MARKET
			elif event.type == QUIT:
				sys.exit(0)

		pygame.display.flip()
		self.clock.tick(30)
		return GAME

	def render_market(self):
		self.screen.blit(self.market_bg_surf, self.market_bg_rect)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == QUIT:
				sys.exit(0)

		pygame.display.flip()
		self.clock.tick(30)
		return GAME

	def render_battle(self):
		self.screen.blit(self.battle_bg_surf, self.battle_bg_rect)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == QUIT:
				sys.exit(0)

		pygame.display.flip()
		self.clock.tick(30)
		return GAME
