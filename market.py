try:
    import sys
    import random
    import json
    import collections
    from constants import *
    from ship import *
    from pool import *
except(ImportError, err):
    print('Failed to load module: %s' % (err))
    sys.exit(2)

class Market():
	def __init__(self, pool):
		self.pool = pool
		self.tier = 0
		self.ships = []
		self.hold = False
		self.reinit()

	def recycle_ships(self):
		while self.ships:
			self.pool.return_ship(self.ships.pop())
		self.refill_ships()

	def toggle_hold_ships(self):
		self.hold = not self.hold

	def upgrade_tier(self):
		self.tier += 1

	def buy_ship(self, s):
		self.ships.remove(s)
		return s

	def sell_ship(self, s):
		self.pool.return_ship(s)

	def refill_ships(self):
		while len(self.ships) < N_MARKET_SHIPS_PER_TIER[self.tier]:
			self.ships.append(self.pool.get_ship(self.tier))

	def reinit(self):
		if not self.hold:
			self.recycle_ships()
		else:
			self.refill_ships()
		self.hold = False

