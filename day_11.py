import numpy as np
from itertools import combinations
from util import timeit

def adjacent(grid, point) -> list:

	n,m = grid.shape
	adj = [[-1,0],[1,0],[0,-1],[0,1]]
	valid = []

	for a in adj:
		y,x = point[0] + a[0], point[1] + a[1]
		

		if -1 < y < n and -1 < x < m:
			valid.append((y,x))

	return valid

@timeit
def star(file_name: str, empty_multiplier: int) -> int:

	grid = []
	empty_rows, empty_columns = [], []

	with open(file_name, 'r') as f:

		for n,line in enumerate(f.readlines()):

			new_line = [i for i in line.strip()]
			grid.append(new_line)

			if '#' not in new_line:
				empty_rows.append(n)

	grid = np.array(grid)

	for n,line in enumerate(grid.transpose()):

		if '#' not in line:
			empty_columns.append(n)

	galaxies = list(zip(*np.where(grid == '#')))
	total_len = 0

	for i in combinations(galaxies,2):

		yy = [i[0][0], i[1][0]]
		xx = [i[0][1], i[1][1]]

		total_len += (abs(i[0][0] - i[1][0])+abs(i[0][1] - i[1][1]))
		total_len += len([j for j in empty_rows if min(yy) < j < max(yy)]) * (empty_multiplier - 1)
		total_len += len([j for j in empty_columns if min(xx) < j < max(xx)]) * (empty_multiplier - 1)

	return total_len

if __name__ == "__main__":

	print(f"Star 1: {star('day_11.txt',2)}")
	print(f"Star 2: {star('day_11.txt',1000000)}")