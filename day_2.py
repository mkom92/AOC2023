def star(file_name, star_num) -> int:

	# Star 1 

	limits = {
		'red': 12
		, 'green': 13
		, 'blue': 14
	}

	ids = 0

	# Start 2

	powers = 0

	with open(file_name, 'r') as f:

		for line in f.readlines():

			info = line.strip().split(':')
			game_id = int(info[0].split(' ')[1])


			game_is_valid = True 


			colours = {
				'red': 0
				, 'green': 0
				, 'blue': 0
			}

			for cubes in info[1].replace(';',',').split(','):

				colour = cubes.strip().split(' ')[1].strip()
				value = int(cubes.strip().split(' ')[0].strip())

				if limits[colour] < value:
					game_is_valid = False

				colours[colour] = max(colours[colour], value)


			if game_is_valid:

				ids += game_id

			power = 1
			for col in colours.values():
				power *= col

			powers += power

		if star_num == 1:
			return ids
		else:
			return powers

if __name__ == '__main__':

	print(f"Star 1: {star('day_2.txt', 1)}")
	print(f"Star 2: {star('day_2.txt', 2)}")