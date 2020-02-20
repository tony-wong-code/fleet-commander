try:
    import sys
    import pygame

    from utilities import *
    from constants import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Ship(pygame.sprite.Sprite):
	def __init__(self, ship_info, ship_id):
		super(Ship, self).__init__()
		self.ship_id = ship_id
		self.name = ship_info['name']
		self.race = ship_info['race']
		self.size = ship_info['size']
		self.role = ship_info['role']
		self.tier = ship_info['tier']
		self.volley = ship_info['volley']
		self.weapon_dps = ship_info['weapon_dps']
		self.weapon_type = ship_info['weapon_type']
		self.drone_dps = ship_info['drone_dps']
		self.total_dps = ship_info['total_dps']
		self.salvo_period = ship_info['salvo_period']
		self.shield_k = ship_info['shield_k']
		self.armor_k = ship_info['armor_k']
		self.hull_k = ship_info['hull_k']
		self.total_hp = ship_info['total_hp']
		self.shield = self.shield_k * 1000
		self.armor = self.armor_k * 1000
		self.hull = self.hull_k * 1000
		self.shield_recharge = ship_info['shield_recharge']
		self.armor_recharge = ship_info['armor_recharge']
		self.total_recharge = ship_info['total_recharge']
		self.remote_shield_rep = ship_info['remote_shield_rep']
		self.remote_armor_rep = ship_info['remote_armor_rep']
		self.total_remote_rep = ship_info['total_remote_rep']
		self.neuts = ship_info['neuts']
		self.auras = ship_info['auras']
		self.webs_scrams = ship_info['webs_scrams']
		self.cap_transfers = ship_info['cap_transfers']
		self.sensor_boosters = ship_info['sensor_boosters']
		self.track_guide_disrupts = ship_info['track_guide_disrupts']
		self.ecm = ship_info['ecm']
		self.damps = ship_info['damps']
		self.painters = ship_info['painters']
		self.warp_fields = ship_info['warp_fields']
		self.evasion = ship_info['evasion']
		self.ship_score = ship_info['ship_score']
		self.is_alive = True

		self.battle_stats = [
			[self.volley, int(self.salvo_period*10), self.weapon_type, self.drone_dps*MECHANIC_DRONE_CYCLE_TIME],
			[self.shield, self.armor, self.hull],
			[self.shield_recharge*MECHANIC_SHIELD_CYCLE_TIME, self.armor_recharge*MECHANIC_ARMOR_CYCLE_TIME],
			[self.remote_shield_rep*MECHANIC_SHIELD_CYCLE_TIME, self.remote_armor_rep*MECHANIC_ARMOR_CYCLE_TIME],
			[self.neuts, self.auras, self.webs_scrams, self.cap_transfers, self.sensor_boosters, self.track_guide_disrupts, self.ecm, self.damps, self.painters, self.warp_fields]
		]

		self.abilities = []
		if self.auras != 0:
			self.abilities.append(A_AURA)
		if self.warp_fields != 0:
			self.abilities.append(A_WARP_FIELD)
		if self.cap_transfers != 0:
			self.abilities.append(A_CAP_TRANSFER)
		if self.ecm != 0:
			self.abilities.append(A_ECM)
		if self.webs_scrams != 0:
			self.abilities.append(A_TACKLE)
		if self.neuts != 0:
			self.abilities.append(A_NEUT)
		if self.sensor_boosters != 0:
			self.abilities.append(A_SENSOR_BOOSTER)
		if self.damps != 0:
			self.abilities.append(A_DAMP)
		if self.painters != 0:
			self.abilities.append(A_PAINTER)
		if self.track_guide_disrupts != 0:
			self.abilities.append(A_DISRUPTOR)

		self.image_path = 'ships/' + self.name.lower() + '.png'
		self.icon_surf, self.icon_rect = load_png(self.image_path, SHIP_ICON_SIZE)
		self.overlay_surf, self.overlay_rect = load_png(self.image_path, SHIP_ICON_OVERLAY_SIZE)
