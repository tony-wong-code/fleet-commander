try:
    import sys
    import math
    import random
    import collections
    import pygame
    import operator
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

		self.font_medium = pygame.font.Font(FONT, MEDIUM_FONT_SIZE)
		self.font_small = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.font_mini = pygame.font.Font(FONT, MINI_FONT_SIZE)
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

		self.upgrade_button_rect = pygame.Rect((0, 0), MARKET_BUTTON_SIZE)
		self.upgrade_button_rect.center = MARKET_BUTTON_POS_0
		self.upgrade_button_surf = pygame.Surface(MARKET_BUTTON_SIZE)
		self.upgrade_button_surf.fill(GRAY)
		self.upgrade_button_surf.set_alpha(200)
		self.refresh_button_rect = pygame.Rect((0, 0), MARKET_BUTTON_SIZE)
		self.refresh_button_rect.center = MARKET_BUTTON_POS_1
		self.refresh_button_surf = pygame.Surface(MARKET_BUTTON_SIZE)
		self.refresh_button_surf.fill(GRAY)
		self.refresh_button_surf.set_alpha(200)
		self.hold_button_rect = pygame.Rect((0, 0), MARKET_BUTTON_SIZE)
		self.hold_button_rect.center = MARKET_BUTTON_POS_2
		self.hold_button_surf = pygame.Surface(MARKET_BUTTON_SIZE)
		self.hold_button_surf.fill(GRAY)
		self.hold_button_surf.set_alpha(200)
		self.salvage_button_rect = pygame.Rect((0, 0), MARKET_BUTTON_SIZE)
		self.salvage_button_rect.center = MARKET_BUTTON_POS_3
		self.salvage_button_surf = pygame.Surface(MARKET_BUTTON_SIZE)
		self.salvage_button_surf.fill(GRAY)
		self.salvage_button_surf.set_alpha(200)

		self.upgrade_button_icon_surfs = []
		for i in range(1, N_TIERS):
			s, r = load_png('overlay_icons/tier_' + str(i) + '.png', MARKET_BUTTON_ICON_SIZE)
			self.upgrade_button_icon_surfs.append(s)
		self.upgrade_button_icon_rect = pygame.Rect((0, 0), MARKET_BUTTON_ICON_SIZE)
		self.upgrade_button_icon_rect.center = MARKET_BUTTON_LEFT_ICON_POS_0

		self.refresh_button_icon_surf, self.refresh_button_icon_rect = load_png('overlay_icons/roll.png', MARKET_BUTTON_ICON_SIZE)
		self.refresh_button_icon_rect.center = MARKET_BUTTON_LEFT_ICON_POS_1
		self.hold_button_icon_surf, self.hold_button_icon_rect = load_png('overlay_icons/hold.png', MARKET_BUTTON_ICON_SIZE)
		self.hold_button_icon_rect.center = MARKET_BUTTON_LEFT_ICON_POS_2
		self.salvage_button_icon_surf, self.salvage_button_icon_rect = load_png('overlay_icons/salvage.png', MARKET_BUTTON_ICON_SIZE)
		self.salvage_button_icon_rect.center = MARKET_BUTTON_LEFT_ICON_POS_3
		self.plex_icon_surf, self.tmp_rect = load_png('overlay_icons/plex.png', MARKET_BUTTON_ICON_2_SIZE)
		self.plex_icon_rect_0 = pygame.Rect((0, 0), MARKET_BUTTON_ICON_2_SIZE)
		self.plex_icon_rect_1 = pygame.Rect((0, 0), MARKET_BUTTON_ICON_2_SIZE)
		self.plex_icon_rect_3 = pygame.Rect((0, 0), MARKET_BUTTON_ICON_2_SIZE)
		self.plex_icon_rect_0.center = MARKET_BUTTON_RIGHT_ICON_POS_0
		self.plex_icon_rect_1.center = MARKET_BUTTON_RIGHT_ICON_POS_1
		self.plex_icon_rect_3.center = MARKET_BUTTON_RIGHT_ICON_POS_3
		self.market_plex_surf, self.market_plex_rect = load_png('overlay_icons/plex.png', MARKET_PLEX_ICON_SIZE)
		self.market_plex_rect.center = MARKET_PLEX_ICON_POS




		for i in range(N_COMMANDER_CHOICES):
			self.commander_name_surfs.append(self.commander_font_medium.render(self.commander_dict[self.choose_from_commanders[i]].name, AA, WHITE))
			self.commander_name_rects.append(self.commander_name_surfs[i].get_rect())
			self.commander_name_rects[-1].center = COMMANDER_NAME_POS[i]
			self.commander_race_surfs.append(self.commander_font_small.render(self.commander_dict[self.choose_from_commanders[i]].race, AA, WHITE))
			self.commander_race_rects.append(self.commander_race_surfs[i].get_rect())
			self.commander_race_rects[-1].center = COMMANDER_RACE_POS[i]
			self.commander_bonus_surfs.append(self.commander_font_mini.render(self.commander_dict[self.choose_from_commanders[i]].bonus_description, AA, WHITE))
			self.commander_bonus_rects.append(self.commander_bonus_surfs[i].get_rect())
			self.commander_bonus_rects[-1].center = COMMANDER_BONUS_DESC_POS[i]
			self.commander_penalty_surfs.append(self.commander_font_mini.render(self.commander_dict[self.choose_from_commanders[i]].penalty_description, AA, WHITE))
			self.commander_penalty_rects.append(self.commander_penalty_surfs[i].get_rect())
			self.commander_penalty_rects[-1].center = COMMANDER_PENALTY_DESC_POS[i]

			self.commander_info_surfs.append(pygame.Surface(COMMANDER_SELECT_INFO_RECT_SIZE))
			self.commander_info_surfs[-1].fill(GRAY)
			self.commander_info_surfs[-1].set_alpha(230)
			self.commander_info_rects.append(self.commander_info_surfs[-1].get_rect())
			self.commander_info_rects[-1].center = COMMANDER_SELECT_INFO_RECT_POS[i]

		self.commander = None
		self.players = []
		self.pool = Pool()
		self.opponents = []
		self.next_opponent = None
		self.players_dict = collections.defaultdict()
		self.you = None

		self.ship_overlay_font_medium = pygame.font.Font(FONT, BIG_FONT_SIZE)
		self.ship_overlay_font_small = pygame.font.Font(FONT, SMALL_FONT_SIZE)
		self.ship_overlay_font_mini = pygame.font.Font(FONT, MINI_FONT_SIZE)

		self.ship_overlay_ability_surfs = collections.defaultdict()
		self.ship_overlay_ability_aura_surf, self.ship_overlay_ability_aura_rect = load_png('overlay_icons/aura.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_AURA_POS)
		self.ship_overlay_ability_surfs[A_AURA] = self.ship_overlay_ability_aura_surf
		self.ship_overlay_ability_warp_field_surf, self.ship_overlay_ability_warp_field_rect = load_png('overlay_icons/warp_field.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WARP_FIELD_POS)
		self.ship_overlay_ability_surfs[A_WARP_FIELD] = self.ship_overlay_ability_warp_field_surf
		self.ship_overlay_ability_cap_transfer_surf, self.ship_overlay_ability_cap_transfer_rect = load_png('overlay_icons/cap_transfer.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_CAP_TRANSFER_POS)
		self.ship_overlay_ability_surfs[A_CAP_TRANSFER] = self.ship_overlay_ability_cap_transfer_surf
		self.ship_overlay_ability_ecm_surf, self.ship_overlay_ability_ecm_rect = load_png('overlay_icons/ecm.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_ECM_POS)
		self.ship_overlay_ability_surfs[A_ECM] = self.ship_overlay_ability_ecm_surf
		self.ship_overlay_ability_tackle_surf, self.ship_overlay_ability_tackle_rect = load_png('overlay_icons/tackle.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_TACKLE_POS)
		self.ship_overlay_ability_surfs[A_TACKLE] = self.ship_overlay_ability_tackle_surf
		self.ship_overlay_ability_neut_surf, self.ship_overlay_ability_neut_rect = load_png('overlay_icons/neut.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_NEUT_POS)
		self.ship_overlay_ability_surfs[A_NEUT] = self.ship_overlay_ability_neut_surf
		self.ship_overlay_ability_sensor_booster_surf, self.ship_overlay_ability_sensor_booster_rect = load_png('overlay_icons/sensor_booster.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_SENSOR_BOOSTER_POS)
		self.ship_overlay_ability_surfs[A_SENSOR_BOOSTER] = self.ship_overlay_ability_sensor_booster_surf
		self.ship_overlay_ability_damp_surf, self.ship_overlay_ability_damp_rect = load_png('overlay_icons/damp.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_DAMP_POS)
		self.ship_overlay_ability_surfs[A_DAMP] = self.ship_overlay_ability_damp_surf
		self.ship_overlay_ability_painter_surf, self.ship_overlay_ability_painter_rect = load_png('overlay_icons/painter.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_PAINTER_POS)
		self.ship_overlay_ability_surfs[A_PAINTER] = self.ship_overlay_ability_painter_surf
		self.ship_overlay_ability_disruptor_surf, self.ship_overlay_ability_disruptor_rect = load_png('overlay_icons/disruptor.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_DISRUPTOR_POS)
		self.ship_overlay_ability_surfs[A_DISRUPTOR] = self.ship_overlay_ability_disruptor_surf

		self.ship_overlay_weapon_surfs = collections.defaultdict()
		self.ship_overlay_weapon_energy_surf, self.ship_overlay_weapon_type_rect = load_png('overlay_icons/energy.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_ENERGY] = self.ship_overlay_weapon_energy_surf
		self.ship_overlay_weapon_missile_surf, self.ship_overlay_weapon_type_rect = load_png('overlay_icons/missile.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_MISSILE] = self.ship_overlay_weapon_missile_surf
		self.ship_overlay_weapon_hybrid_surf, self.ship_overlay_weapon_type_rect = load_png('overlay_icons/hybrid.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_HYBRID] = self.ship_overlay_weapon_hybrid_surf
		self.ship_overlay_weapon_projectile_surf, self.ship_overlay_weapon_type_rect = load_png('overlay_icons/projectile.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_PROJECTILE] = self.ship_overlay_weapon_projectile_surf
		self.ship_overlay_weapon_smartbomb_surf, self.ship_overlay_weapon_type_rect = load_png('overlay_icons/smartbomb.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_SMARTBOMB] = self.ship_overlay_weapon_smartbomb_surf
		self.ship_overlay_weapon_none_surf, self.ship_overlay_weapon_none_rect = load_png('overlay_icons/none.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_WEAPON_POS)
		self.ship_overlay_weapon_surfs[W_NONE] = self.ship_overlay_weapon_none_surf

		self.ship_overlay_drones_surf, self.ship_overlay_drones_rect = load_png('overlay_icons/drones.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_DRONES_POS)
		self.ship_overlay_total_dps_surf, self.ship_overlay_total_dps_rect = load_png('overlay_icons/total_dps.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_TOTAL_DPS_POS)
		self.ship_overlay_volley_surf, self.ship_overlay_volley_rect = load_png('overlay_icons/volley.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_VOLLEY_POS)
		self.ship_overlay_salvo_period_surf, self.ship_overlay_salvo_period_rect = load_png('overlay_icons/salvo_period.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_SALVO_PERIOD_POS)
		self.ship_overlay_shield_surf, self.ship_overlay_shield_rect = load_png('overlay_icons/shield.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_SHIELD_POS)
		self.ship_overlay_armor_surf, self.ship_overlay_armor_rect = load_png('overlay_icons/armor.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_ARMOR_POS)
		self.ship_overlay_hull_surf, self.ship_overlay_hull_rect = load_png('overlay_icons/hull.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_HULL_POS)
		self.ship_overlay_total_hp_surf, self.ship_overlay_total_hp_rect = load_png('overlay_icons/total_hp.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_TOTAL_HP_POS)
		self.ship_overlay_shield_recharge_surf, self.ship_overlay_shield_recharge_rect = load_png('overlay_icons/shield_recharge.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS)
		self.ship_overlay_armor_recharge_surf, self.ship_overlay_armor_recharge_rect = load_png('overlay_icons/armor_recharge.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS)
		self.ship_overlay_total_recharge_surf, self.ship_overlay_total_recharge_rect = load_png('overlay_icons/total_recharge.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_TOTAL_RECHARGE_POS)
		self.ship_overlay_remote_shield_surf, self.ship_overlay_remote_shield_rect = load_png('overlay_icons/remote_shield.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_REMOTE_SHIELD_POS)
		self.ship_overlay_remote_armor_surf, self.ship_overlay_remote_armor_rect = load_png('overlay_icons/remote_armor.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_REMOTE_ARMOR_POS)
		self.ship_overlay_total_remote_surf, self.ship_overlay_total_remote_rect = load_png('overlay_icons/total_remote_rep.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ICON_TOTAL_REMOTE_POS)
		self.ship_overlay_evasion_surf, self.ship_overlay_evasion_rect = load_png('overlay_icons/evasion.png', SHIP_OVERLAY_SMALL_ICON_SIZE, SHIP_OVERLAY_ABILITY_ICONS_POS[6])

		self.ship_selection = None
		self.ship_escrow = None


	def draw_commander_overlay(self, mouse_pos):
		for ranking, cmdr in enumerate(self.players):
			if cmdr.rect.collidepoint(mouse_pos):
				bg_rect = pygame.Rect((0, 0), COMMANDER_OVERLAY_SIZE)
				bg_rect.center = COMMANDER_OVERLAY_POS
				bg_surf = pygame.Surface(COMMANDER_OVERLAY_SIZE)
				bg_surf.fill(GRAY)
				bg_surf.set_alpha(240)
				txt = COMMANDER_OVERLAY_TEXT_RANKING[ranking]
				txt = ''.join([txt, ' [', str(cmdr.station_health), ']'])
				if cmdr.who == self.commander:
					txt = ''.join([txt, ' (You)'])
				elif cmdr.who == self.next_opponent:
					txt = ''.join([txt, ' (Next)'])
				cmdr_ranking_surf = self.commander_font_small.render(txt, AA, WHITE)
				cmdr_ranking_rect = cmdr_ranking_surf.get_rect()
				cmdr_ranking_rect.center = COMMANDER_OVERLAY_TEXT_POS_0
				cmdr_name_surf = self.commander_font_small.render(self.commander_dict[cmdr.who].name, AA, WHITE)
				cmdr_name_rect = cmdr_name_surf.get_rect()
				cmdr_name_rect.center = COMMANDER_OVERLAY_TEXT_POS_1
				cmdr_bonus_surf = self.commander_font_mini.render(self.commander_dict[cmdr.who].bonus_description, AA, WHITE)
				cmdr_bonus_rect = cmdr_bonus_surf.get_rect()
				cmdr_bonus_rect.center = COMMANDER_OVERLAY_TEXT_POS_2
				cmdr_penalty_surf = self.commander_font_mini.render(self.commander_dict[cmdr.who].penalty_description, AA, WHITE)
				cmdr_penalty_rect = cmdr_penalty_surf.get_rect()
				cmdr_penalty_rect.center = COMMANDER_OVERLAY_TEXT_POS_3


				self.screen.blit(bg_surf, bg_rect)
				self.screen.blit(self.commander_dict[cmdr.who].commander_overlay_surf, self.commander_dict[cmdr.who].commander_overlay_rect)
				self.screen.blit(cmdr_name_surf, cmdr_name_rect)
				self.screen.blit(cmdr_bonus_surf, cmdr_bonus_rect)
				self.screen.blit(cmdr_penalty_surf, cmdr_penalty_rect)
				self.screen.blit(cmdr_ranking_surf, cmdr_ranking_rect)
				self.draw_hexagon(COMMANDER_OVERLAY_TIER_POS, 20, YELLOW)
				self.draw_hexagon(COMMANDER_OVERLAY_TIER_POS, 24, YELLOW)
				c_tier_surf = self.commander_font_small.render(str(self.players_dict[cmdr.who].tier), AA, YELLOW)
				c_tier_rect = c_tier_surf.get_rect()
				c_tier_rect.center = COMMANDER_OVERLAY_TIER_POS
				self.screen.blit(c_tier_surf, c_tier_rect)

	def draw_ship_overlay(self, mouse_pos):
		for s in self.you.ships_in_market:
			if s is not None and self.pool.ship_dict[s].icon_rect.collidepoint(mouse_pos):
				self.draw_ship_overlay_helper(s)
		for s in self.you.ships:
			if s is not None and self.pool.ship_dict[s].icon_rect.collidepoint(mouse_pos):
				self.draw_ship_overlay_helper(s)

	def draw_ship_overlay_helper(self, s):
		bg_rect = pygame.Rect((0, 0), SHIP_OVERLAY_SIZE)
		bg_rect.center = SHIP_OVERLAY_POS
		bg_surf = pygame.Surface(SHIP_OVERLAY_SIZE)
		bg_surf.fill(GRAY)
		bg_surf.set_alpha(255)
		self.screen.blit(bg_surf, bg_rect)

		s_surf = self.pool.ship_dict[s].overlay_surf
		s_rect = self.pool.ship_dict[s].overlay_rect
		s_rect.center = SHIP_ICON_OVERLAY_POS
		self.screen.blit(s_surf, s_rect)

		s_name_surf = self.ship_overlay_font_medium.render(self.pool.ship_dict[s].name, AA, WHITE)
		s_name_rect = s_name_surf.get_rect()
		s_name_rect.left, s_name_rect.top = SHIP_OVERLAY_NAME_POS
		self.screen.blit(s_name_surf, s_name_rect)

		s_race_surf = self.ship_overlay_font_small.render(RACE_NAMES[self.pool.ship_dict[s].race], AA, WHITE)
		s_race_rect = s_race_surf.get_rect()
		s_race_rect.left, s_race_rect.top = SHIP_OVERLAY_RACE_POS
		self.screen.blit(s_race_surf, s_race_rect)

		s_role_surf = self.ship_overlay_font_mini.render(self.pool.ship_dict[s].role, AA, WHITE)
		s_role_rect = s_role_surf.get_rect()
		s_role_rect.left, s_role_rect.top = SHIP_OVERLAY_ROLE_POS
		self.screen.blit(s_role_surf, s_role_rect)

		for i, a in enumerate(self.pool.ship_dict[s].abilities):
			self.screen.blit(self.ship_overlay_ability_surfs[a], SHIP_OVERLAY_ABILITY_ICONS_RECT[i])

		s_abilities_surf = self.ship_overlay_font_small.render('Abilities', AA, WHITE)
		s_abilities_rect = s_abilities_surf.get_rect()
		s_abilities_rect.center = SHIP_OVERLAY_ABILITY_TEXT_POS
		s_abilities_rect.left = SHIP_OVERLAY_ABILITY_TEXT_POS[0]
		self.screen.blit(s_abilities_surf, s_abilities_rect)

		self.draw_hexagon(SHIP_OVERLAY_TIER_POS, 20, YELLOW)
		self.draw_hexagon(SHIP_OVERLAY_TIER_POS, 24, YELLOW)
		s_tier_surf = self.ship_overlay_font_small.render(str(self.pool.ship_dict[s].tier), AA, YELLOW)
		s_tier_rect = s_tier_surf.get_rect()
		s_tier_rect.center = SHIP_OVERLAY_TIER_POS
		self.screen.blit(s_tier_surf, s_tier_rect)

		self.screen.blit(self.ship_overlay_weapon_surfs[self.pool.ship_dict[s].weapon_type], self.ship_overlay_weapon_type_rect)
		self.screen.blit(self.ship_overlay_drones_surf, self.ship_overlay_drones_rect)
		self.screen.blit(self.ship_overlay_total_dps_surf, self.ship_overlay_total_dps_rect)
		self.screen.blit(self.ship_overlay_volley_surf, self.ship_overlay_volley_rect)
		self.screen.blit(self.ship_overlay_salvo_period_surf, self.ship_overlay_salvo_period_rect)
		self.screen.blit(self.ship_overlay_shield_surf, self.ship_overlay_shield_rect)
		self.screen.blit(self.ship_overlay_armor_surf, self.ship_overlay_armor_rect)
		self.screen.blit(self.ship_overlay_hull_surf, self.ship_overlay_hull_rect)
		self.screen.blit(self.ship_overlay_total_hp_surf, self.ship_overlay_total_hp_rect)
		self.screen.blit(self.ship_overlay_shield_recharge_surf, self.ship_overlay_shield_recharge_rect)
		self.screen.blit(self.ship_overlay_armor_recharge_surf, self.ship_overlay_armor_recharge_rect)
		self.screen.blit(self.ship_overlay_total_recharge_surf, self.ship_overlay_total_recharge_rect)
		self.screen.blit(self.ship_overlay_remote_shield_surf, self.ship_overlay_remote_shield_rect)
		self.screen.blit(self.ship_overlay_remote_armor_surf, self.ship_overlay_remote_armor_rect)
		self.screen.blit(self.ship_overlay_total_remote_surf, self.ship_overlay_total_remote_rect)
		self.screen.blit(self.ship_overlay_evasion_surf, self.ship_overlay_evasion_rect)
		s_weapon_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].weapon_dps) + ' dps', AA, WHITE)
		s_weapon_text_rect = s_weapon_text_surf.get_rect()
		s_weapon_text_rect.center = SHIP_OVERLAY_ICON_WEAPON_TEXT_POS
		s_weapon_text_rect.right = SHIP_OVERLAY_ICON_WEAPON_TEXT_POS[0]
		self.screen.blit(s_weapon_text_surf, s_weapon_text_rect)
		s_drones_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].drone_dps) + ' dps', AA, WHITE)
		s_drones_text_rect = s_drones_text_surf.get_rect()
		s_drones_text_rect.center = SHIP_OVERLAY_ICON_DRONES_TEXT_POS
		s_drones_text_rect.right = SHIP_OVERLAY_ICON_DRONES_TEXT_POS[0]
		self.screen.blit(s_drones_text_surf, s_drones_text_rect)
		s_total_dps_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].total_dps) + ' dps', AA, WHITE)
		s_total_dps_text_rect = s_total_dps_text_surf.get_rect()
		s_total_dps_text_rect.center = SHIP_OVERLAY_ICON_TOTAL_DPS_TEXT_POS
		s_total_dps_text_rect.right = SHIP_OVERLAY_ICON_TOTAL_DPS_TEXT_POS[0]
		self.screen.blit(s_total_dps_text_surf, s_total_dps_text_rect)
		s_volley_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].volley), AA, WHITE)
		s_volley_text_rect = s_volley_text_surf.get_rect()
		s_volley_text_rect.center = SHIP_OVERLAY_ICON_VOLLEY_TEXT_POS
		s_volley_text_rect.right = SHIP_OVERLAY_ICON_VOLLEY_TEXT_POS[0]
		self.screen.blit(s_volley_text_surf, s_volley_text_rect)
		s_salvo_period_text_surf = self.ship_overlay_font_mini.render(format(self.pool.ship_dict[s].salvo_period, '.1f') + ' s', AA, WHITE)
		s_salvo_period_text_rect = s_salvo_period_text_surf.get_rect()
		s_salvo_period_text_rect.center = SHIP_OVERLAY_ICON_SALVO_PERIOD_TEXT_POS
		s_salvo_period_text_rect.right = SHIP_OVERLAY_ICON_SALVO_PERIOD_TEXT_POS[0]
		self.screen.blit(s_salvo_period_text_surf, s_salvo_period_text_rect)
		s_shield_text_surf = self.ship_overlay_font_mini.render(f'{int(self.pool.ship_dict[s].shield_k * 1000):,}' + ' ehp', AA, WHITE)
		s_shield_text_rect = s_shield_text_surf.get_rect()
		s_shield_text_rect.center = SHIP_OVERLAY_ICON_SHIELD_TEXT_POS
		s_shield_text_rect.right = SHIP_OVERLAY_ICON_SHIELD_TEXT_POS[0]
		self.screen.blit(s_shield_text_surf, s_shield_text_rect)
		s_armor_text_surf = self.ship_overlay_font_mini.render(f'{int(self.pool.ship_dict[s].armor_k * 1000):,}' + ' ehp', AA, WHITE)
		s_armor_text_rect = s_armor_text_surf.get_rect()
		s_armor_text_rect.center = SHIP_OVERLAY_ICON_ARMOR_TEXT_POS
		s_armor_text_rect.right = SHIP_OVERLAY_ICON_ARMOR_TEXT_POS[0]
		self.screen.blit(s_armor_text_surf, s_armor_text_rect)
		s_hull_text_surf = self.ship_overlay_font_mini.render(f'{int(self.pool.ship_dict[s].hull_k * 1000):,}' + ' ehp', AA, WHITE)
		s_hull_text_rect = s_hull_text_surf.get_rect()
		s_hull_text_rect.center = SHIP_OVERLAY_ICON_HULL_TEXT_POS
		s_hull_text_rect.right = SHIP_OVERLAY_ICON_HULL_TEXT_POS[0]
		self.screen.blit(s_hull_text_surf, s_hull_text_rect)
		s_total_hp_text_surf = self.ship_overlay_font_mini.render(f'{int(self.pool.ship_dict[s].total_hp * 1000):,}' + ' ehp', AA, WHITE)
		s_total_hp_text_rect = s_total_hp_text_surf.get_rect()
		s_total_hp_text_rect.center = SHIP_OVERLAY_ICON_TOTAL_HP_TEXT_POS
		s_total_hp_text_rect.right = SHIP_OVERLAY_ICON_TOTAL_HP_TEXT_POS[0]
		self.screen.blit(s_total_hp_text_surf, s_total_hp_text_rect)
		s_shield_recharge_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].shield_recharge) + ' ehp/s', AA, WHITE)
		s_shield_recharge_text_rect = s_shield_recharge_text_surf.get_rect()
		s_shield_recharge_text_rect.center = SHIP_OVERLAY_ICON_SHIELD_RECHARGE_TEXT_POS
		s_shield_recharge_text_rect.right = SHIP_OVERLAY_ICON_SHIELD_RECHARGE_TEXT_POS[0]
		self.screen.blit(s_shield_recharge_text_surf, s_shield_recharge_text_rect)
		s_armor_recharge_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].armor_recharge) + ' ehp/s', AA, WHITE)
		s_armor_recharge_text_rect = s_armor_recharge_text_surf.get_rect()
		s_armor_recharge_text_rect.center = SHIP_OVERLAY_ICON_ARMOR_RECHARGE_TEXT_POS
		s_armor_recharge_text_rect.right = SHIP_OVERLAY_ICON_ARMOR_RECHARGE_TEXT_POS[0]
		self.screen.blit(s_armor_recharge_text_surf, s_armor_recharge_text_rect)
		s_total_recharge_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].total_recharge) + ' ehp/s', AA, WHITE)
		s_total_recharge_text_rect = s_total_recharge_text_surf.get_rect()
		s_total_recharge_text_rect.center = SHIP_OVERLAY_ICON_TOTAL_RECHARGE_TEXT_POS
		s_total_recharge_text_rect.right = SHIP_OVERLAY_ICON_TOTAL_RECHARGE_TEXT_POS[0]
		self.screen.blit(s_total_recharge_text_surf, s_total_recharge_text_rect)
		s_remote_shield_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].remote_shield_rep) + ' ehp/s', AA, WHITE)
		s_remote_shield_text_rect = s_remote_shield_text_surf.get_rect()
		s_remote_shield_text_rect.center = SHIP_OVERLAY_ICON_REMOTE_SHIELD_TEXT_POS
		s_remote_shield_text_rect.right = SHIP_OVERLAY_ICON_REMOTE_SHIELD_TEXT_POS[0]
		self.screen.blit(s_remote_shield_text_surf, s_remote_shield_text_rect)
		s_remote_armor_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].remote_armor_rep) + ' ehp/s', AA, WHITE)
		s_remote_armor_text_rect = s_remote_armor_text_surf.get_rect()
		s_remote_armor_text_rect.center = SHIP_OVERLAY_ICON_REMOTE_ARMOR_TEXT_POS
		s_remote_armor_text_rect.right = SHIP_OVERLAY_ICON_REMOTE_ARMOR_TEXT_POS[0]
		self.screen.blit(s_remote_armor_text_surf, s_remote_armor_text_rect)
		s_total_remote_text_surf = self.ship_overlay_font_mini.render(str(self.pool.ship_dict[s].total_remote_rep) + ' ehp/s', AA, WHITE)
		s_total_remote_text_rect = s_total_remote_text_surf.get_rect()
		s_total_remote_text_rect.center = SHIP_OVERLAY_ICON_TOTAL_REMOTE_TEXT_POS
		s_total_remote_text_rect.right = SHIP_OVERLAY_ICON_TOTAL_REMOTE_TEXT_POS[0]
		self.screen.blit(s_total_remote_text_surf, s_total_remote_text_rect)
		s_recharge_rate_text_surf = self.ship_overlay_font_mini.render('RECHARGE RATES', AA, WHITE)
		s_recharge_rate_text_rect = s_recharge_rate_text_surf.get_rect()
		s_recharge_rate_text_rect.center = SHIP_OVERLAY_RECHARGE_RATE_TEXT_POS
		self.screen.blit(s_recharge_rate_text_surf, s_recharge_rate_text_rect)
		s_remote_rep_text_surf = self.ship_overlay_font_mini.render('REMOTE REPAIR', AA, WHITE)
		s_remote_rep_text_rect = s_remote_rep_text_surf.get_rect()
		s_remote_rep_text_rect.center = SHIP_OVERLAY_REMOTE_REP_TEXT_POS
		self.screen.blit(s_remote_rep_text_surf, s_remote_rep_text_rect)
		s_evasion_text_surf = self.ship_overlay_font_mini.render(f'{self.pool.ship_dict[s].evasion:.2f}', AA, WHITE)
		s_evasion_text_rect = s_evasion_text_surf.get_rect()
		s_evasion_text_rect.center = SHIP_OVERLAY_ABILITY_ICONS_POS[7]
		s_evasion_text_rect.right = SHIP_OVERLAY_ABILITY_ICONS_POS[7][0]
		self.screen.blit(s_evasion_text_surf, s_evasion_text_rect)


	def find_next_opponent(self):
		self.next_opponent = random.choice(self.opponents)

	def init_players(self):
		plyrs = random.sample(self.available_commanders, 7)
		self.opponents = plyrs[:]
		plyrs.append(self.commander)
		for p in plyrs:
			s, r = load_png(self.commander_dict[p].image, COMMANDER_RANKING_ICON_SIZE)
			self.players_dict[p] = Player(p, self.pool, s, r)
			self.players.append(self.players_dict[p])
		self.players.sort(key=operator.attrgetter('station_health'), reverse=True)
		self.you = self.players_dict[self.commander]
		self.find_next_opponent()

	def init_player_market(self):
		if self.you.hold_ships == False:
			self.you.ships_in_market = []
		self.you.hold_ships = False
		while len(self.you.ships_in_market) < N_MARKET_SHIPS_PER_TIER[self.you.tier]:
			self.you.ships_in_market.append(self.pool.get_ship(self.you.tier))

	def draw_upgrade_button(self):
		if self.you.tier < N_TIERS - 1:
			self.screen.blit(self.upgrade_button_surf, self.upgrade_button_rect)
			surf = self.font_mini.render('Upgrade to Tier ' + str(self.you.tier + 1), AA, WHITE)
			rect = surf.get_rect()
			rect.center = MARKET_BUTTON_POS_0
			self.screen.blit(surf, rect)
			self.screen.blit(self.upgrade_button_icon_surfs[self.you.tier], self.upgrade_button_icon_rect)
			self.screen.blit(self.plex_icon_surf, self.plex_icon_rect_0)
			surf = self.font_mini.render(str(self.you.upgrade_cost), AA, ORANGE)
			rect = surf.get_rect()
			rect.center = MARKET_BUTTON_RIGHT_TEXT_0
			rect.right = MARKET_BUTTON_RIGHT_TEXT_0[0]
			self.screen.blit(surf, rect)
			if self.you.plex < abs(self.you.upgrade_cost):
				self.screen.blit(self.upgrade_button_surf, self.upgrade_button_rect)

	def draw_refresh_button(self):
		self.screen.blit(self.refresh_button_surf, self.refresh_button_rect)
		surf = self.font_mini.render('Refresh Market', AA, WHITE)
		rect = surf.get_rect()
		rect.center = MARKET_BUTTON_POS_1
		self.screen.blit(surf, rect)
		self.screen.blit(self.refresh_button_icon_surf, self.refresh_button_icon_rect)
		self.screen.blit(self.plex_icon_surf, self.plex_icon_rect_1)
		surf = self.font_mini.render(str(ROLL_COST), AA, ORANGE)
		rect = surf.get_rect()
		rect.center = MARKET_BUTTON_RIGHT_TEXT_1
		rect.right = MARKET_BUTTON_RIGHT_TEXT_1[0]
		self.screen.blit(surf, rect)
		if self.you.plex < abs(ROLL_COST):
			self.screen.blit(self.refresh_button_surf, self.refresh_button_rect)

	def draw_hold_button(self):
		self.screen.blit(self.hold_button_surf, self.hold_button_rect)
		surf = self.font_mini.render('Reserve Market', AA, WHITE)
		rect = surf.get_rect()
		rect.center = MARKET_BUTTON_POS_2
		self.screen.blit(surf, rect)
		self.screen.blit(self.hold_button_icon_surf, self.hold_button_icon_rect)
		if len([_ for _ in self.you.ships_in_market if _ is not None]) == 0:
			self.screen.blit(self.hold_button_surf, self.hold_button_rect)

	def draw_salvage_button(self):
		self.screen.blit(self.salvage_button_surf, self.salvage_button_rect)
		surf = self.font_mini.render('Salvage Ship', AA, WHITE)
		rect = surf.get_rect()
		rect.center = MARKET_BUTTON_POS_3
		self.screen.blit(surf, rect)
		self.screen.blit(self.salvage_button_icon_surf, self.salvage_button_icon_rect)
		self.screen.blit(self.plex_icon_surf, self.plex_icon_rect_3)
		surf = self.font_mini.render('+' + str(SALVAGE_CREDIT), AA, ORANGE)
		rect = surf.get_rect()
		rect.center = MARKET_BUTTON_RIGHT_TEXT_3
		rect.right = MARKET_BUTTON_RIGHT_TEXT_3[0]
		self.screen.blit(surf, rect)
		if len([_ for _ in self.you.ships if _ is not None]) == 0:
			self.screen.blit(self.salvage_button_surf, self.salvage_button_rect)

	def draw_market(self, mouse_pos):
		self.draw_upgrade_button()
		self.draw_refresh_button()
		self.draw_hold_button()
		self.draw_salvage_button()
		self.screen.blit(self.market_plex_surf, self.market_plex_rect)
		surf = self.font_medium.render(str(self.you.plex) + '/' + str(MAX_PLEX), AA, ORANGE)
		rect = surf.get_rect()
		rect.center = MARKET_PLEX_TEXT_POS
		rect.right = MARKET_PLEX_TEXT_POS[0]
		self.screen.blit(surf, rect)

		for i, s in enumerate(self.you.ships_in_market):
			if s is None:
				pos = ((i + 1)*MARKET_SHIP_ICON_PADDING + int((i + 0.5)*MARKET_SHIP_ICON_SIZE[0]) + MARKET_SHIP_ICON_OFFSET[self.you.tier], RESOLUTION[1]//4)
				self.draw_hexagon(pos, color=ORANGE)
			else:
				r = self.pool.ship_dict[s].icon_rect
				r.center = ((i + 1)*MARKET_SHIP_ICON_PADDING + int((i + 0.5)*MARKET_SHIP_ICON_SIZE[0]) + MARKET_SHIP_ICON_OFFSET[self.you.tier], RESOLUTION[1]//4)
				self.screen.blit(self.pool.ship_dict[s].icon_surf, r)
		for i in range(N_SHIPS_PER_PLAYER):
			if self.ship_escrow != None and self.you.ships[i] == None:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=YELLOW)
			else:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i])
			s = self.commander_font_medium.render(str(i + 1), AA, WHITE)
			r = s.get_rect()
			r.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
			self.screen.blit(s, r)
			if self.you.ships[i] != None:
				self.screen.blit(self.pool.ship_dict[self.you.ships[i]].icon_surf, self.pool.ship_dict[self.you.ships[i]].icon_rect)

	def draw_hexagon(self, pos, radius=BATTLE_HEXAGON_RADIUS, color=TEAL):
		x = pos[0]
		y = pos[1]
		pygame.draw.aalines(
			self.screen,
			color,
			True,
			[
		        (x + radius * math.cos(2 * math.pi * i / 6), y + radius * math.sin(2 * math.pi * i / 6))
		        for i in range(6)
    		],
    		1
    	)

	def draw_player_ranking(self):
		for i, p in enumerate(self.players):
			r = pygame.Rect(COMMANDER_RANKING_HEALTH_POS[i], COMMANDER_RANKING_HEALTH_SIZE)
			s = pygame.Surface(r.size)
			s.fill(RED)
			r2_size = (int(COMMANDER_RANKING_HEALTH_SIZE[0]*(p.station_health/100)), COMMANDER_RANKING_HEALTH_SIZE[1])
			r2 = pygame.Rect(COMMANDER_RANKING_HEALTH_POS[i], r2_size)
			s2 = pygame.Surface(r2.size)
			s2.fill(GREEN)
			if p.who == self.next_opponent:
				r.top = COMMANDER_RANKING_HEALTH_POS[i][1] + COMMANDER_OPPONENT_OFFSET[1]
				r2.top = r.top
				p.rect.center = (COMMANDER_RANKING_ICON_POS[i][0], COMMANDER_RANKING_ICON_POS[i][1] + COMMANDER_OPPONENT_OFFSET[1])
			else:
				p.rect.center = COMMANDER_RANKING_ICON_POS[i]
				if p.who == self.commander:
					r_you_pos = (p.rect.left - HIGHLIGHT_THICKNESS, p.rect.top - HIGHLIGHT_THICKNESS)
					r_you = pygame.Rect(r_you_pos, HIGHLIGHT_YOUR_COMMANDER_SIZE)
					s_you = pygame.Surface(r_you.size)
					s_you.fill(TEAL)
					s_you.set_alpha(180)
					self.screen.blit(s_you, r_you)
			self.screen.blit(s, r)
			self.screen.blit(s2, r2)
			self.screen.blit(p.surf, p.rect)
			

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
				# START OF MARKET PHASE
				if event.button == 1 and self.commander != None:
					self.available_commanders.pop(self.commander)
					self.render_state = MARKET
					self.init_players()
					self.init_player_market()
			elif event.type == QUIT:
				sys.exit(0)

		pygame.display.flip()
		self.clock.tick(30)
		return GAME

	def render_market(self):
		self.screen.blit(self.market_bg_surf, self.market_bg_rect)
		mouse_pos = pygame.mouse.get_pos()
		self.draw_player_ranking()
		self.draw_market(mouse_pos)

		self.draw_commander_overlay(mouse_pos)
		self.draw_ship_overlay(mouse_pos)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					for i, s in enumerate(self.you.ships_in_market):
						if s != None and self.pool.ship_dict[s].icon_rect.collidepoint(mouse_pos):
							self.ship_selection = s
							self.ship_selection_index = i
					if self.ship_escrow != None:
						for i, r in enumerate(BATTLE_HEXAGON_RECTS):
							if r.collidepoint(mouse_pos):
								self.you.ships[i] = self.ship_escrow
								self.pool.ship_dict[self.ship_escrow].icon_rect.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
								self.you.ships_in_market[self.ship_selection_index] = None
								self.ship_escrow = None
								self.ship_selection_index = None
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					if self.ship_selection != None and self.pool.ship_dict[self.ship_selection].icon_rect.collidepoint(mouse_pos):
						self.ship_escrow = self.ship_selection
						self.ship_selection = None
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
