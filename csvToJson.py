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
		ship['race'] = row['race']
		ship['ship_class'] = row['ship_class']
		ship['attack'] = int(row['attack'])
		ship['tier'] = int(row['tier'])
		ship['shields'] = int(row['shields'])
		ship['armor'] = int(row['armor'])
		ship['hull'] = int(row['hull'])
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
		data['commanders'].append(commander)

with open(jsonFileName, 'w') as jsonFile:
	jsonFile.write(json.dumps(data))