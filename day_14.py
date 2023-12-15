from util import timeit
import re
import functools

@functools.lru_cache(maxsize=None)
def move_rock(row: str, rock:int, direction: int):

	row_list = [i for i in row]

	if direction == 1:
		lim = 1
	else:
		lim = 0

	if (rock == 0 and direction == -1) or (rock == len(row_list) - 1 and direction == 1):

		return row
	else:
		row_list[rock] = '.'

		while len(row_list)  - lim > rock > 0 - lim:

			if row_list[rock + direction] != '.':

				row_list[rock] = 'O'

				return ''.join(row_list)

			else:
				rock += direction

		row_list[rock] = 'O'
		return ''.join(row_list)


@functools.lru_cache(maxsize=None)
def tilt(row:str, direction: int):

	rounded_rocks_p = re.compile('O')
	rounded_rocks = [int(o.start()) for o in rounded_rocks_p.finditer(row)]

	if direction == 1:
		rounded_rocks = rounded_rocks[::-1]

	for rock in rounded_rocks:
		row = move_rock(row, rock, direction)

	return row

@functools.lru_cache(maxsize=None)
def tilt_all(grid: tuple, direction: int) -> tuple:

	return tuple(tilt(row, direction) for row in grid)

@functools.lru_cache(maxsize=None)
def switch_grid(grid: tuple):

	return tuple(''.join(row) for row in list(zip(*grid)))

@timeit
def new_star_1(file_name: str) -> int:

	with open(file_name, 'r') as f:

		grid = tuple(line.strip() for line in f.readlines())

	grid = switch_grid(grid)
	grid = tilt_all(grid, -1)
	grid = switch_grid(grid)

	return sum([row.count('O') * (len(grid) - n) for n,row in enumerate(grid)])

@functools.lru_cache(maxsize=None)
def tilt_cycle(grid: tuple):

	grid = switch_grid(grid)
	grid = tilt_all(grid, -1)


	grid = switch_grid(grid)
	grid = tilt_all(grid, -1)


	grid = switch_grid(grid)
	grid = tilt_all(grid, 1)


	grid = switch_grid(grid)
	grid = tilt_all(grid, 1)

	return grid

@timeit
def new_star_2(file_name: str) -> int:

	with open(file_name, 'r') as f:

		grid = tuple(line.strip() for line in f.readlines())

	cycles = 0

	grids = {}

	while cycles < 1000: 

		cycles += 1

		try:
			grid = grids[grid][0]
			grids[grid][1].append(cycles)

		except:

			new_grid = tilt_cycle(grid)
			grids[grid] = [new_grid,[cycles]]
			grid = new_grid


	# 	if cycles % 10000000 == 0:

	# 		print(cycles)

	mult = 0
	for k,v in grids.items():

		if len(v[1]) > 1:
			mult += 1

		if mult == 2:
			cycle_start = v[1][0] - 1
			cycle_steps = v[1][1] - v[1][0] + 1

			loop_start = 1000000000 - cycle_start - 1
			last_step = loop_start % cycle_steps 

			mult += 1

		if mult > 2:

			if last_step == 0:
				grid = v[0]
				break
			else:
				last_step -= 1

	return sum([row.count('O') * (len(grid) - n) for n,row in enumerate(grid)])

if __name__ == '__main__':

	print(f"Star 1 - attempt 2: {new_star_1('day_14.txt')}")
	print(f"Star 2 - attempt 2: {new_star_2('day_14.txt')}")