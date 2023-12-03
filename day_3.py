import re

def star(file_name, star_num) -> int:

	# Read the file and collect position data of all the numbers and signs


	numbers_re = re.compile('[\d]*')
	signs_re = re.compile('[^\.^\d]')

	numbers_pos = []
	signs_pos = []

	gears = []

	with open(file_name, 'r') as f:

		for n, line in enumerate(f.readlines()):

			for m in numbers_re.finditer(line.strip()):

				if m.group():
					numbers_pos.append([n,m.start() - 1, m.start() + len(str(m.group())), m.group()])

			for m in signs_re.finditer(line.strip()):

				if m.group() == '*' and star_num == 2:

					gears.append([n, m.start(), m.group()])

				elif star_num == 1:

					signs_pos.append([n, m.start(), m.group()])

	# Result value

	sum_of_parts = 0

	# Star 1

	if star_num == 1:

		# Check whether the parts are valid and sum up their values

		for number in numbers_pos:

			is_valid = False

			for sign in signs_pos:

				if sign[0] - 1 <= number[0] and number[0] <= sign[0] + 1 and number[1] <= sign[1] and sign[1] <= number[2]:

					is_valid = True

					break

			if is_valid:

				sum_of_parts += int(number[3])


	else:

		# Find all the parts adjacent to the gears, multiply the values and sum them up

		for gear in gears:

			parts_ct = 0
			parts = []

			for number in numbers_pos:

				if gear[0] - 1 <= number[0] and number[0] <= gear[0] + 1 and number[1] <= gear[1] and gear[1] <= number[2]:

					parts_ct += 1
					parts.append(int(number[3]))

			if parts_ct == 2:

				sum_of_parts += parts[0] * parts[1]


	return sum_of_parts

if __name__ == '__main__':

	print(f"Star 1: {star('day_3.txt',1)}")
	print(f"Star 2: {star('day_3.txt',2)}")
