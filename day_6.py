from math import prod, sqrt, floor
from util import timeit


def ways_to_win(t, d) -> int:

	ways_to_win = []

	for n, T in enumerate(t):

		sub_result = 0

		for x in range(int(T)):

			y = (x * (int(T) - x))

			if y > int(d[n]):

				sub_result += 1

		ways_to_win.append(sub_result)

	return prod(ways_to_win)


@timeit
def star(file_name, star_num) -> int:

	with open(file_name, 'r') as f:

		inp = [[i.strip() for i in line.split()][1:] for line in f.readlines()]


	if star_num == 1:

		return ways_to_win(inp[0], inp[1])

	elif star_num == 2:

		inp_s2 = [[int(''.join(i))] for i in inp]

		return ways_to_win(inp_s2[0], inp_s2[1])

@timeit
def star_2_math(file_name) -> int:

	with open(file_name, 'r') as f:

		T, y = [int(''.join([i.strip() for i in line.split(':')[1]])) for line in f.readlines()]

	# y < x * (T - x) --> -x^2 + Tx - y > 0

	delta = sqrt(T**2 - (4*(-1)*(-y)))
	x1, x2 = (-T - delta)/2, (-T + delta)/2

	return floor(x2 - x1)

if __name__ == '__main__':

	print(f"Star 1: {star('day_6.txt',1)}")
	print(f"Star 2: {star('day_6.txt',2)}")

	print(f"Star 2 (math solution): {star_2_math('day_6.txt')}")