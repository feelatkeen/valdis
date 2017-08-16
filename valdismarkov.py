from valdict import valdisdict
import random
from collections import deque
import re

def make_markov_model(data):
	markov_model = dict()
	for i in range(0, len(data)-1):
		if data[i] in markov_model:
			markov_model[data[i]].update([data[i+1]])
		else:
			print(data[i+1])
			markov_model[data[i]] = valdisdict([data[i+1]])
	return markov_model

def make_higher_order_markov_model(order,data):
	markov_model = dict()

	for i in range(0, len(data)-order):
		window = tuple(data[i: i+order])
		if window in markov_model:
			markov_model[window].update([data[i+order]])
		else:
			print(data[i+order])
			markov_model[window] = valdisdict(iterable=[data[i+order]])
	return markov_model

def generate_random_start(model):
	return random.choice(list(model.keys()))
def generate_random_sentence(length, markov_model):
	current_wrd = generate_random_start(markov_model)
	print(markov_model[current_wrd])
	sentence = [current_wrd]
	for i in range(0, length):
		current_dictogram = markov_model[current_wrd]
		random_weighted_word = current_dictogram.return_weighted_random_word()
		current_wrd = random_weighted_word
		if current_wrd not in sentence:
			sentence.append(current_wrd)
	sentence[0] = sentence[0].capitalize()
	return ' '.join(sentence)
	return sentence
