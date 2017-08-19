import random
from collections import defaultdict, Counter

def build_chain(words):
    """ build Markov chain from the list of words """
    chain = defaultdict(Counter)
    for idx, current_word in enumerate(words[:-1]):
        next_word = words[idx+1]
        chain[current_word].update([next_word])
    return chain

def generate(chain, length):
    """ generate new text given length from the chain """
    current_word = random.choice(list(chain.keys()))
    ret = [current_word]
    sentlen = length
    for i in range(sentlen):
        next_pairs = chain[current_word].items()
        next_words, weights = list(zip(*next_pairs))
        current_word = random.choices(next_words, weights)[0]
        if current_word not in ret:
            ret.append(current_word)
        if current_word == "end":
            sentlen = i

    return ' '.join(ret)

#спасибо Zagrebelin за скрипт