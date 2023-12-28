import re

import functools
from util import timeit


@functools.lru_cache(maxsize=None)
def switch_layout(layout: tuple) -> tuple:

	return tuple(''.join(i) for i in list(zip(*layout)))


@functools.lru_cache(maxsize=None)
def turns_and_splits(row: str, direction: int, tilt: int) -> tuple:

	if tilt == 1:
		p = re.compile(r'(\||\\|/)')

	else:
		p = re.compile(r'(-|\\|/)')

	find_tas = [m.start() for m in p.finditer(row)]

	return find_tas if direction == 1 else find_tas[::-1]


@functools.lru_cache(maxsize=None)
def beam(layout: tuple, y: int, x: int, direction: int, tilt: int, visited: tuple) -> tuple:

	run = [(y,x,direction,tilt)]

	while len(run) > 0:

		new_run = []

		for inp in run:

			y,x,direction,tilt = inp

			if tilt == -1:
				row = switch_layout(layout)[y]
			else:
				row = layout[y]


			actual_yx = (y,x) if tilt == 1 else (x,y)
			turns = turns_and_splits(row, direction, tilt)

			if direction == 1:
				

				try:
					next_turn = min([i for i in turns if i >= x])
					# print("NT1: ",next_turn)
					visited += tuple((y,j,direction,tilt) for j in range(x, next_turn + 1)) if tilt == 1 else tuple((j,y,direction,tilt) for j in range(x, next_turn + 1))
					x = next_turn

				except:

					visited += tuple((y,j,direction,tilt) for j in range(x, len(row))) if tilt == 1 else tuple((j,y,direction,tilt) for j in range(x, len(row)))
					next

			else:

				try:
					next_turn = max([i for i in turns if i <= x])
					visited += tuple((y,j,direction,tilt) for j in range(next_turn, x + 1)) if tilt == 1 else tuple((j,y,direction,tilt) for j in range(next_turn, x + 1))
					x = next_turn

				except:

					visited += tuple((y,j,direction,tilt) for j in range(0, x + 1)) if tilt == 1 else tuple((j,y,direction,tilt) for j in range(0, x + 1))
					next

			if row[x] == '\\':

				tilt = -tilt
				y,x = x, y + direction
				actual_yx = (y,x) if tilt == 1 else (x,y)

				if (actual_yx[0],actual_yx[1],direction,tilt) not in visited and x >= 0 and x <= len(row) - 1:
					new_run.append((y,x,direction,tilt))

			elif row[x] == '/':

				tilt = -tilt
				direction = -direction
				y,x = x, y + direction
				actual_yx = (y,x) if tilt == 1 else (x,y)

				if (actual_yx[0],actual_yx[1],direction,tilt) not in visited and x >= 0 and x <= len(row) - 1:
					new_run.append((y,x,direction,tilt))
				

			elif (row[x] == '-' and tilt == -1) or (row[x] == '|' and tilt == 1):


				if tilt == 1:

					if y - 1 < 0:

						if (y + 1, x, 1, -1) not in visited:
							new_run.append((x, y + 1, 1, -1))

					elif y + 1 > len(row) - 1: 

						if (y - 1, x, 1, -1) not in visited:
							new_run.append((x, y - 1, -1, -1))

					else:

						if (y + 1, x, 1, -1) not in visited:
							new_run.append((x, y + 1, 1, -1))

						if (y - 1, x, -1, -1) not in visited:
							new_run.append((x, y - 1, -1, -1))

				else:

					if y - 1 < 0:

						if (x, y + 1, 1, 1) not in visited:
							new_run.append((x, y + 1, 1, 1))

					elif y + 1 > len(row) - 1: 

						if (x, y - 1, -1, 1) not in visited:
							new_run.append((x, y - 1, -1, 1))

					else:

						if (x, y + 1, 1, 1) not in visited:
							new_run.append((x, y + 1, 1, 1))

						if (x, y - 1, -1, 1) not in visited:
							new_run.append((x, y - 1, -1, 1))

		run = new_run
	return visited


@timeit
def star_1(file_name: str) -> int:

	with open(file_name, 'r') as f:

		layout = tuple(line.strip() for line in f.readlines())

	visited = ()
	visited += beam(layout,0,0,1,1,visited)
	energized = set(i[:2] for i in visited)

	return len(energized)


@timeit
def star_2(file_name: str) -> int:

	with open(file_name, 'r') as f:

		layout = tuple(line.strip() for line in f.readlines())


	max_energized = 0
	max_visited = ()

	from_left = [(y,0,1,1) for y in range(len(layout[0]))]
	from_right = [(y,len(layout[0])-1,-1,1) for y in range(len(layout[0]))]
	from_top = [(0,x,1,-1) for x in range(len(layout[0]))]
	from_bottom = [(len(layout[0])-1,x,-1,-1) for x in range(len(layout[0]))]

	start = from_left + from_right + from_top + from_bottom

	for inp in start:

		y,x,direction,tilt = inp

		if tilt == -1:
			y,x = x,y

		visited = ()
		visited += beam(layout,y,x,direction,tilt,visited)
		energized = set(i[:2] for i in visited)
		max_energized = max([len(energized),max_energized])
		
		if len(energized) == max_energized:
			max_visited = energized

	return max_energized


if __name__ == '__main__':

	print(f"Star 1: {star_1('day_16.txt')}")
	print(f"Star 2: {star_2('day_16.txt')}")