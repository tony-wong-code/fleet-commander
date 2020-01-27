try:
    import sys
    import pygame
    from constants import *
    from utilities import *
    from pool import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Overlay():
	def __init__(self, pool):
		self.bg = pygame.Surface(HOVER_SHIP_STATS_SIZE)
		self.bg.fill(STATS_OVERLAY_BG_COLOR)
		self.bg_rect = self.bg.get_rect()
		self.bg_rect.x = HOVER_SHIP_STATS_POS[0]
		self.bg_rect.y = HOVER_SHIP_STATS_POS[1]
		self.bg.set_alpha(OVERLAY_ALPHA)
		self.pool = pool
		self.overlay_surf = list()
		self.ship_name = pygame.font.Font(FONT, BIG_FONT_SIZE)
		self.ship_name_surf = None
		self.ship_name_rect = None
		self.ship_race = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.ship_race_surf = None
		self.ship_race_rect = None
		self.ship_tier = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.ship_tier_surf = None
		self.ship_tier_rect = None
		self.ship_shields = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.ship_shields_surf = None
		self.ship_shields_rect = None
		self.ship_armor = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.ship_armor_surf = None
		self.ship_armor_rect = None
		self.ship_hull = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.ship_hull_surf = None
		self.ship_hull_rect = None

	def render(self, screen, s):
		screen.blit(self.bg, self.bg_rect)
		ship_surf, ship_rect = load_png(self.pool.ship_dict[s].name.lower() + '.png', OVERLAY_SHIP_ICON_SIZE)
		ship_rect.x = OVERLAY_SHIP_ICON_POS[0]
		ship_rect.y = OVERLAY_SHIP_ICON_POS[1]
		screen.blit(ship_surf, ship_rect)
		
		self.ship_name_surf = self.ship_name.render(self.pool.ship_dict[s].name, OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_name_rect = self.ship_name_surf.get_rect()
		self.ship_name_rect.x = OVERLAY_SHIP_NAME_POS[0]
		self.ship_name_rect.y = OVERLAY_SHIP_NAME_POS[1]
		self.ship_race_surf = self.ship_race.render(self.pool.ship_dict[s].race, OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_race_rect = self.ship_race_surf.get_rect()
		self.ship_race_rect.x = OVERLAY_SHIP_RACE_POS[0]
		self.ship_race_rect.y = OVERLAY_SHIP_RACE_POS[1]
		self.ship_tier_surf = self.ship_tier.render('tier: ' + str(self.pool.ship_dict[s].tier), OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_tier_rect = self.ship_tier_surf.get_rect()
		self.ship_tier_rect.x = OVERLAY_SHIP_TIER_POS[0]
		self.ship_tier_rect.y = OVERLAY_SHIP_TIER_POS[1]
		self.ship_shields_surf = self.ship_shields.render('shields: ' + str(self.pool.ship_dict[s].shields), OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_shields_rect = self.ship_shields_surf.get_rect()
		self.ship_shields_rect.x = OVERLAY_SHIP_SHIELDS_POS[0]
		self.ship_shields_rect.y = OVERLAY_SHIP_SHIELDS_POS[1]
		self.ship_armor_surf = self.ship_armor.render('armor: ' + str(self.pool.ship_dict[s].armor), OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_armor_rect = self.ship_armor_surf.get_rect()
		self.ship_armor_rect.x = OVERLAY_SHIP_ARMOR_POS[0]
		self.ship_armor_rect.y = OVERLAY_SHIP_ARMOR_POS[1]
		self.ship_hull_surf = self.ship_hull.render('hull: ' + str(self.pool.ship_dict[s].hull), OVERLAY_FONT_ANTIALIASING, OVERLAY_FONT_COLOR)
		self.ship_hull_rect = self.ship_hull_surf.get_rect()
		self.ship_hull_rect.x = OVERLAY_SHIP_HULL_POS[0]
		self.ship_hull_rect.y = OVERLAY_SHIP_HULL_POS[1]

		screen.blit(self.ship_name_surf, self.ship_name_rect)
		screen.blit(self.ship_race_surf, self.ship_race_rect)
		screen.blit(self.ship_tier_surf, self.ship_tier_rect)
		screen.blit(self.ship_shields_surf, self.ship_shields_rect)
		screen.blit(self.ship_armor_surf, self.ship_armor_rect)
		screen.blit(self.ship_hull_surf, self.ship_hull_rect)


