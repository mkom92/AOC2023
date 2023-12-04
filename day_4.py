import re

def matches(elf_numbers_list, winning_numbers_list) -> list:

	star_1 = 0
	star_2 = 0

	for number in elf_numbers_list:

		if number in winning_numbers_list:

			if star_1 == 0:

				star_1 += 1
				star_2 += 1

			else:

				star_1 *= 2
				star_2 += 1

	return [star_1, star_2]


def add_occurence(dict, card, add_coeficient):

	try:
		dict[card] += 1
	except:
		dict[card] = 1

	return dict


def star(file_name, star_num) -> int:

	result = 0

	if star_num == 2:

		card_occurrences = {}

	with open(file_name, 'r') as f:

		for line in f.readlines():

			m = re.match(r"Card(\s+)(?P<card>\d+)\: (?P<winning_numbers>.+) \| (?P<elf_numbers>.+)",line.strip())
			card, winning_numbers, elf_numbers = int(m.group('card')), m.group('winning_numbers'), m.group('elf_numbers')

			winning_numbers_list = [int(i) for i in winning_numbers.split()]
			elf_numbers_list = [int(i) for i in elf_numbers.split()]


			if star_num == 1:

				card_result = matches(elf_numbers_list, winning_numbers_list)[0]

				result += card_result

			elif star_num == 2:

				matching_numbers = matches(elf_numbers_list, winning_numbers_list)[1]

				# card_occurrences = add_occurence(card_occurrences, card)

				try:
					card_occurrences[card] += 1
				except:
					card_occurrences[card] = 1

				for i in range(matching_numbers):

					# card_occurrences = add_occurence(card_occurrences, int(card) + i + 1)

					try:
						card_occurrences[card + i + 1] += 1 * card_occurrences[card]
					except:
						card_occurrences[card + i + 1] = 1 * card_occurrences[card]


	if star_num == 2:

		result = sum(card_occurrences.values())

	return result

if __name__ == '__main__':

	print(f"Star 1: {star('day_4.txt', 1)}")
	print(f"Star 1: {star('day_4.txt', 2)}")