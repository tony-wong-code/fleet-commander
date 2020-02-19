try:
    import sys
    import pygame
    import math

    from utilities import *
    from constants import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)


RESOLUTION = (1280, 800)
AA = True

FONT = 'evesansneue-regular.otf'
BIG_FONT_SIZE = 50
MEDIUM_FONT_SIZE = 30
SMALL_FONT_SIZE = 20
MINI_FONT_SIZE = 15

N_TIERS = 6
#N_SHIP_COPIES_PER_TIER = (18, 15, 15, 12, 9, 6)
N_SHIP_COPIES_PER_TIER = (1, 1, 1, 1, 1, 1)
N_MARKET_SHIPS_PER_TIER = (4, 5, 6, 7, 8, 9)
N_MARKET_SHIPS_PER_ROW = 3

SHIP_ICON_SIZE = (100, 100)
SHIP_ICON_PADDING = (20, 20)
MARKET_ICON_SIZE = (100, 100)
MARKET_ICON_PADDING = (50, 20)
MARKET_CONTROL_OFFSET = (100, 50)
MARKET_OFFSET = (MARKET_CONTROL_OFFSET[0] + MARKET_ICON_SIZE[0] + MARKET_ICON_PADDING[0], MARKET_CONTROL_OFFSET[1])
UPGRADE_TIER_ICON_POS = (MARKET_CONTROL_OFFSET[0], MARKET_CONTROL_OFFSET[1])
RECYCLE_ICON_POS = (MARKET_CONTROL_OFFSET[0], UPGRADE_TIER_ICON_POS[1] + MARKET_ICON_SIZE[1] + MARKET_ICON_PADDING[1])
HOLD_ICON_POS = (MARKET_CONTROL_OFFSET[0], RECYCLE_ICON_POS[1] + MARKET_ICON_SIZE[1] + MARKET_ICON_PADDING[1])
HOVER_PADDING = (75, 0)
HOVER_SHIP_STATS_POS = (MARKET_OFFSET[0] + N_MARKET_SHIPS_PER_ROW*(SHIP_ICON_SIZE[0] + SHIP_ICON_PADDING[0]) + HOVER_PADDING[0], MARKET_CONTROL_OFFSET[1])
HOVER_SHIP_STATS_SIZE = (500, (N_MARKET_SHIPS_PER_TIER[-1] // N_MARKET_SHIPS_PER_ROW)*(SHIP_ICON_SIZE[1] + SHIP_ICON_PADDING[1]) - SHIP_ICON_PADDING[1])

STATS_OVERLAY_BG_COLOR = (38, 38, 38)
OVERLAY_ALPHA = 150
OVERLAY_SHIP_ICON_SIZE = (200, 200)
OVERLAY_SHIP_ICON_POS = (HOVER_SHIP_STATS_POS[0], HOVER_SHIP_STATS_POS[1])
OVERLAY_FONT_COLOR = (255, 255, 255)
OVERLAY_FONT_ANTIALIASING = True
OVERLAY_TEXT_PADDING = (20, 50)
OVERLAY_SHIP_NAME_POS = (OVERLAY_SHIP_ICON_POS[0] + OVERLAY_SHIP_ICON_SIZE[0] + OVERLAY_TEXT_PADDING[0], OVERLAY_SHIP_ICON_POS[1] + OVERLAY_TEXT_PADDING[1])
OVERLAY_SHIP_RACE_POS = (OVERLAY_SHIP_NAME_POS[0], OVERLAY_SHIP_NAME_POS[1] + OVERLAY_TEXT_PADDING[1])
OVERLAY_SHIP_ATTACK_POS = (OVERLAY_SHIP_ICON_POS[0] + OVERLAY_TEXT_PADDING[0], HOVER_SHIP_STATS_POS[1] + OVERLAY_SHIP_ICON_SIZE[1])
OVERLAY_SHIP_SHIELDS_POS = (OVERLAY_SHIP_ATTACK_POS[0], OVERLAY_SHIP_ATTACK_POS[1] + SMALL_FONT_SIZE)
OVERLAY_SHIP_ARMOR_POS = (OVERLAY_SHIP_ATTACK_POS[0], OVERLAY_SHIP_SHIELDS_POS[1] + SMALL_FONT_SIZE)
OVERLAY_SHIP_HULL_POS = (OVERLAY_SHIP_ATTACK_POS[0], OVERLAY_SHIP_ARMOR_POS[1] + SMALL_FONT_SIZE)
OVERLAY_TIER_ICON_SIZE = (40, 40)

STATION_HEALTH = 100
N_SHIPS_PER_PLAYER = 9
BOARD_SIZE = (5, 2)
TILE_SIZE = (100, 100)
TILE_PADDING = (35, 35)
BOARD_OFFSET = (0.5*RESOLUTION[0] - 2.5*TILE_SIZE[0] - 2*TILE_PADDING[0], 0.5*RESOLUTION[1] + TILE_PADDING[1])

BATTLE_TILE_PADDING = (100, 60)
BATTLE_BOARD_OFFSET_P1 = (0.5*RESOLUTION[0] - 2.5*TILE_SIZE[0] - 2*BATTLE_TILE_PADDING[0], 0.5*RESOLUTION[1] + BATTLE_TILE_PADDING[1])
BATTLE_BOARD_OFFSET_P2 = (0.5*RESOLUTION[0] - 2.5*TILE_SIZE[0] - 2*BATTLE_TILE_PADDING[0], 0.5*RESOLUTION[1] - 2*(BATTLE_TILE_PADDING[1] + TILE_SIZE[1]))

REPROCESS_SIZE = (150, 150)
REPROCESS_PADDING = (50, (2*(TILE_SIZE[1] + 0.5*TILE_PADDING[1]) - REPROCESS_SIZE[1])/2)
REPROCESS_POS = (BOARD_OFFSET[0] + 5*(TILE_SIZE[0] + TILE_PADDING[0]) + REPROCESS_PADDING[0], BOARD_OFFSET[1] + REPROCESS_PADDING[1])

HUMAN = 0
COMPUTER = 1

END_TURN_SIZE = (200, 50)
END_TURN_PADDING = (20, 20)
END_TURN_POS = (RESOLUTION[0] - END_TURN_SIZE[0] - END_TURN_PADDING[0], RESOLUTION[1] - END_TURN_SIZE[1] - END_TURN_PADDING[1])
END_TURN_COLOR = (38, 38, 38)
END_TURN_ALPHA = 150
END_TURN_FONT_COLOR = (0, 255, 0)
END_TURN_FONT_ANTIALIASING = OVERLAY_FONT_ANTIALIASING
END_TURN_TEXT = 'ENTER BATTLE'

STARTING_PLEX = 3
PLEX_ICON_SIZE = (30, 30)
PLEX_PADDING = (75, 0)
PLEX_POS = (MARKET_CONTROL_OFFSET[0] + PLEX_PADDING[0], END_TURN_POS[1] + PLEX_PADDING[1])
MAX_PLEX = 10
SHIP_COST = -3
SHIP_REPROCESS = 1
RECYCLE_COST = 1
ROLL_COST = -1
SALVAGE_CREDIT = 1
UPGRADE_COST = (-5, -7, -8, -9, -11)
PLEX_FONT_ANTIALIASING = OVERLAY_FONT_ANTIALIASING
PLEX_FONT_COLOR = (255, 196, 71)
PLEX_TEXT_PADDING = (25, (PLEX_ICON_SIZE[1] - SMALL_FONT_SIZE)//2)
PLEX_TEXT_POS = (MARKET_CONTROL_OFFSET[0] + PLEX_TEXT_PADDING[0], END_TURN_POS[1] + PLEX_TEXT_PADDING[1])
UPGRADE_TIER_PLEX_ICON_POS = (UPGRADE_TIER_ICON_POS[0] - PLEX_ICON_SIZE[0], UPGRADE_TIER_ICON_POS[1] + (MARKET_ICON_SIZE[1] - PLEX_ICON_SIZE[1])//3)
RECYCLE_PLEX_ICON_POS = (RECYCLE_ICON_POS[0] - PLEX_ICON_SIZE[0], RECYCLE_ICON_POS[1] + (MARKET_ICON_SIZE[1] - PLEX_ICON_SIZE[1])//3)
MISC_PLEX_TEXT_PADDING = (PLEX_ICON_SIZE[0] - SMALL_FONT_SIZE, PLEX_ICON_SIZE[1])

ORDER_TEXT_FONT_ANTIALIASING = OVERLAY_FONT_ANTIALIASING
ORDER_TEXT_FONT_COLOR = (255, 255, 255)

BLACK = (0, 0, 0)
GRAY = (38, 38, 38)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
TEAL = (98, 184, 219)
ORANGE = (255, 129, 0)

BATTLE_TILE_SIZE = (200, 200)
STATUS_SHIELDS_RADIUS = 68
STATUS_ARMOR_RADIUS = 62
STATUS_HULL_RADIUS = 56
STATUS_OUTLINE_THICKNESS = 1
STATUS_GRANULARITY_SHIELDS = 1
STATUS_GRANULARITY_ARMOR = 1
STATUS_GRANULARITY_HULL = 1
STATUS_INTERVALS = 75
START_ANGLE = 135
END_ANGLE = 45
TOTAL_ANGLE = 360 - (START_ANGLE - END_ANGLE)
EACH_ANGLE = TOTAL_ANGLE / STATUS_INTERVALS
THICKNESS_BETWEEN_ANGLES = 3
SHIP_ICON_BATTLE_PADDING = (10, 10)
SHIP_ICON_BATTLE_SIZE = (2*STATUS_SHIELDS_RADIUS + SHIP_ICON_BATTLE_PADDING[0], 2*STATUS_SHIELDS_RADIUS + SHIP_ICON_BATTLE_PADDING[1])

TITLE_FONT_SIZE = 100
TITLE_POS = (RESOLUTION[0]//2, RESOLUTION[1]//3)
MENU_FONT_SIZE = TITLE_FONT_SIZE // 3
MENU_0_POS = (TITLE_POS[0], RESOLUTION[1]//2 + RESOLUTION[1]//8)
MENU_1_POS = (MENU_0_POS[0], MENU_0_POS[1] + 1.5*MENU_FONT_SIZE)
MENU_2_POS = (MENU_0_POS[0], MENU_1_POS[1] + 1.5*MENU_FONT_SIZE)
MENU_3_POS = (MENU_0_POS[0], MENU_2_POS[1] + 1.5*MENU_FONT_SIZE)
MENU_SIZE = 4
START_GAME = 0
STATS = 1
TUTORIAL = 2
EXIT = 3

# game states
MENU = 0
GAME = 1
COMMANDER_SELECT = 2
MARKET = 3
BATTLE = 4

COMMANDER_SELECT_SIZE = (RESOLUTION[0]//5, RESOLUTION[0]//5)
N_COMMANDER_CHOICES = 3
COMMANDER_SELECT_ICON_POS = []
COMMANDER_NAME_POS = []
COMMANDER_RACE_POS = []
COMMANDER_BONUS_DESC_POS = []
COMMANDER_PENALTY_DESC_POS = []
COMMANDER_SELECT_INFO_RECT_POS = []
COMMANDER_PADDING = (RESOLUTION[0] - (N_COMMANDER_CHOICES * COMMANDER_SELECT_SIZE[0]))//(N_COMMANDER_CHOICES + 1)
for i in range(N_COMMANDER_CHOICES):
	COMMANDER_SELECT_ICON_POS.append((int((i + 1)*COMMANDER_PADDING + (0.5+i)*COMMANDER_SELECT_SIZE[0]), RESOLUTION[1]//3))
	COMMANDER_NAME_POS.append((COMMANDER_SELECT_ICON_POS[-1][0], COMMANDER_SELECT_ICON_POS[-1][1] + COMMANDER_SELECT_SIZE[1]//2 + MEDIUM_FONT_SIZE))
	COMMANDER_RACE_POS.append((COMMANDER_NAME_POS[-1][0], COMMANDER_NAME_POS[-1][1] + MEDIUM_FONT_SIZE))
	#COMMANDER_BONUS_DESC_POS.append((COMMANDER_RACE_POS[-1][0] - COMMANDER_SELECT_SIZE[0]//2, COMMANDER_RACE_POS[-1][1] + 3*SMALL_FONT_SIZE))
	#COMMANDER_PENALTY_DESC_POS.append((COMMANDER_BONUS_DESC_POS[-1][0], COMMANDER_BONUS_DESC_POS[-1][1] + 2*SMALL_FONT_SIZE))
	COMMANDER_BONUS_DESC_POS.append((COMMANDER_RACE_POS[-1][0], COMMANDER_RACE_POS[-1][1] + 3*SMALL_FONT_SIZE))
	COMMANDER_PENALTY_DESC_POS.append((COMMANDER_BONUS_DESC_POS[-1][0], COMMANDER_BONUS_DESC_POS[-1][1] + 2*SMALL_FONT_SIZE))
	COMMANDER_SELECT_INFO_RECT_POS.append((COMMANDER_SELECT_ICON_POS[-1][0], RESOLUTION[1]//2))
COMMANDER_SELECT_INFO_RECT_SIZE = (RESOLUTION[0]//4, RESOLUTION[0]//2.15)
COMMANDER_SELECT_HIGHLIGHT_RECT_SIZE = (COMMANDER_SELECT_INFO_RECT_SIZE[0] + COMMANDER_PADDING//4, COMMANDER_SELECT_INFO_RECT_SIZE[1] + COMMANDER_PADDING//4)

COMMANDER_RANKING_ICON_SIZE = (40, 40)
COMMANDER_RANKING_HEALTH_SIZE = (COMMANDER_RANKING_ICON_SIZE[0], 5)
COMMANDER_RANKING_ICON_POS = []
COMMANDER_RANKING_HEALTH_POS = []
COMMANDER_RANKING_ICON_PADDING = (20, 20)
COMMANDER_RANKING_PADDING = (RESOLUTION[0] - 8*COMMANDER_RANKING_ICON_SIZE[0] - 7*COMMANDER_RANKING_ICON_PADDING[0])//2
N_PLAYERS = 8
for i in range(N_PLAYERS):
	COMMANDER_RANKING_ICON_POS.append(
		(
		COMMANDER_RANKING_PADDING + int((0.5 + i)*COMMANDER_RANKING_ICON_SIZE[0]) + i*COMMANDER_RANKING_ICON_PADDING[0],
		COMMANDER_RANKING_ICON_SIZE[0]//2 + COMMANDER_RANKING_ICON_PADDING[1]
		)
	)
	COMMANDER_RANKING_HEALTH_POS.append(
		(
		COMMANDER_RANKING_ICON_POS[i][0] - int(0.5*COMMANDER_RANKING_ICON_SIZE[0]),
		COMMANDER_RANKING_ICON_POS[i][1] + int(0.5*COMMANDER_RANKING_ICON_SIZE[1]),
		)
	)
COMMANDER_OPPONENT_OFFSET = (0, 20)
HIGHLIGHT_THICKNESS = 4
HIGHLIGHT_YOUR_COMMANDER_SIZE = (
	COMMANDER_RANKING_ICON_SIZE[0] + 2*HIGHLIGHT_THICKNESS,
	COMMANDER_RANKING_ICON_SIZE[1] + COMMANDER_RANKING_HEALTH_SIZE[1] + 2*HIGHLIGHT_THICKNESS
)
COMMANDER_OVERLAY_SIZE = (RESOLUTION[0]//4, RESOLUTION[1]//2)
COMMANDER_OVERLAY_POS = (RESOLUTION[0]//2, RESOLUTION[1]//2.5)
COMMANDER_OVERLAY_POS_RIGHT = COMMANDER_OVERLAY_POS[0] + COMMANDER_OVERLAY_SIZE[0]//2
COMMANDER_OVERLAY_ICON_SIZE = (RESOLUTION[0]//7, RESOLUTION[0]//7)
COMMANDER_OVERLAY_ICON_PADDING = (COMMANDER_OVERLAY_SIZE[0] - COMMANDER_OVERLAY_ICON_SIZE[0])//2
COMMANDER_OVERLAY_ICON_POS = (
	COMMANDER_OVERLAY_POS[0],
	COMMANDER_OVERLAY_POS[1] - int(0.5*COMMANDER_OVERLAY_SIZE[1]) + int(0.5*COMMANDER_OVERLAY_ICON_SIZE[1]) + COMMANDER_OVERLAY_ICON_PADDING
)
COMMANDER_OVERLAY_TEXT_POS_0 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_ICON_POS[1] - int(0.5*COMMANDER_OVERLAY_ICON_SIZE[1]) - MEDIUM_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_1 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_ICON_POS[1] + int(0.5*COMMANDER_OVERLAY_ICON_SIZE[1]) + MEDIUM_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_2 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_TEXT_POS_1[1] + 2*SMALL_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_3 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_TEXT_POS_2[1] + SMALL_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_4 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_TEXT_POS_3[1] + SMALL_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_5 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_TEXT_POS_4[1] + SMALL_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_POS_6 = (COMMANDER_OVERLAY_POS[0], COMMANDER_OVERLAY_TEXT_POS_5[1] + SMALL_FONT_SIZE)
COMMANDER_OVERLAY_TEXT_RANKING = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']
COMMANDER_OVERLAY_TIER_POS = (COMMANDER_OVERLAY_POS_RIGHT - 40, COMMANDER_OVERLAY_TEXT_POS_0[1])



MARKET_SHIP_ICON_SIZE = (100, 100)
MARKET_SHIP_ICON_PADDING = (RESOLUTION[0] - N_MARKET_SHIPS_PER_TIER[-1]*MARKET_SHIP_ICON_SIZE[0])//(N_MARKET_SHIPS_PER_TIER[-1] + 1)
MARKET_SHIP_ICON_OFFSET = []
for i in range(N_TIERS):
	MARKET_SHIP_ICON_OFFSET.append(((N_MARKET_SHIPS_PER_TIER[-1]-N_MARKET_SHIPS_PER_TIER[i])*(MARKET_SHIP_ICON_SIZE[0] + MARKET_SHIP_ICON_PADDING))//2)
BATTLE_HEXAGON_RADIUS = 50
BATTLE_HEXAGON_APOTHEM = BATTLE_HEXAGON_RADIUS // (2*math.tan(math.radians(30)))
BATTLE_HEXAGON_OFFSET = int(math.sqrt(math.pow(2*BATTLE_HEXAGON_APOTHEM, 2) - math.pow(BATTLE_HEXAGON_APOTHEM, 2)))
BATTLE_HEXAGON_PADDING = (50, 50)
BATTLE_HEXAGON_SCREEN_BOTTOM_PADDING = 50
BATTLE_HEXAGON_SCREEN_LEFT_PADDING = 50
BATTLE_HEXAGON_X_ANCHOR = 4*BATTLE_HEXAGON_RADIUS + 2*BATTLE_HEXAGON_PADDING[0] + BATTLE_HEXAGON_SCREEN_LEFT_PADDING
BATTLE_HEXAGON_Y_ANCHOR = RESOLUTION[1] - 5*BATTLE_HEXAGON_APOTHEM - 2*BATTLE_HEXAGON_PADDING[1] - BATTLE_HEXAGON_SCREEN_BOTTOM_PADDING
BATTLE_HEXAGON_POS_PLAYER_1 = [
	(BATTLE_HEXAGON_X_ANCHOR, BATTLE_HEXAGON_Y_ANCHOR),
	(BATTLE_HEXAGON_X_ANCHOR + BATTLE_HEXAGON_OFFSET + BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + BATTLE_HEXAGON_APOTHEM + int(0.5*BATTLE_HEXAGON_PADDING[1])),
	(BATTLE_HEXAGON_X_ANCHOR + 2*BATTLE_HEXAGON_OFFSET + 2*BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + 2*BATTLE_HEXAGON_APOTHEM + BATTLE_HEXAGON_PADDING[1]),
	(BATTLE_HEXAGON_X_ANCHOR - BATTLE_HEXAGON_OFFSET - BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + BATTLE_HEXAGON_APOTHEM + int(0.5*BATTLE_HEXAGON_PADDING[1])),
	(BATTLE_HEXAGON_X_ANCHOR, BATTLE_HEXAGON_Y_ANCHOR + 2*BATTLE_HEXAGON_APOTHEM + BATTLE_HEXAGON_PADDING[1]),
	(BATTLE_HEXAGON_X_ANCHOR + BATTLE_HEXAGON_OFFSET + BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + 3*BATTLE_HEXAGON_APOTHEM + int(1.5*BATTLE_HEXAGON_PADDING[1])),
	(BATTLE_HEXAGON_X_ANCHOR - 2*BATTLE_HEXAGON_OFFSET - 2*BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + 2*BATTLE_HEXAGON_APOTHEM + BATTLE_HEXAGON_PADDING[1]),
	(BATTLE_HEXAGON_X_ANCHOR - BATTLE_HEXAGON_OFFSET - BATTLE_HEXAGON_PADDING[0], BATTLE_HEXAGON_Y_ANCHOR + 3*BATTLE_HEXAGON_APOTHEM + int(1.5*BATTLE_HEXAGON_PADDING[1])),
	(BATTLE_HEXAGON_X_ANCHOR, BATTLE_HEXAGON_Y_ANCHOR + 4*BATTLE_HEXAGON_APOTHEM + 2*BATTLE_HEXAGON_PADDING[1]),
]
BATTLE_HEXAGON_RECTS = []
for i in range(len(BATTLE_HEXAGON_POS_PLAYER_1)):
	r = pygame.Rect((0, 0), MARKET_SHIP_ICON_SIZE)
	r.center = BATTLE_HEXAGON_POS_PLAYER_1[i]
	BATTLE_HEXAGON_RECTS.append(r)

RACE_NAMES = ['Amarr', 'Caldari', 'Gallente', 'Minmatar', 'Pirate Faction']

SHIP_OVERLAY_SIZE = (RESOLUTION[0]//2.3, RESOLUTION[1]//1.6)
SHIP_OVERLAY_PADDING = (25, 25)
SHIP_OVERLAY_POS = (RESOLUTION[0] - int(0.5*SHIP_OVERLAY_SIZE[0]) - SHIP_OVERLAY_PADDING[0], RESOLUTION[1] - int(0.5* SHIP_OVERLAY_SIZE[1]) - SHIP_OVERLAY_PADDING[1])
SHIP_ICON_OVERLAY_SIZE = (300, 300)
SHIP_ICON_OVERLAY_POS = (SHIP_OVERLAY_POS[0] - SHIP_OVERLAY_SIZE[0]//2.7, SHIP_OVERLAY_POS[1] - SHIP_OVERLAY_SIZE[1]//2 + SHIP_ICON_OVERLAY_SIZE[1]//2.4)
SHIP_OVERLAY_POS_LEFT = SHIP_OVERLAY_POS[0] - SHIP_OVERLAY_SIZE[0]//2
SHIP_OVERLAY_POS_RIGHT = SHIP_OVERLAY_POS[0] + SHIP_OVERLAY_SIZE[0]//2
SHIP_OVERLAY_POS_TOP = SHIP_OVERLAY_POS[1] - SHIP_OVERLAY_SIZE[1]//2
SHIP_OVERLAY_POS_BOTTOM = SHIP_OVERLAY_POS[1] + SHIP_OVERLAY_SIZE[1]//2
SHIP_OVERLAY_NAME_POS = (SHIP_OVERLAY_POS_LEFT + int(0.85*SHIP_ICON_OVERLAY_SIZE[0]), SHIP_OVERLAY_POS_TOP + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_RACE_POS = (SHIP_OVERLAY_NAME_POS[0], SHIP_OVERLAY_NAME_POS[1] + int(1.3*BIG_FONT_SIZE))
SHIP_OVERLAY_ROLE_POS = ((SHIP_OVERLAY_NAME_POS[0], SHIP_OVERLAY_RACE_POS[1] + int(1.4*SMALL_FONT_SIZE)))

WEAPON_TYPES = ['energy', 'missile', 'hybrid', 'projectile', 'smartbomb']
SHIP_OVERLAY_SMALL_ICON_SIZE = (32, 32)
"""SHIP_OVERLAY_ICON_WEAPON_POS = 
SHIP_OVERLAY_ICON_DRONES_POS = 
SHIP_OVERLAY_ICON_VOLLEY_POS = 
SHIP_OVERLAY_ICON_SALVO_PERIOD_POS = 
SHIP_OVERLAY_ICON_SHIELD_POS = 
SHIP_OVERLAY_ICON_ARMOR_POS = 
SHIP_OVERLAY_ICON_HULL_POS = 
SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS = 
SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS = 
SHIP_OVERLAY_ICON_EVASION_POS = 
"""
N_SHIP_ABILITIES = 10
A_AURA = 0
A_WARP_FIELD = 1
A_CAP_TRANSFER = 2
A_ECM = 3
A_TACKLE = 4
A_NEUT = 5
A_SENSOR_BOOSTER = 6
A_DAMP = 7
A_PAINTER = 8
A_DISRUPTOR = 9

SHIP_OVERLAY_ABILITY_PADDING = ((SHIP_OVERLAY_SIZE[0] - 10*SHIP_OVERLAY_SMALL_ICON_SIZE[0])//11, SHIP_OVERLAY_POS_BOTTOM - SHIP_OVERLAY_SMALL_ICON_SIZE[1])
SHIP_OVERLAY_ICON_AURA_POS = ((1 + 0)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(0.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_WARP_FIELD_POS = ((1 + 1)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(1.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_CAP_TRANSFER_POS = ((1 + 2)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(2.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_ECM_POS = ((1 + 3)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_TACKLE_POS = ((1 + 4)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(4.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_NEUT_POS = ((1 + 5)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(5.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_SENSOR_BOOSTER_POS = ((1 + 6)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(6.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_DAMP_POS = ((1 + 7)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(7.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_PAINTER_POS = ((1 + 8)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(8.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])
SHIP_OVERLAY_ICON_DISRUPTOR_POS = ((1 + 9)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(9.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ABILITY_PADDING[1])

SHIP_OVERLAY_ABILITY_ICONS_POS = [
	#SHIP_OVERLAY_ICON_AURA_POS,
	#SHIP_OVERLAY_ICON_WARP_FIELD_POS,
	SHIP_OVERLAY_ICON_CAP_TRANSFER_POS,
	SHIP_OVERLAY_ICON_ECM_POS,
	SHIP_OVERLAY_ICON_TACKLE_POS,
	SHIP_OVERLAY_ICON_NEUT_POS,
	SHIP_OVERLAY_ICON_SENSOR_BOOSTER_POS,
	SHIP_OVERLAY_ICON_DAMP_POS,
	SHIP_OVERLAY_ICON_PAINTER_POS,
	SHIP_OVERLAY_ICON_DISRUPTOR_POS
]
SHIP_OVERLAY_ABILITY_ICONS_RECT = []
for p in SHIP_OVERLAY_ABILITY_ICONS_POS:
	r = pygame.Rect((0, 0), SHIP_OVERLAY_SMALL_ICON_SIZE)
	r.center = p
	SHIP_OVERLAY_ABILITY_ICONS_RECT.append(r)

W_NONE = -1
W_ENERGY = 0
W_MISSILE = 1
W_HYBRID = 2
W_PROJECTILE = 3
W_SMARTBOMB = 4
SHIP_OVERLAY_ABILITY_TEXT_POS = ((1 + 0)*SHIP_OVERLAY_ABILITY_PADDING[0] + int(0.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]) + SHIP_OVERLAY_POS_LEFT, SHIP_OVERLAY_ICON_AURA_POS[1])
SHIP_OVERLAY_TIER_POS = (SHIP_OVERLAY_POS_RIGHT - 40, SHIP_OVERLAY_POS_TOP + 40)
SHIP_OVERLAY_ICON_WEAPON_POS = (SHIP_OVERLAY_NAME_POS[0], SHIP_OVERLAY_ROLE_POS[1] + BIG_FONT_SIZE)
SHIP_OVERLAY_ICON_DRONES_POS = (SHIP_OVERLAY_ICON_WEAPON_POS[0], SHIP_OVERLAY_ICON_WEAPON_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_TOTAL_DPS_POS = (SHIP_OVERLAY_ICON_WEAPON_POS[0], SHIP_OVERLAY_ICON_DRONES_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_VOLLEY_POS = (SHIP_OVERLAY_ICON_WEAPON_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_WEAPON_POS[1])
SHIP_OVERLAY_ICON_SALVO_PERIOD_POS = (SHIP_OVERLAY_ICON_VOLLEY_POS[0], SHIP_OVERLAY_ICON_VOLLEY_POS[1] + MEDIUM_FONT_SIZE)

SHIP_OVERLAY_ICON_WEAPON_TEXT_POS = (SHIP_OVERLAY_ICON_WEAPON_POS[0] + int(3.1*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_WEAPON_POS[1])
SHIP_OVERLAY_ICON_DRONES_TEXT_POS = (SHIP_OVERLAY_ICON_DRONES_POS[0] + int(3.1*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_DRONES_POS[1])
SHIP_OVERLAY_ICON_TOTAL_DPS_TEXT_POS = (SHIP_OVERLAY_ICON_TOTAL_DPS_POS[0] + int(3.1*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_TOTAL_DPS_POS[1])
SHIP_OVERLAY_ICON_VOLLEY_TEXT_POS = (SHIP_OVERLAY_ICON_VOLLEY_POS[0] + int(2.4*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_VOLLEY_POS[1])
SHIP_OVERLAY_ICON_SALVO_PERIOD_TEXT_POS = (SHIP_OVERLAY_ICON_SALVO_PERIOD_POS[0] + int(2.4*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_SALVO_PERIOD_POS[1])

SHIP_OVERLAY_ICON_SHIELD_POS = (SHIP_OVERLAY_POS_LEFT + int(2*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_TOTAL_DPS_POS[1] + int(1.5*BIG_FONT_SIZE))
SHIP_OVERLAY_ICON_ARMOR_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0], SHIP_OVERLAY_ICON_SHIELD_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_HULL_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0], SHIP_OVERLAY_ICON_ARMOR_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_TOTAL_HP_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0], SHIP_OVERLAY_ICON_HULL_POS[1] + MEDIUM_FONT_SIZE)

SHIP_OVERLAY_ICON_SHIELD_TEXT_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0] + int(3.3*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_SHIELD_POS[1])
SHIP_OVERLAY_ICON_ARMOR_TEXT_POS = (SHIP_OVERLAY_ICON_ARMOR_POS[0] + int(3.3*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_ARMOR_POS[1])
SHIP_OVERLAY_ICON_HULL_TEXT_POS = (SHIP_OVERLAY_ICON_HULL_POS[0] + int(3.3*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_HULL_POS[1])
SHIP_OVERLAY_ICON_TOTAL_HP_TEXT_POS = (SHIP_OVERLAY_ICON_TOTAL_HP_POS[0] + int(3.3*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_TOTAL_HP_POS[1])

SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_SHIELD_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_ARMOR_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_TOTAL_RECHARGE_POS = (SHIP_OVERLAY_ICON_SHIELD_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_HULL_POS[1] + MEDIUM_FONT_SIZE)

SHIP_OVERLAY_ICON_SHIELD_RECHARGE_TEXT_POS = (SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[1])
SHIP_OVERLAY_ICON_ARMOR_RECHARGE_TEXT_POS = (SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS[1])
SHIP_OVERLAY_ICON_TOTAL_RECHARGE_TEXT_POS = (SHIP_OVERLAY_ICON_TOTAL_RECHARGE_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_TOTAL_RECHARGE_POS[1])
SHIP_OVERLAY_RECHARGE_RATE_TEXT_POS = ((SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[0] + SHIP_OVERLAY_ICON_SHIELD_RECHARGE_TEXT_POS[0])//2, SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[1] - MEDIUM_FONT_SIZE)

SHIP_OVERLAY_ICON_REMOTE_SHIELD_POS = (SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_SHIELD_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_REMOTE_ARMOR_POS = (SHIP_OVERLAY_ICON_ARMOR_RECHARGE_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_ARMOR_POS[1] + MEDIUM_FONT_SIZE)
SHIP_OVERLAY_ICON_TOTAL_REMOTE_POS = (SHIP_OVERLAY_ICON_TOTAL_RECHARGE_POS[0] + int(5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_HULL_POS[1] + MEDIUM_FONT_SIZE)

SHIP_OVERLAY_ICON_REMOTE_SHIELD_TEXT_POS = (SHIP_OVERLAY_ICON_REMOTE_SHIELD_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_REMOTE_SHIELD_POS[1])
SHIP_OVERLAY_ICON_REMOTE_ARMOR_TEXT_POS = (SHIP_OVERLAY_ICON_REMOTE_ARMOR_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_REMOTE_ARMOR_POS[1])
SHIP_OVERLAY_ICON_TOTAL_REMOTE_TEXT_POS = (SHIP_OVERLAY_ICON_TOTAL_REMOTE_POS[0] + int(3.5*SHIP_OVERLAY_SMALL_ICON_SIZE[0]), SHIP_OVERLAY_ICON_TOTAL_REMOTE_POS[1])
SHIP_OVERLAY_REMOTE_REP_TEXT_POS = ((SHIP_OVERLAY_ICON_REMOTE_SHIELD_POS[0] + SHIP_OVERLAY_ICON_REMOTE_SHIELD_TEXT_POS[0])//2, SHIP_OVERLAY_ICON_SHIELD_RECHARGE_POS[1] - MEDIUM_FONT_SIZE)

MARKET_BUTTON_ICON_SIZE = (50, 50)
MARKET_BUTTON_ICON_2_SIZE = (32, 32)
MARKET_BUTTON_SIZE = (RESOLUTION[0]//4, 75)
MARKET_BUTTON_PADDING = 100
MARKET_BUTTON_POS_0 = (int(3*RESOLUTION[0]//4), RESOLUTION[1]//2)
MARKET_BUTTON_POS_1 = (MARKET_BUTTON_POS_0[0], MARKET_BUTTON_POS_0[1] + MARKET_BUTTON_PADDING)
MARKET_BUTTON_POS_2 = (MARKET_BUTTON_POS_0[0], MARKET_BUTTON_POS_1[1] + MARKET_BUTTON_PADDING)
MARKET_BUTTON_POS_3 = (MARKET_BUTTON_POS_0[0], MARKET_BUTTON_POS_2[1] + MARKET_BUTTON_PADDING)
MARKET_BUTTON_POS_LEFT = MARKET_BUTTON_POS_0[0] - MARKET_BUTTON_SIZE[0]//2
MARKET_BUTTON_POS_RIGHT = MARKET_BUTTON_POS_0[0] + MARKET_BUTTON_SIZE[0]//2
MARKET_BUTTON_LEFT_ICON_POS_0 = (MARKET_BUTTON_POS_LEFT + MARKET_BUTTON_SIZE[0]//6, MARKET_BUTTON_POS_0[1])
MARKET_BUTTON_LEFT_ICON_POS_1 = (MARKET_BUTTON_LEFT_ICON_POS_0[0], MARKET_BUTTON_POS_1[1])
MARKET_BUTTON_LEFT_ICON_POS_2 = (MARKET_BUTTON_LEFT_ICON_POS_0[0], MARKET_BUTTON_POS_2[1])
MARKET_BUTTON_LEFT_ICON_POS_3 = (MARKET_BUTTON_LEFT_ICON_POS_0[0], MARKET_BUTTON_POS_3[1])
MARKET_BUTTON_RIGHT_ICON_POS_0 = (MARKET_BUTTON_POS_RIGHT - MARKET_BUTTON_SIZE[0]//12, MARKET_BUTTON_POS_0[1])
MARKET_BUTTON_RIGHT_ICON_POS_1 = (MARKET_BUTTON_RIGHT_ICON_POS_0[0], MARKET_BUTTON_POS_1[1])
MARKET_BUTTON_RIGHT_ICON_POS_2 = (MARKET_BUTTON_RIGHT_ICON_POS_0[0], MARKET_BUTTON_POS_2[1])
MARKET_BUTTON_RIGHT_ICON_POS_3 = (MARKET_BUTTON_RIGHT_ICON_POS_0[0], MARKET_BUTTON_POS_3[1])
MARKET_BUTTON_RIGHT_TEXT_0 = (MARKET_BUTTON_RIGHT_ICON_POS_0[0] - MARKET_BUTTON_ICON_2_SIZE[0]//1.5, MARKET_BUTTON_RIGHT_ICON_POS_0[1])
MARKET_BUTTON_RIGHT_TEXT_1 = (MARKET_BUTTON_RIGHT_TEXT_0[0], MARKET_BUTTON_RIGHT_ICON_POS_1[1])
MARKET_BUTTON_RIGHT_TEXT_3 = (MARKET_BUTTON_RIGHT_TEXT_0[0], MARKET_BUTTON_RIGHT_ICON_POS_3[1])
MARKET_PLEX_ICON_SIZE = (64, 64)
MARKET_PLEX_ICON_POS = (MARKET_BUTTON_POS_0[0] + MARKET_PLEX_ICON_SIZE[0]//1.5, MARKET_BUTTON_POS_0[1] - int(0.8*MARKET_BUTTON_PADDING))
MARKET_PLEX_TEXT_POS = (MARKET_BUTTON_POS_0[0], MARKET_PLEX_ICON_POS[1])