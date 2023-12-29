import re
from util import timeit

@timeit
def star(file_name: str, star_num: int) -> int:

	dig_plan = []

	with open(file_name, 'r') as f:

		for line in f.readlines():

			p = re.match(r'(?P<direction>[A-Z]) (?P<cube_meters>[0-9]+) \((?P<colour>.+)\)',line.strip())

			dig_plan.append((p.group('direction'),int(p.group('cube_meters')),p.group('colour')))

	nodes = [(0,0)]
	elements = 0
	boundry_points = 0

	# Shoelace formula + pick's theory

	if star_num == 1:

		directions = {
			'U': (-1, 0),
			'D': ( 1, 0),
			'L': ( 0,-1),
			'R': ( 0, 1)
		}

		for dig in dig_plan:

			nodes += [tuple(a + b for a,b in zip(nodes[-1], tuple(x * dig[1] for x in directions[dig[0]])))]

			boundry_points += sum((list(abs(a - b) for a,b in zip(nodes[-1],nodes[-2]))))
			elements += nodes[-2][1] * nodes[-1][0] - nodes[-1][1] * nodes[-2][0]

	elif star_num == 2:

		directions = {
			'3': (-1, 0),
			'1': ( 1, 0),
			'2': ( 0,-1),
			'0': ( 0, 1)
		}

		for dig in dig_plan:

			direction = dig[2][-1]
			steps = int(dig[2].strip('#')[:-1], 16)

			nodes += [tuple(a + b for a,b in zip(nodes[-1], tuple(x * steps for x in directions[direction])))]
			
			boundry_points += sum((list(abs(a - b) for a,b in zip(nodes[-1],nodes[-2]))))
			elements += nodes[-2][1] * nodes[-1][0] - nodes[-1][1] * nodes[-2][0]

	return abs(elements)/2 + boundry_points/2 + 1


if __name__ == '__main__':
	print(f"Star 1: {star('day_18.txt', 1)}")
	print(f"Star 2: {star('day_18.txt', 2)}")