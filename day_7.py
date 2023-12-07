import pandas as pd
from collections import Counter
from util import timeit

def card_val(card, wild_enabled = False):

	card_map = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

	if wild_enabled:
		card_map['J'] = 1

	try:
		return [int(card), chr(96+int(card))]
	except:
		return [card_map[card], chr(96+card_map[card])]


def poker(hand, wild_enabled = False):

	cards = (card_val(i, wild_enabled)[0] for i in hand)
	hand_transcribed = ''.join(card_val(i, wild_enabled)[1] for i in hand)

	values = Counter(cards)
	top_occurrences = values.most_common()[0][1]
	top_occurring = [val[0] for val in values.most_common() if val[1] == top_occurrences]
	if 1 < top_occurrences < 5:
		next_higher = max([val[1] for val in values.most_common() if val[1] != top_occurrences])
	len_v = len(values)	

	ranks = {
		'1,5': 7
		, '2,4': 6
		, '2,3': 5
		, '3,3': 4
		, '3,2': 3
		, '4,2': 2
		, '5,1': 1
	}

	if wild_enabled:

		wildcard_occurrences = values[1]

		if wildcard_occurrences > 0:

			if wildcard_occurrences == top_occurrences:

				if top_occurrences == 5:

					return [7, hand_transcribed]

				elif len(top_occurring) > 1:

					return [ranks[','.join([str(len_v - 1), str(top_occurrences + wildcard_occurrences)])], hand_transcribed]

				else:

					return [ranks[','.join([str(len_v - 1), str(next_higher + wildcard_occurrences)])], hand_transcribed]

			else:

				return [ranks[','.join([str(len_v - 1), str(top_occurrences + wildcard_occurrences)])], hand_transcribed]

	

	return [ranks[','.join([str(len_v), str(top_occurrences)])], hand_transcribed]


@timeit
def star(file_name, wild_enabled = False) -> int:

	with open(file_name, 'r') as f:

		hands = [[i.strip() for i in line.strip().split()] for line in f.readlines()]

	powers = {'hand': [], 'value': [], 'power': [], 'hand_transcribed': []}
	
	for hand in hands:

		hand_power = poker(hand[0], wild_enabled)

		powers['hand'].append(hand[0])
		powers['value'].append(int(hand[1]))
		powers['power'].append(hand_power[0])
		powers['hand_transcribed'].append(hand_power[1])


	powers_df = pd.DataFrame(powers).sort_values(by = ['power','hand_transcribed']).reset_index().drop(['index'], axis = 1).reset_index()
	powers_df['total_value'] = powers_df[['index','value']].apply(lambda x: (x['index'] + 1) * x['value'], axis = 1)

	return sum(powers_df['total_value'])


if __name__ == "__main__":

	print(f"Star 1: {star('day_7.txt')}")
	print(f"Star 2: {star('day_7.txt', True)}")