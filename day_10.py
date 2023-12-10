from numpy import matrix
from util import timeit

def pipes(sign: str, y: int, x: int) -> list:

	possible_directions = {
		 'S': [[-1,0],[1,0],[0,-1],[0,1]]
		,'|': [[-1,0],[1,0]]
		,'-': [[0,1],[0,-1]]
		,'L': [[-1,0],[0,1]]
		,'J': [[-1,0],[0,-1]]
		,'7': [[1,0],[0,-1]]
		,'F': [[1,0],[0,1]]
	}

	return [[a + b for a,b in zip(i, [y,x])] for i in possible_directions[sign]]


def next_move(grid:list, y: int, x: int, visited: list) -> list:

	# Check valid outputs
	possible_directions = pipes(grid[y,x], y, x)

	for field in possible_directions:

		try:
			current_symbol = grid[field[0],field[1]]
		except:
			current_symbol = 'N'

		if current_symbol == 'S' and len(visited) > 2:
			return field

		elif field in visited:
			next
		
		else:

			try:
				next_element = pipes(grid[field[0],field[1]], field[0], field[1])

				if [y,x] in next_element:
					return field

			except:
				next

@timeit
def star(file_name: str) -> int:

	grid = []
	y, x = -1, -1

	with open(file_name, 'r') as f:

		for n, line in enumerate(f.readlines()):

			new_line = [val for val in line.strip()]
			grid.append(new_line)

			if y > -1:
				next 
			elif 'S' in new_line:
				y, x = n, new_line.index('S')

	grid = matrix(grid)
	finish = 'Z'
	steps = 0
	visited = [[y,x]]

	while finish != 'S':

		y, x = next_move(grid,y,x,visited)
		finish = grid[y,x]
		visited.append([y,x])
		steps += 1

	# for field in visited:
	# 	grid[field[0],field[1]] = 'X'
	# print(grid)


	return steps/2

if __name__ == "__main__":

	print(f"Star 1: {star('day_10.txt')}")