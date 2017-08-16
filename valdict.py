import random

class valdisdict(dict):
	def __init__(self, iterable=None):
		super(valdisdict, self).__init__()
		self.types = 0
		self.tokens = 0
		if iterable:
			self.update(iterable)
	def update(self, iterable):
		for wrd in iterable:
			if wrd in self:
				self[wrd] += 1
				self.types += 1
			else:
				self[wrd] = 1
				self.types += 1
				self.tokens += 1
	def count(self):
		if wrd in self:
			return self[wrd]
		return 0
	def return_random_word(self):
		random_key = random.sample(self, 1)
		return random_key[0]
	def return_weighted_random_word(self):
		random_int = random.randint(0, self.tokens)
		index = 0
		list_of_keys = self.keys()
		for i in range(0, self.types):
			index += self[list(list_of_keys)[i]]
			if index > random_int:
				return list(list_of_keys)[i]
			else:
				return list(list_of_keys)[i]