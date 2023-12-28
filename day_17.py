from heapq import heappush, heappop
from util import timeit


def g_val(grid: tuple, point: tuple, prev_g: int) -> int:

	return prev_g + grid[point[0]][point[1]]


def neighbors(grid: tuple, point: tuple, direction: tuple, steps: int, min_moves: int, max_moves: int) -> list:

	directions = {
		 (-1,0): [(0,-1),(0,1),(-1,0)]
		,(1,0): [(0,-1),(0,1),(1,0)]
		,(0,-1): [(-1,0),(1,0),(0,-1)]
		,(0,1): [(-1,0),(1,0),(0,1)]
		,(0,0): [(-1,0),(1,0),(0,-1),(0,1)]
	}

	if min_moves > steps:
		if steps == 0:
			valid_adj = directions[direction]
		else:
			valid_adj = [directions[direction][-1]]
	else:
		valid_adj = directions[direction] if steps < max_moves else directions[direction][:2]

	neighbors = []

	for x in valid_adj:

		new_point = tuple(a+b for a,b in zip(point,x))

		if (0 <= new_point[0] <= len(grid) - 1) and (0 <= new_point[1] <= len(grid[0]) - 1):
			neighbors.append(new_point)

	return neighbors

@timeit
def star(file_name: str, min_moves: int, max_moves: int) -> int:

	with open(file_name,'r') as f:
		grid = tuple(tuple(int(i) for i in line.strip()) for line in f.readlines())

	start = (0,0)
	end = (len(grid)-1, len(grid[0])-1)

	g = g_val(grid, start, 0)

	visited = set()
	visited_val = {}

	pq = [(g,(start,(0,0),0),())]

	while pq:

		cost, point, path = heappop(pq)

		if point not in visited:

			visited.add(point)
			visited_val[point] = cost

			path += (point[0],)
			if point[0] == end and point[2] >= min_moves:
				break


			for next_point in neighbors(grid, point[0], point[1], point[2], min_moves, max_moves):

				new_cost = g_val(grid, next_point, cost)

				if next_point in visited:
					if visited_val[next_point] < new_cost:
						next

				new_direction = tuple(a - b for a,b in zip(next_point,point[0]))
				new_steps = point[2] + 1 if new_direction == point[1] else 1

				heappush(pq, (new_cost, (next_point, new_direction, new_steps), path))


	# for p in path:
	# 	print(p)

	return cost - g_val(grid,start,0)


if __name__ == '__main__':

	print(f"Star 1: {star('day_17.txt',0,3)}")
	print(f"Star 2: {star('day_17.txt',4,10)}")