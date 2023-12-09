from util import timeit

def get_diff(oasis_line_inp: list) -> int:

	return [val - oasis_line_inp[n-1] for n, val in enumerate(oasis_line_inp) if n > 0]


def test_line(oasis_line_inp: list) -> bool:

	return (len(set(oasis_line_inp)) == 1 and max(oasis_line_inp) == 0)


def extrapolate(oasis_line_inp: list, history = False) -> int:

	line_test, generated_lines, next_line = test_line(oasis_line_inp), [oasis_line_inp], oasis_line_inp

	while not line_test:

		next_line = get_diff(next_line)
		generated_lines.insert(0,next_line)
		line_test = test_line(next_line)

	for n,line in enumerate(generated_lines):

		try:
			if history:
				generated_lines[n+1].insert(0,generated_lines[n+1][0] - line[0])

			else:	
				generated_lines[n+1].append(line[-1] + generated_lines[n+1][-1])
		except:
			break

	return generated_lines[-1][0] if history else generated_lines[-1][-1]


@timeit
def star(file_name: str, history = False) -> int:

	with open(file_name, 'r') as f:

		oasis_inp = [[int(i) for i in line.strip().split()] for line in f.readlines()]

	result = 0
	for oasis_line_inp in oasis_inp:
		result += extrapolate(oasis_line_inp, history)

	return result

if __name__ == "__main__":

	print(f"Star 1: {star('day_9.txt')}")
	print(f"Star 2: {star('day_9.txt', True)}")