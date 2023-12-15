import numpy as np
from util import timeit

# def compare_reflection(pattern, smudge: bool) -> list:

# 	yy,xx = pattern.shape
# 	for n, row in enumerate(pattern):

# 		try:
# 			if np.count_nonzero(row == pattern[n+1]) >= len(row) - bool(smudge):

# 				test_rows = min([yy - n - 2, n])

# 				if np.count_nonzero(pattern[n-test_rows:n+1] == np.flip(pattern[n+1:n+test_rows+2],0)) >= np.count_nonzero(pattern[n-test_rows:n+1]) - bool(smudge):

# 					return [True, n+1]
# 		except:
# 			next

# 	return [False, 0]


def compare_reflection(pattern, smudge: bool, prev_val: int) -> list:

	yy,xx = pattern.shape
	for n, row in enumerate(pattern):

		try:
			if np.count_nonzero(row == pattern[n+1]) >= len(row) - bool(smudge) and n != prev_val - 1:

				test_rows = min([yy - n - 2, n])

				if np.count_nonzero(pattern[n-test_rows:n+1] == np.flip(pattern[n+1:n+test_rows+2],0)) >= np.count_nonzero(pattern[n-test_rows:n+1]) - bool(smudge):

					return [True, n+1]
		except:
			next

	return [False, 0]


@timeit
def star(file_name: str, smudge: bool) -> int:

	with open(file_name, 'r') as f:
		patterns = [[[j for j in i] for i in part.split('\n')] for part in f.read().split('\n\n')]

	total_pattern_val = 0
	for k,pattern in enumerate(patterns):

		m = np.array(pattern)

		# mirrored, reflections = compare_reflection(m, smudge)

		# if mirrored:
		# 	total_pattern_val += reflections * 100

		# 	print(f"{k}: {reflections}")

		# else:
		# 	mirrored, reflections = compare_reflection(np.transpose(m), smudge)
		# 	total_pattern_val += reflections

		# 	print(f"{k}: {reflections}")

		if not smudge:

			mirrored, reflections = compare_reflection(m, smudge, 99)

			if mirrored:
				total_pattern_val += reflections * 100

			else:
				mirrored, reflections = compare_reflection(np.transpose(m), smudge, 99)
				total_pattern_val += reflections

		else:

			prev_mirrored, prev_reflections_y = compare_reflection(m, False, 99)
			prev_mirrored, prev_reflections_x = compare_reflection(np.transpose(m), False, 99)


			if prev_mirrored:
				val = prev_reflections_x
			else: 
				val = prev_reflections_y * 100

			mirrored, reflections = compare_reflection(m, smudge, prev_reflections_y)

			if mirrored:
				total_pattern_val += reflections * 100

			else:
				mirrored, reflections = compare_reflection(np.transpose(m), smudge, prev_reflections_x)
				if mirrored:
					total_pattern_val += reflections

				else:
					total_pattern_val += val


	return total_pattern_val

if __name__ == "__main__":

	print(f"Start 1: {star('day_13.txt', False)}")
	print(f"Start 2: {star('day_13.txt', True)}")