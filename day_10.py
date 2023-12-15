from numpy import matrix, count_nonzero
from util import timeit

def pipes(sign: str, y: int, x: int) -> list:

	possible_directions = {
		 'S': [[-1,0],[0,1],[1,0],[0,-1]]
		,'|': [[-1,0],[1,0]]
		,'-': [[0,1],[0,-1]]
		,'L': [[-1,0],[0,1]]
		,'J': [[-1,0],[0,-1]]
		,'7': [[1,0],[0,-1]]
		,'F': [[1,0],[0,1]]
	}

	return [[a + b for a,b in zip(i, [y,x])] for i in possible_directions[sign]]

def left_right(sign: str, y:int, x:int, step_direction: list) -> list:

	sides = {
		 '|': {'L':[[0,-1]], 'R':[[0,1]]}
		,'-': {'L':[[1,0]], 'R':[[-1,0]]}
		,'L': {'L':[[0,-1],[1,-1],[1,0]], 'R':[]}
		,'J': {'L':[], 'R':[[1,0],[1,1],[0,1]]}
		,'7': {'L':[], 'R':[[0,1],[-1,1],[-1,0]]}
		,'F': {'L':[], 'R':[[-1,0],[-1,-1],[0,-1]]}
	}

	if sign in ['|','-','L','7']:

		if step_direction[0] + step_direction[1] == -1:
			return [[[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['L']], [[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['R']]]
		else:
			return [[[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['R']], [[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['L']]]

	else:
		if step_direction[0] == 0:
			return [[[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['R']], [[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['L']]]
		else:
			return [[[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['L']], [[a + b for a,b in zip(i, [y,x])] for i in sides[sign]['R']]]


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
def star(file_name: str, star_num: int) -> int:

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
	left, right = [], []

	while finish != 'S':

		sign = grid[y,x]
		prev = [y,x]
		y, x = next_move(grid,y,x,visited)
		finish = grid[y,x]
		visited.append([y,x])
		steps += 1
		step_direction = [b-a for a,b in zip(prev,[y,x])]

		if sign != 'S':
			l_dir, r_dir = left_right(sign, y, x, step_direction)

			left += l_dir
			right += r_dir

	new_left = [[i[0],i[1]] for i in set([(x[0],x[1]) for x in left])]
	new_right = [[i[0],i[1]] for i in set([(x[0],x[1]) for x in right])]

	if star_num == 2:

		n,m = grid.shape

		o_found = False
		for i,line in enumerate(grid):

			for j,v in enumerate(line.tolist()[0]):
				if [i,j] in visited:
					if j > 0 and not o_found:
						o_found = True
						if [i,j-1] in new_right:
							new_left, new_right = new_right, new_left
					break
				else:
					grid[i,j] = 'O'

			for j,v in enumerate(line.tolist()[0][::-1]):
				if [i,m-j-1] in visited:
					break
				else:
					grid[i,m-1-j] = 'O'

		for field in new_left:
			if field not in visited and -1 < field[0] < n and -1 < field[1] < m:
				if grid[field[0], field[1]] not in ['O','I'] :
					grid[field[0], field[1]] = 'O'

		for field in new_right:
			if field not in visited and -1 < field[0] < n and -1 < field[1] < m:
				if grid[field[0], field[1]] not in ['O','I'] :
					grid[field[0], field[1]] = 'I'




		for i,line in enumerate(grid):

			for j,v in enumerate(line.tolist()[0]):

				if [i,j] in visited:
					grid[i,j] = '#'

				elif grid[i,j] != 'O':

					not_o = True
					for x in [[-1,0],[-1,1],[-1,-1], [0,1],[0,-1], [1,0],[1,1],[1,-1]]:

						if grid[i+x[0], j+x[1]] =='I':
							grid[i,j] = 'I'
							not_o = False
							break

		return count_nonzero(grid == 'I')

	return steps/2

if __name__ == "__main__":

	print(f"Star 1: {star('day_10.txt',1)}")
	print(f"Star 2: {star('day_10.txt',2)}")