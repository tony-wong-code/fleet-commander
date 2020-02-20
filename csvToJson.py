try:
	import os
	import sys
	import csv
	import json
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

csvFileName = 'ships.csv'
jsonFileName = 'ships.json'

data = dict()
path = os.path.join('', csvFileName)
data['ships'] = list()
with open(path) as csvFile:
	csvReader = csv.DictReader(csvFile)
	for row in csvReader:
		ship = dict()
		ship['name'] = row['name']
		ship['race'] = int(row['race'])
		ship['size'] = int(row['size'])
		ship['role'] = row['role']
		ship['tier'] = int(row['tier'])
		ship['volley'] = float(row['volley'])
		ship['weapon_dps'] = float(row['weapon_dps'])
		ship['weapon_type'] = int(row['weapon_type'])
		ship['drone_dps'] = float(row['drone_dps'])
		ship['total_dps'] = float(row['total_dps'])
		ship['salvo_period'] = float(row['salvo_period'])
		ship['shield_k'] = float(row['shield_k'])
		ship['armor_k'] = float(row['armor_k'])
		ship['hull_k'] = float(row['hull_k'])
		ship['total_hp'] = float(row['total_hp'])
		ship['shield_recharge'] = float(row['shield_recharge'])
		ship['armor_recharge'] = float(row['armor_recharge'])
		ship['total_recharge'] = float(row['total_recharge'])
		ship['remote_shield_rep'] = float(row['remote_shield_rep'])
		ship['remote_armor_rep'] = float(row['remote_armor_rep'])
		ship['total_remote_rep'] = float(row['total_remote_rep'])
		ship['neuts'] = int(row['neuts'])
		ship['auras'] = int(row['auras'])
		ship['webs_scrams'] = int(row['webs_scrams'])
		ship['cap_transfers'] = int(row['cap_transfers'])
		ship['sensor_boosters'] = int(row['sensor_boosters'])
		ship['track_guide_disrupts'] = int(row['track_guide_disrupts'])
		ship['ecm'] = int(row['ecm'])
		ship['damps'] = int(row['damps'])
		ship['painters'] = int(row['painters'])
		ship['warp_fields'] = int(row['warp_fields'])
		ship['evasion'] = float(row['evasion'])
		ship['ship_score'] = float(row['ship_score'])
		data['ships'].append(ship)
		
with open(jsonFileName, 'w') as jsonFile:
	jsonFile.write(json.dumps(data))

csvFileName = 'commanders.csv'
jsonFileName = 'commanders.json'

data = dict()
path = os.path.join('', csvFileName)
data['commanders'] = list()
with open(path) as csvFile:
	csvReader = csv.DictReader(csvFile)
	for row in csvReader:
		commander = dict()
		commander['name'] = row['name']
		commander['race'] = row['race']
		commander['bloodline'] = row['bloodline']
		commander['image'] = row['image']
		commander['bonus'] = row['bonus']
		commander['penalty'] = row['penalty']
		commander['quick_upgrade_chance'] = row['quick_upgrade_chance']
		commander['slow_upgrade_chance'] = row['slow_upgrade_chance']
		data['commanders'].append(commander)

with open(jsonFileName, 'w') as jsonFile:
	jsonFile.write(json.dumps(data))