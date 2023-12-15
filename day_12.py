import functools
import re
from util import timeit

@functools.lru_cache(maxsize=None)
def decoding(instruction: str, parts_map: tuple):

	if parts_map == ():

		if instruction.count('#') == 0:

			return 1

		else:

			return 0

	elif instruction == '':

		return 0 

	elif instruction.count('#') + instruction.count('?') < sum(parts_map):

		return 0

	char = instruction[0]
	dmg_group = parts_map[0]


	# def functions for # 

	def hashtag(instruction: str, parts_map: tuple):

		dmg_group = parts_map[0]

		test_dmg = '#'*dmg_group
		test_vs = re.sub(r'\?','#',instruction[:dmg_group])

		try:
			next_char_test = instruction[dmg_group] != '#'
			is_end = False
		except:
			is_end = True


		if is_end:
			return 1

		else:

			if test_vs == test_dmg and next_char_test:

				return decoding(instruction[dmg_group+1:], parts_map[1:])

			else:

				return 0


	if char == '#':

		return hashtag(instruction, parts_map)

	elif char == '.':

		return decoding(instruction[1:], parts_map)

	elif char == '?':

		return hashtag(instruction, parts_map) + decoding(instruction[1:], parts_map)


@timeit
def star_1(file_name: str) -> int:


	with open(file_name, 'r') as f:

		inp = [[i for i in line.strip().split(' ')] for line in f.readlines()]
	
	total_val = 0
	for i in inp:

		val = 0
		instruction, parts_map = i[0], tuple(int(j) for j in i[1].split(','))

		val = decoding(instruction, parts_map)
		total_val += val

	return total_val


@timeit
def star_2(file_name: str) -> int:


	with open(file_name, 'r') as f:

		inp = [[i for i in line.strip().split(' ')] for line in f.readlines()]
	
	total_val = 0
	for i in inp:

		val = 0
		instruction, parts_map = '?'.join([i[0] for _ in range(5)]), tuple(int(j) for j in i[1].split(',')) * 5
		val = decoding(instruction, parts_map)
		total_val += val

	return total_val



if __name__ == "__main__":
	print(f"Star 1: {star_1('day_12.txt')}")
	print(f"Star 2: {star_2('day_12.txt')}")