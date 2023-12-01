from re import sub

# Star 1

def star_1(file_name) -> int:

	result = 0
	with open(file_name,'r') as f:
		for line in f.readlines():
			num_in_line = sub(r'[^\d]','',line.strip())
			result += int(num_in_line[0] + num_in_line[-1])
	return result

# Star 2

def star_2(file_name) -> int:

	result = 0

	spelled_digits = {
		'one': 'one1one'
		, 'two': 'two2two'
		, 'three': 'three3three'
		, 'four': 'four4four'
		, 'five': 'five5five'
		, 'six': 'six6six'
		, 'seven': 'seven7seven'
		, 'eight': 'eight8eight'
		, 'nine': 'nine9nine'
	}

	with open(file_name,'r') as f:
		for line in f.readlines():
			new_line = line.strip()
			for digit in spelled_digits.keys():
				if digit in new_line:
					new_line = sub(digit, spelled_digits[digit], new_line)

			num_in_line = sub(r'[^\d]','',new_line)
			result += int(num_in_line[0] + num_in_line[-1])

	return result

if __name__ == "__main__":

	print(f"""
	Star 1: {star_1('day_1.txt')}
	Star 2: {star_2('day_1.txt')}
	""")