try:
    import sys
    import random
    import json
    import collections
    from constants import *
    from ship import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Pool():
	def __init__(self):
		with open('ships.json') as json_file:
			data = json.load(json_file)
			
		ships = data["ships"]
		self.ship_dict = collections.defaultdict()
		self.available = [set() for _ in range(N_TIERS)]
		i = 0
		for s in ships:
			for j in range(N_SHIP_COPIES_PER_TIER[s['tier']]):
				self.ship_dict[i+j] = Ship(s)
				self.available[s['tier']].add(i+j)
			i += N_SHIP_COPIES_PER_TIER[s['tier']]
		for t in range(1, N_TIERS):
			self.available[t] = self.available[t-1].union(self.available[t])

	def return_ship(self, s):
		for t in range(self.ship_dict[s].tier, N_TIERS):
			self.available[t].add(s)

	def get_ship(self, tier):
		res = random.choice(list(self.available[tier]))
		for t in range(tier + 1):
			if res in self.available[t]:
				self.available[t].remove(res)
		return res