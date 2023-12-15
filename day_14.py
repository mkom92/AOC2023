import numpy as np
from util import timeit
import re
import functools

def move(grid, y: int, x: int, direction: tuple) -> list:

	new_y, new_x = y, x
	n,m = grid.shape

	if direction[0] == 1 or direction[1] == 1:
		lim = 1
	else:
		lim = 0

	if direction[0] != 0:
		while n - lim > new_y > 0 - lim:

			if grid[new_y + direction[0], new_x] != '.':
				return [new_y, new_x]
			else:
				new_y += direction[0]
		
		return [new_y, new_x]

	else:
		while m - lim > new_x > 0 - lim:

			if grid[new_y, new_x + direction[1]] != '.':
				return [new_y, new_x]
			else:
				new_x += direction[1]
		
		return [new_y, new_x]


def adjust_grid(grid, direction: tuple):

	n,m = grid.shape
	rounded_rocks = list(zip(*np.where(grid == 'O')))

	if direction[0] == 1 or direction[1] == 1:

		rounded_rocks = rounded_rocks[::-1]

	for rock in rounded_rocks:

		y,x = rock

		if (direction[0] == -1 and y == 0) or (direction[1] == -1 and x == 0) or (direction[0] == 1 and y == n-1) or (direction[1] == 1 and x == m-1):
			next
		else:
			new_y, new_x = move(grid, y, x, direction)

			grid[y,x] = '.'
			grid[new_y,new_x] = 'O'


@timeit
def star_1(file_name: str) -> int:

	with open(file_name,'r') as f:

		grid_inp = [[i for i in line.strip()] for line in f.readlines()]

	grid = np.array(grid_inp)

	adjust_grid(grid,(-1,0))

	n,m = grid.shape
	total_load = 0
	for mult, row in enumerate(grid):

		total_load += (n-mult) * np.count_nonzero(row == 'O')

	return total_load


########################################
# NEW APPROACH
########################################


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

	while cycles < 1000000000: 

		grid = tilt_cycle(grid)

		cycles += 1

	# 	if cycles % 10000000 == 0:

	# 		print(cycles)


	return sum([row.count('O') * (len(grid) - n) for n,row in enumerate(grid)])

if __name__ == '__main__':

	# print(f"Star 1: {star_1('day_14.txt')}")
	print(f"Star 1 - attempt 2: {new_star_1('day_14.txt')}")
	print(f"Star 2 - attempt 2: {new_star_2('day_14.txt')}")