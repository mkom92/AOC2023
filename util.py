from functools import wraps
from time import perf_counter
from heapq import heappop, heappush


def timeit(func):
    
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()

        print(f'Total time: {(end_time - start_time):.4f} seconds')
        return result
    return timeit_wrapper


def neighbours(point,grid,dire):

    n,m = grid.shape
    xn,ym = point
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    adjacent = []

    for d in directions:

        x,y = point[0]+d[0], point[1]+d[1]


        if 0 <= x < n and 0 <= y < m:

            if dire == 'up' and grid[x][y] - grid[xn][ym] < 2:

                adjacent.append((x,y))

            elif dire == 'down' and grid[xn][ym] - grid[x][y] < 2:

                adjacent.append((x,y))

    return adjacent 


def djikstra(start,grid,dire,end = (99,99), end_val = 99):

    visited = set()
    pq = [(0,start,())]
    last_1 = 0

    while pq:

        steps, point, path = heappop(pq)

        if point not in visited:

            visited.add(point)
            path = (point,path)

            if end_val == 99:
                if point == end: 
                    print(steps)
                    break

            else:
                n,m = point
                if grid[n][m] == end_val:
                    print(steps)
                    break

            for point2 in neighbours(point,grid,dire):

                if point2 not in visited: 
                    
                    heappush(pq, (steps+1, point2, path))