from numpy import prod


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


def star(file_name, star_num) -> int:

	with open(file_name, 'r') as f:

		inp = [[i.strip() for i in line.split()][1:] for line in f.readlines()]


	if star_num == 1:

		return ways_to_win(inp[0], inp[1])

	elif star_num == 2:

		inp_s2 = [[int(''.join(i))] for i in inp]

		return ways_to_win(inp_s2[0], inp_s2[1])


if __name__ == '__main__':

	print(f"Star 1: {star('day_6.txt',1)}")
	print(f"Star 2: {star('day_6.txt',2)}")