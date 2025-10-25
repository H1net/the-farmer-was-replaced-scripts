def create_maze():
	clear()
	plant(Entities.Bush)
	while get_entity_type()==Entities.Bush:
			substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
			if num_items(Items.Weird_Substance) > substance:
				use_item(Items.Weird_Substance, substance)
				return 1
			if can_harvest():
				harvest()
				plant(Entities.Bush)
			if num_items(Items.Fertilizer)==0:
				# I do not have trade unlocked
				#trade(Items.Fertilizer)
				return 0
			
			use_item(Items.Fertilizer)

# === Helper Functions ===

def turn_left(dir):
	if dir == North:
		return West
	if dir == West:
		return South
	if dir == South:
		return East
	if dir == East:
		return North

def turn_right(dir):
	if dir == North:
		return East
	if dir == East:
		return South
	if dir == South:
		return West
	if dir == West:
		return North

def try_move(dir):
	if can_move(dir):
		move(dir)
		return True
	return False

# === Strategy 1: Follow the left wall ===

def wall_follow_left():
	dir = North
	while True:
		left = turn_left(dir)
		if can_move(left):
			dir = left
			move(dir)
		elif can_move(dir):
			move(dir)
		else:
			dir = turn_right(dir)
		
		if get_entity_type() == Entities.Treasure:
			harvest()
			return 1


# === Strategy 2: Follow the right wall ===

def wall_follow_right():
	dir = North
	while True:
		right = turn_right(dir)
		if can_move(right):
			dir = right
			move(dir)
		elif can_move(dir):
			move(dir)
		else:
			dir = turn_left(dir)
		
		if get_entity_type() == Entities.Treasure:
			harvest()
			return 1

# === Strategy 3 (improved): Move towards the treasure with exploration memory ===

def move_towards_treasure():
	tiles = {}          # Dictionary: (x, y) -> info about walls and bifurcation
	path = []           # List containing the path taken
	bifurcations = []   # List containing bifurcations not yet fully explored

	while True:
		# If another drone already got the treasure, wait until the maze resets
		m = measure()
		if m == None:
			while measure() == None:
				return 1

		x = get_pos_x()
		y = get_pos_y()
		pos = (x, y)

		# Check if standing on the treasure
		if get_entity_type() == Entities.Treasure:
			harvest()
			return 1

		# Detect walls around the current tile
		walls = {
			North: not can_move(North),
			East:  not can_move(East),
			South: not can_move(South),
			West:  not can_move(West)
		}

		# If the tile hasn't been recorded yet
		if pos not in tiles:
			n_walls = 0

			if walls[North]:
				n_walls = n_walls + 1
			if walls[East]:
				n_walls = n_walls + 1
			if walls[South]:
				n_walls = n_walls + 1
			if walls[West]:
				n_walls = n_walls + 1

			is_bifurcation = n_walls < 3  # Less than 3 walls = bifurcation

			tiles[pos] = {
				"walls": walls,
				"visited": True,
				"bifurcation": is_bifurcation
			}

			if is_bifurcation:
				bifurcations.append(pos)

		# Mark the tile as visited
		tiles[pos]["visited"] = True

		if len(path) == 0 or path[-1] != pos:
			path.append(pos)

		# Find free directions not yet visited
		free_dirs = []
		for d in [North, East, South, West]:
			if not walls[d]:
				dx = 0
				dy = 0
				if d == North:
					dy = 1
				elif d == South:
					dy = -1
				elif d == East:
					dx = 1
				elif d == West:
					dx = -1

				next_pos = (x + dx, y + dy)

				if next_pos not in tiles or not tiles[next_pos]["visited"]:
					free_dirs.append(d)

		# Randomly choose one of the available directions
		if len(free_dirs) > 0:
			r = random()
			dir = free_dirs[0]

			if len(free_dirs) == 2:
				if r > 0.5:
					dir = free_dirs[1]
			elif len(free_dirs) == 3:
				if r < 0.33:
					dir = free_dirs[0]
				elif r < 0.66:
					dir = free_dirs[1]
				else:
					dir = free_dirs[2]
			elif len(free_dirs) == 4:
				if r < 0.25:
					dir = free_dirs[0]
				elif r < 0.5:
					dir = free_dirs[1]
				elif r < 0.75:
					dir = free_dirs[2]
				else:
					dir = free_dirs[3]

			move(dir)
			continue

		# No free paths — backtrack to the previous bifurcation
		if len(path) > 1:
			path.pop()
			prev = path[-1]
			px = prev[0]
			py = prev[1]

			# Physically move backwards
			if px > x:
				move(East)
			elif px < x:
				move(West)
			elif py > y:
				move(North)
			elif py < y:
				move(South)

			x = get_pos_x()
			y = get_pos_y()
			pos = (x, y)

			# If back at a bifurcation, try another unexplored direction
			if pos in tiles and tiles[pos]["bifurcation"]:
				walls = tiles[pos]["walls"]
				free_dirs = []

				for d in [North, East, South, West]:
					if not walls[d]:
						dx = 0
						dy = 0
						if d == North:
							dy = 1
						elif d == South:
							dy = -1
						elif d == East:
							dx = 1
						elif d == West:
							dx = -1
						next_pos = (x + dx, y + dy)

						if next_pos not in tiles or not tiles[next_pos]["visited"]:
							free_dirs.append(d)

				if len(free_dirs) > 0:
					r = random()
					dir = free_dirs[0]

					if len(free_dirs) == 2:
						if r > 0.5:
							dir = free_dirs[1]
					elif len(free_dirs) == 3:
						if r < 0.33:
							dir = free_dirs[0]
						elif r < 0.66:
							dir = free_dirs[1]
						else:
							dir = free_dirs[2]
					elif len(free_dirs) == 4:
						if r < 0.25:
							dir = free_dirs[0]
						elif r < 0.5:
							dir = free_dirs[1]
						elif r < 0.75:
							dir = free_dirs[2]
						else:
							dir = free_dirs[3]

					move(dir)

			
def treasure_hunt():
	
	# Uses wall-following strategies
	spawn_drone(wall_follow_left)
	spawn_drone(wall_follow_right)
	
	# Uses the bifurcation exploration strategy
	while num_drones() != max_drones():
		spawn_drone(move_towards_treasure)
		if get_entity_type() != Entities.Hedge:
			return 1

	move_towards_treasure()