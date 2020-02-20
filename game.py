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
		self.hold_button_icon_surf_2, self.hold_button_icon_rect_2 = load_png('overlay_icons/hold.png', HOLD_ICON_SIZE)
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

		self.enter_battle_rect = pygame.Rect((0, 0), ENTER_BATTLE_RECT_SIZE)
		self.enter_battle_rect.center = ENTER_BATTLE_RECT_POS
		self.enter_battle_surf = pygame.Surface(ENTER_BATTLE_RECT_SIZE)
		self.enter_battle_surf.fill(GRAY)
		self.enter_battle_surf.set_alpha(200)
		self.enter_battle_text_surf = self.font_mini.render('Warp to Battle', AA, WHITE)
		self.enter_battle_text_rect = self.enter_battle_text_surf.get_rect()
		self.enter_battle_text_rect.center = ENTER_BATTLE_TEXT_POS
		self.enter_battle_icon_surf, self.enter_battle_icon_rect = load_png('overlay_icons/battle.png', ENTER_BATTLE_ICON_SIZE)
		self.enter_battle_icon_rect.center = ENTER_BATTLE_ICON_POS



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
		self.ship_swap_index = None

		# AI fitting screen
		self.ai_fitting_icon_surf, self.ai_fitting_icon_rect = load_png('ai.png', AI_FITTING_ICON_SIZE, AI_FITTING_ICON_POS)
		self.ai_fitting_text_surf = self.font_medium.render('Opponents are selecting ships...', AA, WHITE)
		self.ai_fitting_text_rect = self.ai_fitting_text_surf.get_rect()
		self.ai_fitting_text_rect.center = AI_FITTING_TEXT_POS

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
		if self.render_state == FLEET_BATTLE:
			for s in self.players_dict[self.next_opponent].ships:
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
		s_weapon_text_surf = self.ship_overlay_font_mini.render(f'{self.pool.ship_dict[s].weapon_dps:,}' + ' dps', AA, WHITE)
		s_weapon_text_rect = s_weapon_text_surf.get_rect()
		s_weapon_text_rect.center = SHIP_OVERLAY_ICON_WEAPON_TEXT_POS
		s_weapon_text_rect.right = SHIP_OVERLAY_ICON_WEAPON_TEXT_POS[0]
		self.screen.blit(s_weapon_text_surf, s_weapon_text_rect)
		s_drones_text_surf = self.ship_overlay_font_mini.render(f'{self.pool.ship_dict[s].drone_dps:,}' + ' dps', AA, WHITE)
		s_drones_text_rect = s_drones_text_surf.get_rect()
		s_drones_text_rect.center = SHIP_OVERLAY_ICON_DRONES_TEXT_POS
		s_drones_text_rect.right = SHIP_OVERLAY_ICON_DRONES_TEXT_POS[0]
		self.screen.blit(s_drones_text_surf, s_drones_text_rect)
		s_total_dps_text_surf = self.ship_overlay_font_mini.render(f'{self.pool.ship_dict[s].total_dps:,}' + ' dps', AA, WHITE)
		s_total_dps_text_rect = s_total_dps_text_surf.get_rect()
		s_total_dps_text_rect.center = SHIP_OVERLAY_ICON_TOTAL_DPS_TEXT_POS
		s_total_dps_text_rect.right = SHIP_OVERLAY_ICON_TOTAL_DPS_TEXT_POS[0]
		self.screen.blit(s_total_dps_text_surf, s_total_dps_text_rect)
		s_volley_text_surf = self.ship_overlay_font_mini.render(f'{self.pool.ship_dict[s].volley:,}', AA, WHITE)
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

	def roll_ships(self, plyr):
		plyr.plex = max(0, plyr.plex + ROLL_COST)
		for i, s in enumerate(plyr.ships_in_market):
			if s != None:
				self.pool.return_ship(s)
				plyr.ships_in_market[i] = None
		for i, s in enumerate(plyr.ships_in_market):
			s = self.pool.get_ship(plyr.tier)
			plyr.ships_in_market[i] = s
			self.pool.remove_ship(s)

	def refill_ships(self, plyr):
		if not plyr.hold_ships:
			for i, s in enumerate(plyr.ships_in_market):
				if s != None:
					self.pool.return_ship(s)
					plyr.ships_in_market[i] = None
		plyr.hold_ships = False
		for i, s in enumerate(plyr.ships_in_market):
			if s == None:
				self.pool.get_ship(plyr.tier)
				plyr.ships_in_market[i] = s
				self.pool.remove_ship(s)


	def upgrade_tier(self, plyr):
		if plyr.tier < N_TIERS - 1:
			plyr.plex = max(0, plyr.plex + plyr.upgrade_cost)
			plyr.tier = min(N_TIERS - 1, plyr.tier + 1)
			plyr.upgrade_cost = UPGRADE_COST[plyr.tier]
			n_ship_slots = N_MARKET_SHIPS_PER_TIER[plyr.tier] - N_MARKET_SHIPS_PER_TIER[plyr.tier - 1]
			for _ in range(n_ship_slots):
				plyr.ships_in_market.append(None)

	def salvage_ship(self, plyr, ship_index):
		plyr.plex = min(MAX_PLEX, plyr.plex + SALVAGE_CREDIT)
		self.pool.return_ship(plyr.ships[ship_index])
		plyr.ships[ship_index] = None
		plyr.salvaging = False

	def swap_ships(self, plyr, i, j):
		plyr.ships[i], plyr.ships[j] = plyr.ships[j], plyr.ships[i]
		if plyr == self.you:
			if plyr.ships[i] != None:
				self.pool.ship_dict[plyr.ships[i]].icon_rect.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
			if plyr.ships[j] != None:
				self.pool.ship_dict[plyr.ships[j]].icon_rect.center = BATTLE_HEXAGON_POS_PLAYER_1[j]

	def find_next_opponent(self):
		self.next_opponent = random.choice(self.opponents)

	def fit_ai(self, plyr):
		ship_bag = []
		for i in range(N_MARKET_SHIPS_PER_TIER[plyr.tier]):
			ship_bag.append(self.pool.get_ship(plyr.tier))
		if (plyr.tier < N_TIERS - 1):
			if (plyr.plex >= abs(plyr.upgrade_cost)):
				if (random.randrange(0, 100)/100) < self.commander_dict[plyr.who].quick_upgrade_chance:
					plyr.plex + plyr.upgrade_cost
					plyr.tier = min(N_TIERS - 1, plyr.tier + 1)
					plyr.upgrade_cost = UPGRADE_COST[plyr.tier]
			if (plyr.plex + SHIP_COST >= abs(plyr.upgrade_cost)):
				if (random.randrange(0, 100)/100) < self.commander_dict[plyr.who].slow_upgrade_chance:
					plyr.plex + plyr.upgrade_cost
					plyr.tier = min(N_TIERS - 1, plyr.tier + 1)
					plyr.upgrade_cost = UPGRADE_COST[plyr.tier]
		n_new_ships = plyr.plex // abs(SHIP_COST)
		if n_new_ships > 0:
			n_rolls = plyr.plex % abs(ROLL_COST)
			for i in range(N_MARKET_SHIPS_PER_TIER[plyr.tier] * n_rolls):
				ship_bag.append(self.pool.get_ship(plyr.tier))
			ships = []
			for s in ship_bag:
				ships.append(self.pool.ship_dict[s])
			ships.sort(key=operator.attrgetter('ship_score'))
			
			### pick best ships
			current_ships = []
			for s in plyr.ships:
				if s != None:
					current_ships.append(self.pool.ship_dict[s])
			ship_candidates = []
			for _ in range(n_new_ships):
				ship_candidates.append(ships.pop())
			for s in ship_candidates:
				ship_bag.remove(s.ship_id)
			if len(current_ships) + len(ship_candidates) > N_SHIPS_PER_PLAYER:
				current_ships.extend(ship_candidates)
				current_ships.sort(key=operator.attrgetter('ship_score'), reverse=True)
				while len(current_ships) > N_SHIPS_PER_PLAYER:
					s = current_ships.pop()
					for i, ship in enumerate(plyr.ships):
						if ship != None and s.ship_id == ship:
							plyr.ships[i] = None
							self.pool.return_ship(s.ship_id)
							continue
			for i, ship in enumerate(plyr.ships):
				if len(ship_candidates) > 0 and ship == None:
					s = ship_candidates.pop()
					plyr.ships[i] = s.ship_id

			###
		for s in ship_bag:
			self.pool.return_ship(s)
		plyr.plex = 0




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
			s = self.pool.get_ship(self.you.tier)
			self.you.ships_in_market.append(s)
			self.pool.remove_ship(s)

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
		if self.you.plex < abs(ROLL_COST) or self.you.hold_ships:
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

	def draw_enter_battle_button(self):
		self.screen.blit(self.enter_battle_surf, self.enter_battle_rect)
		self.screen.blit(self.enter_battle_text_surf, self.enter_battle_text_rect)
		self.screen.blit(self.enter_battle_icon_surf, self.enter_battle_icon_rect)

	def draw_market(self, mouse_pos):
		self.draw_upgrade_button()
		self.draw_refresh_button()
		self.draw_hold_button()
		self.draw_salvage_button()
		self.draw_enter_battle_button()
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
				if self.you.hold_ships:
					self.hold_button_icon_rect_2.center = r.center
					self.screen.blit(self.hold_button_icon_surf_2, self.hold_button_icon_rect_2)
		for i in range(N_SHIPS_PER_PLAYER):
			if self.ship_escrow != None and self.you.ships[i] == None:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=YELLOW)
			else:
				if self.you.salvaging:
					self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=GRAY)
				else:
					self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i])
			s = self.commander_font_medium.render(str(i + 1), AA, WHITE)
			r = s.get_rect()
			r.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
			self.screen.blit(s, r)
			if self.you.ships[i] != None:
				self.screen.blit(self.pool.ship_dict[self.you.ships[i]].icon_surf, self.pool.ship_dict[self.you.ships[i]].icon_rect)
			if self.you.ships[i] != None and self.you.salvaging:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=PURPLE)
			if self.ship_swap_index != None and i != self.ship_swap_index:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=YELLOW)

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
		elif self.render_state == AI_FITTING:
			return self.render_ai_fitting()
		elif self.render_state == FLEET_BATTLE:
			return self.render_fleet_battle()
		else:
			sys.exit(2)

	def render_fleet_battle(self):
		self.screen.blit(self.battle_bg_surf, self.battle_bg_rect)
		opp = self.players_dict[self.next_opponent]
		mouse_pos = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == QUIT:
				sys.exit(0)

		for i in range(N_SHIPS_PER_PLAYER):
			s = self.commander_font_medium.render(str(i + 1), AA, WHITE)
			r = s.get_rect()
			r.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
			self.screen.blit(s, r)
			r.center = BATTLE_HEXAGON_POS_PLAYER_2[N_SHIPS_PER_PLAYER - i - 1]
			self.screen.blit(s, r)

			self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=GRAY)
			self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_2[N_SHIPS_PER_PLAYER - i - 1], color=GRAY)
			if self.you.ships[i] != None:
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_1[i], color=GREEN)
				self.screen.blit(self.pool.ship_dict[self.you.ships[i]].icon_surf, self.pool.ship_dict[self.you.ships[i]].icon_rect)
			if opp.ships[i] != None:
				r = self.pool.ship_dict[opp.ships[i]].icon_rect
				r.center = BATTLE_HEXAGON_POS_PLAYER_2[N_SHIPS_PER_PLAYER - i - 1]
				self.draw_hexagon(BATTLE_HEXAGON_POS_PLAYER_2[N_SHIPS_PER_PLAYER - i - 1], color=RED)
				self.screen.blit(self.pool.ship_dict[opp.ships[i]].icon_surf, r)


		self.draw_battle_status(self.you, opp)

		self.draw_ship_overlay(mouse_pos)
		pygame.display.flip()
		self.clock.tick(30)
		return GAME

	def draw_battle_status(self, p1, p2):
		cmdr_icon_surf_1 = self.commander_dict[p1.who].battle_surf
		cmdr_icon_rect_1 = self.commander_dict[p1.who].battle_rect
		cmdr_icon_rect_1.center = BATTLE_PLAYER_COMMANDER_ICON_POS_1
		self.screen.blit(cmdr_icon_surf_1, cmdr_icon_rect_1)
		cmdr_hp_surf_1, cmdr_hp_rect_1 = load_png('station_hp.png', BATTLE_PLAYER_COMMANDER_HP_ICON_SIZE, BATTLE_PLAYER_COMMANDER_HP_ICON_POS_1)
		self.screen.blit(cmdr_hp_surf_1, cmdr_hp_rect_1)
		cmdr_tier_surf_1, cmdr_tier_rect_1 = load_png(BATTLE_TIER_PATH[p1.tier], BATTLE_PLAYER_COMMANDER_TIER_SIZE, BATTLE_PLAYER_COMMANDER_TIER_POS_1)
		self.screen.blit(cmdr_tier_surf_1, cmdr_tier_rect_1)
		cmdr_hp_text_surf = self.font_mini.render(str(p1.station_health), AA, WHITE)
		cmdr_hp_text_rect = cmdr_hp_text_surf.get_rect()
		cmdr_hp_text_rect.center = BATTLE_PLAYER_COMMANDER_HP_ICON_POS_1
		self.screen.blit(cmdr_hp_text_surf, cmdr_hp_text_rect)
		r = pygame.Rect((0, 0), SHIP_OVERLAY_SMALL_ICON_SIZE)
		r.center = BATTLE_PLAYER_SHIP_SHIELD_ICON_POS_1
		self.screen.blit(self.ship_overlay_shield_surf, r)
		r.center = BATTLE_PLAYER_SHIP_ARMOR_ICON_POS_1
		self.screen.blit(self.ship_overlay_armor_surf, r)
		r.center = BATTLE_PLAYER_SHIP_HULL_ICON_POS_1
		self.screen.blit(self.ship_overlay_hull_surf, r)

		for i, s in enumerate(p1.ships):
			txt_str = str(i + 1) + '.  '
			if s != None:
				txt_str = ''.join([txt_str, self.pool.ship_dict[s].name])
			txt_surf = self.font_mini.render(txt_str, AA, WHITE)
			txt_rect = txt_surf.get_rect()
			txt_rect.center = BATTLE_PLAYER_SHIP_TEXT_POS_1[i]
			txt_rect.left = BATTLE_PLAYER_SHIP_TEXT_POS_1[i][0]
			self.screen.blit(txt_surf, txt_rect)

			if s != None:
				r = pygame.Rect((0, 0), BATTLE_PLAYER_SHIP_STATUS_BAR_SIZE)
				r.center = BATTLE_PLAYER_SHIP_SHIELD_POS_1[i]
				r.left = BATTLE_PLAYER_SHIP_SHIELD_POS_1[i][0]
				sf = pygame.Surface(BATTLE_PLAYER_SHIP_STATUS_BAR_SIZE)
				sf.fill(RED)
				self.screen.blit(sf, r)
				r.center = BATTLE_PLAYER_SHIP_ARMOR_POS_1[i]
				r.left = BATTLE_PLAYER_SHIP_ARMOR_POS_1[i][0]
				self.screen.blit(sf, r)
				r.center = BATTLE_PLAYER_SHIP_HULL_POS_1[i]
				r.left = BATTLE_PLAYER_SHIP_HULL_POS_1[i][0]
				self.screen.blit(sf, r)

		cmdr_icon_surf_2 = self.commander_dict[p2.who].battle_surf
		cmdr_icon_rect_2 = self.commander_dict[p2.who].battle_rect
		cmdr_icon_rect_2.center = BATTLE_PLAYER_COMMANDER_ICON_POS_2
		self.screen.blit(cmdr_icon_surf_2, cmdr_icon_rect_2)
		cmdr_hp_surf_2, cmdr_hp_rect_2 = load_png('station_hp.png', BATTLE_PLAYER_COMMANDER_HP_ICON_SIZE, BATTLE_PLAYER_COMMANDER_HP_ICON_POS_2)
		self.screen.blit(cmdr_hp_surf_2, cmdr_hp_rect_2)
		cmdr_tier_surf_2, cmdr_tier_rect_2 = load_png(BATTLE_TIER_PATH[p2.tier], BATTLE_PLAYER_COMMANDER_TIER_SIZE, BATTLE_PLAYER_COMMANDER_TIER_POS_2)
		self.screen.blit(cmdr_tier_surf_2, cmdr_tier_rect_2)
		cmdr_hp_text_surf = self.font_mini.render(str(p2.station_health), AA, WHITE)
		cmdr_hp_text_rect = cmdr_hp_text_surf.get_rect()
		cmdr_hp_text_rect.center = BATTLE_PLAYER_COMMANDER_HP_ICON_POS_2
		self.screen.blit(cmdr_hp_text_surf, cmdr_hp_text_rect)
		r = pygame.Rect((0, 0), SHIP_OVERLAY_SMALL_ICON_SIZE)
		r.center = BATTLE_PLAYER_SHIP_SHIELD_ICON_POS_2
		self.screen.blit(self.ship_overlay_shield_surf, r)
		r.center = BATTLE_PLAYER_SHIP_ARMOR_ICON_POS_2
		self.screen.blit(self.ship_overlay_armor_surf, r)
		r.center = BATTLE_PLAYER_SHIP_HULL_ICON_POS_2
		self.screen.blit(self.ship_overlay_hull_surf, r)

		for i, s in enumerate(p2.ships):
			txt_str = str(i + 1) + '.  '
			if s != None:
				txt_str = ''.join([txt_str, self.pool.ship_dict[s].name])
			txt_surf = self.font_mini.render(txt_str, AA, WHITE)
			txt_rect = txt_surf.get_rect()
			txt_rect.center = BATTLE_PLAYER_SHIP_TEXT_POS_2[i]
			txt_rect.left = BATTLE_PLAYER_SHIP_TEXT_POS_2[i][0]
			self.screen.blit(txt_surf, txt_rect)

			if s != None:
				r = pygame.Rect((0, 0), BATTLE_PLAYER_SHIP_STATUS_BAR_SIZE)
				r.center = BATTLE_PLAYER_SHIP_SHIELD_POS_2[i]
				r.left = BATTLE_PLAYER_SHIP_SHIELD_POS_2[i][0]
				sf = pygame.Surface(BATTLE_PLAYER_SHIP_STATUS_BAR_SIZE)
				sf.fill(RED)
				self.screen.blit(sf, r)
				r.center = BATTLE_PLAYER_SHIP_ARMOR_POS_2[i]
				r.left = BATTLE_PLAYER_SHIP_ARMOR_POS_2[i][0]
				self.screen.blit(sf, r)
				r.center = BATTLE_PLAYER_SHIP_HULL_POS_2[i]
				r.left = BATTLE_PLAYER_SHIP_HULL_POS_2[i][0]
				self.screen.blit(sf, r)

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

	def render_ai_fitting(self):
		s = pygame.Surface(RESOLUTION)
		s.fill(GRAY)
		r = pygame.Rect((0, 0), RESOLUTION)
		self.screen.blit(s, r)
		self.screen.blit(self.ai_fitting_icon_surf, self.ai_fitting_icon_rect)
		self.screen.blit(self.ai_fitting_text_surf, self.ai_fitting_text_rect)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)
			elif event.type == QUIT:
				sys.exit(0)

		for p in self.players:
			if p != self.you:
				self.fit_ai(p)
		self.render_state = FLEET_BATTLE

		pygame.display.flip()
		self.clock.tick(30)
		return GAME

	def render_market(self):
		self.screen.blit(self.market_bg_surf, self.market_bg_rect)

		r = pygame.Rect((0, 100), (len(self.you.ships_in_market)*(MARKET_SHIP_ICON_SIZE[0] + MARKET_SHIP_ICON_PADDING), 120))
		r.center = (RESOLUTION[0]//2, RESOLUTION[1]//4)
		s = pygame.Surface(r.size)
		s.fill(BLACK)
		s.set_alpha(100)
		self.screen.blit(s, r)

		mouse_pos = pygame.mouse.get_pos()
		self.draw_player_ranking()
		self.draw_market(mouse_pos)

		if self.you.plex < abs(SHIP_COST):
			r = pygame.Rect((0, 100), (len(self.you.ships_in_market)*(MARKET_SHIP_ICON_SIZE[0] + MARKET_SHIP_ICON_PADDING), 120))
			r.center = (RESOLUTION[0]//2, RESOLUTION[1]//4)
			s = pygame.Surface(r.size)
			s.fill(GRAY)
			s.set_alpha(150)
			self.screen.blit(s, r)

		self.draw_commander_overlay(mouse_pos)
		self.draw_ship_overlay(mouse_pos)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit(0)

				### DEBUG
				if event.key == K_p:
					self.you.plex = 100
				###

			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.ship_escrow != None:
						for i, r in enumerate(BATTLE_HEXAGON_RECTS):
							if r.collidepoint(mouse_pos) and self.you.ships[i] == None and self.you.plex >= abs(SHIP_COST):
								self.you.plex = max(0, self.you.plex + SHIP_COST)
								self.you.ships[i] = self.ship_escrow
								self.pool.ship_dict[self.ship_escrow].icon_rect.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
								self.you.ships_in_market[self.ship_selection_index] = None
								self.ship_escrow = None
								self.ship_selection_index = None
								continue
						self.ship_escrow = None
					elif self.you.salvaging:
						for i, r in enumerate(BATTLE_HEXAGON_RECTS):
							if r.collidepoint(mouse_pos) and self.you.ships[i] != None:
								self.salvage_ship(self.you, i)
								continue
						self.you.salvaging = False
					elif self.ship_swap_index != None:
						for i, r in enumerate(BATTLE_HEXAGON_RECTS):
							if r.collidepoint(mouse_pos):
								self.swap_ships(self.you, i, self.ship_swap_index)
								continue
						self.ship_swap_index = None
					else:
						if self.refresh_button_rect.collidepoint(mouse_pos) and self.you.plex >= abs(ROLL_COST) and not self.you.hold_ships:
							self.roll_ships(self.you)
						elif self.upgrade_button_rect.collidepoint(mouse_pos) and self.you.plex >= abs(self.you.upgrade_cost):
							self.upgrade_tier(self.you)
						elif self.hold_button_rect.collidepoint(mouse_pos):
							self.you.hold_ships = not self.you.hold_ships
						elif self.salvage_button_rect.collidepoint(mouse_pos):
							self.you.salvaging = True
						elif self.enter_battle_rect.collidepoint(mouse_pos):
							self.render_state = AI_FITTING
						else:
							for i, r in enumerate(BATTLE_HEXAGON_RECTS):
								if r.collidepoint(mouse_pos) and self.you.ships[i] != None:
									self.ship_swap_index = i
									continue
							for i, s in enumerate(self.you.ships_in_market):
								if s != None and self.pool.ship_dict[s].icon_rect.collidepoint(mouse_pos) and self.you.plex >= abs(SHIP_COST):
									self.ship_escrow = s
									self.ship_selection_index = i
									continue
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
