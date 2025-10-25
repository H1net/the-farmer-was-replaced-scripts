# ===== MAIN FARMING SCRIPT =====
# # Import configuration and helper modules
# import config
# # import plant_logic
# import maze
# import movement

# # from plant_logic import create_maze, treasure_hunt

# times = 30

# #for i in range(times):
	
# 	#create_maze()
# 	#treasure_hunt()

# while True:
# 	if maze.create_maze():
# 		if maze.treasure_hunt():
# 			continue

# set_world_size(8)


# set_world_size(16)
# set_world_size(32)
clear()

ROWS = get_world_size()
COLS = get_world_size()

ND = 1

T = {East: West, West: East, North: South, South: North}
def invert(dir):
	return T[dir]

def go_to(x, y):
	op1 = abs(x - get_pos_x())
	op2 = COLS - op1
		
	if x < get_pos_x():
		dir = West
	else:
		dir = East
		
	if op1 > op2:
		dir = invert(dir)

	steps = min(op1, op2)
	
	for _ in range(steps):
		move(dir)
		
	op1 = abs(y - get_pos_y())
	op2 = ROWS - op1
		
	if y < get_pos_y():
		dir = South
	else:
		dir = North
		
	if op1 > op2:
		dir = invert(dir)

	steps = min(op1, op2)
	
	for _ in range(steps):
		move(dir)
		
def rev(R):
	R = list(R)
	for i in range(len(R) / 2):
		R[i], R[len(R)-i-1] = R[len(R)-i-1], R[i]
	return R
		
def walk(callback, mover=go_to, drone=None):
	srow = (ROWS / ND) * (drone)
	erow = srow + (ROWS / ND)
		
	for i in range(srow, erow):
		R = list(range(COLS))
		if i % 2 != 0:
			rev(R)
		for j in R:
			mover(j, i)
			callback()

def pplant(type):
	harvest()
	if get_entity_type() == type:
		return
	if type in [Entities.Carrot, Entities.Sunflower, Entities.Pumpkin, Entities.Cactus]:
		expected_ground = Grounds.Soil
	else:
		expected_ground = Grounds.Grassland
		
	if get_ground_type() != expected_ground:
		till()
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
	if num_items(Items.water) > 0 and get_water() < 0.5:
		use_item(Items.Water)
	plant(type)

def handle_companion(exclude_ = None, entity = None): 
	if get_companion() == None:
		return None
	if exclude_ == None:
		exclude_ = []
	c = get_companion() 
	
	if c == None:	
		return None
	
	comp_type, (x, y) = c
	
	if y < get_pos_y():
		return None
	
	go_to(x, y)
	#if get_entity_type() == entity:
	#	return None
	pplant(comp_type)
	return x, y

def _dummy_exclude():
	return False

def _row_plant(row, entity, fix_only=False, exclude=None):
	def _inner():
		for col in range(COLS):
			go_to(col, row)
			
			if exclude != None and exclude():
				continue
			
			if fix_only and can_harvest() and get_entity_type() == entity:
				continue
				
			harvest()
			pplant(entity)
			handle_companion(None, entity)
		
	return _inner
	 

def _row_harvest(row, entity=None, replant=False):
	def _inner():
		for col in range(COLS):
			go_to(col, row)
			if entity != None and get_entity_type() != entity:
				continue
			harvest()
			if replant:
				pplant(entity)
	return _inner

def _cells_in_row(row):
	res = []
	for col in range(COLS):
		res.append((row, col))
	return res
	
def _plant_all(entity, fix_only=False, exclude=None):
	go_to(0, 0)
	for i in range(ROWS):
		if not spawn_drone(_row_plant(i, entity, fix_only, exclude)):
			_row_plant(i, entity, fix_only, exclude)()
		move(North)
			
def _harvest_all(entity=None, replant=False):
	go_to(0, 0)
	for i in range(ROWS):
		if not spawn_drone(_row_harvest(i, entity, replant)):
			_row_harvest(i, entity, replant)()
		move(North)
			
def _all_measurements(D):
	def _row_walk(row, D):
		def _inner():
			global D
			for (r, c) in _cells_in_row(row):
				go_to(c, r)
				D.append((measure(), c, r))
		return _inner
	
	for i in range(ROWS):
		if not spawn_drone(_row_walk(i, D)):
			_row_walk(i, D)()

def sleep(time):
	start = get_time()
	while get_time() - start < time:
		pass

def grass():
	_plant_all(Entities.Grass)
	_harvest_all(Entities.Grass)
			
def grassbf():
	_plant_all(Entities.Grass)
	
	for _ in range(50):
		_harvest_all(Entities.Grass)

	while num_drones() > 1:
		pass

def sunflower():
	plants = dict()
	_plant_all(Entities.Sunflower)
	
	while num_drones() > 1:
		pass
	
	def _collect_row(r, v):
		def _inner():
			for c in range(COLS):
				go_to(c, r)
				if measure() == v:
					while not can_harvest():
						pass
					harvest()
		return _inner

	for v in [15, 14, 13, 12, 11, 10, 9, 8, 7]:
		go_to(0, 0)
		for r in range(ROWS):
			if not spawn_drone(_collect_row(r, v)):
				_collect_row(r, v)()
			move(North)
		while num_drones() > 1:
			pass
		
def tree():
	
	def _exclude():
		return get_pos_x() % 2 == get_pos_y() % 2
	
	_plant_all(Entities.Tree, False, _exclude)
	
	_harvest_all(Entities.Tree)

	while num_drones() > 1:
		pass

def treebf():
	
	def _exclude():
		return get_pos_x() % 2 == get_pos_y() % 2
	
	_plant_all(Entities.Tree, False, _exclude)
	
	while num_drones() > 1:
		pass
		
	for _ in range(50):
		_harvest_all(Entities.Tree, True)

		while num_drones() > 1:
			pass

def carrot():
	_plant_all(Entities.Carrot, False)
	
	while num_drones() > 1:
		pass
		
	_harvest_all(Entities.Carrot)

	while num_drones() > 1:
		pass
	
def pumpkin():
	
	def _custom_plant(cells, entity):
		def _inner():
			failed = list(cells)
			while len(failed) > 0:
				new_failed = set()
				for (row, col) in failed:
					go_to(col, row)
					if can_harvest() and get_entity_type() == Entities.Pumpkin:
						continue
					if get_entity_type() != Entities.Pumpkin:
						pplant(entity)
					new_failed.add((row, col))
				failed = rev(new_failed)
		return _inner
		
	def _custom_plant_all(entity):
		for i in range(ROWS):
			if not spawn_drone(_custom_plant(_cells_in_row(i), entity)):
				_custom_plant(_cells_in_row(i), entity)()
	
	_custom_plant_all(Entities.Pumpkin)
	
	while num_drones() > 1:
		pass
	harvest()
	
def cactus():
	_plant_all(Entities.Cactus, False)
	
	
	while num_drones() > 1:
		pass
	
	def _sort_row(r):
		def _inner(): 
			for k in range(COLS//2 + 1):
				swaps = 0
				go_to(k, r)
				for c in range(k, COLS-1-k):
					if measure() != None and measure() > measure(East):
						swap(East)
						swaps += 1
					move(East)
				if swaps == 0:
					break
				for c in range(COLS-2-k, k-1, -1):
					if measure() != None and measure() < measure(West):
						swap(West)
						swaps += 1
					move(West)
				if swaps == 0:
					break
				
		return _inner
	
	def _sort_col(c):
		def _inner():
			for k in range(ROWS//2 + 1):
				swaps = 0
				go_to(c, k)
				for r in range(k, ROWS-1-k):
					if measure() == None or measure(North) == None:
						return
					if measure() > measure(North):
						swap(North)
						swaps += 1
					move(North)
				if swaps == 0:
					break
				for r in range(ROWS-2-k, k-1, -1):
					if measure() == None or measure(South) == None:
						return
					if measure() < measure(South):
						swap(South)
						swaps += 1
					move(South)
				if swaps == 0:
					break
				
		return _inner
	
	for r in range(ROWS):
		if not spawn_drone(_sort_row(r)):
			_sort_row(r)()
			
	while num_drones() > 1:
		pass
			
	for r in range(ROWS):
		if not spawn_drone(_sort_col(r)):
			_sort_col(r)()
	
	while num_drones() > 1:
		pass
	
	go_to(0, 0)
	harvest()
				
	# walk(harvest, go_to, drone)


last_move = None

def mmove(dir):
	global last_move
	if move(dir):
		last_move = dir
		return True
	return False
	
def is_blocked(seen, dir):
	if seen == None:
		return False
	x, y = get_pos_x(), get_pos_y()
	if dir == North:
		return (x, y+1) in seen
	if dir == South:
		return (x, y-1) in seen
	if dir == East:
		return (x+1, y) in seen
	return (x-1, y) in seen
	
def go_to2(x, y, seen=None):
	if seen != None:
		seen.add((get_pos_x(), get_pos_y()))
		
	if last_move in [East, West]:
		if x > get_pos_x():
			if not is_blocked(seen, East) and mmove(East):
				return go_to2(x, y, seen)
		if x < get_pos_x():
			if not is_blocked(seen, West) and mmove(West):
				return go_to2(x, y, seen)
		if y < get_pos_y():
			if not is_blocked(seen, South) and mmove(South):
				return go_to2(x, y, seen)
		if y > get_pos_y():
			if not is_blocked(seen, North) and mmove(North):
				return go_to2(x, y, seen)
	else:
		
		if y < get_pos_y():
			if not is_blocked(seen, South) and mmove(South):
				return go_to2(x, y, seen)
		if y > get_pos_y():
			if not is_blocked(seen, North) and mmove(North):
				return go_to2(x, y, seen)
		if x > get_pos_x():
			if not is_blocked(seen, East) and mmove(East):
				return go_to2(x, y, seen)
		if x < get_pos_x():
			if not is_blocked(seen, West) and mmove(West):
				return go_to2(x, y, seen)
				
	if seen != None:
		for dir in [East, West]:
			if move(dir):
				go_to2(x, y)
	
def dinosaur():
	done = False
	change_hat(Hats.Dinosaur_Hat)
	
	while True:
		can = False
		for d in DIRS:
			if can_move(d):
				can = True
		
		if not can:
			harvest()
			break

			
		
		go_to2(1, 0)
		for r in range(ROWS-1):
			if r % 2 == 0:
				go_to2(COLS-1, r)
			else:
				go_to2(1, r)
			move(North)
		go_to2(0, ROWS-1)
		go_to2(0, 0)
		if get_pos_x() != 0 or get_pos_y() != 0:
			harvest()
			break
		

DIRS = [North, East, South, West]

def index(dir):
	for i in range(len(DIRS)): 
		if DIRS[i] == dir:
			return i
			
	return None

def left(dir):
	return DIRS[index(dir)-1]
	
def right(dir):
	return DIRS[(index(dir)+1)%len(DIRS)]

def shuffled(_D):
	D = list(_D)
	for _ in range(len(D)//2):
		i, j = random() * len(D) // 1, random() * len(D) // 1
		D[i], D[j] = D[j], D[i]
	return D


def maze():
	harvest()
	global ROWS
	global COLS

	t = 60

	set_world_size(32)
	
	ROWS = get_world_size()
	COLS = get_world_size()
	
	plant(Entities.Bush)
	def _init_maze():
		substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1) 
		use_item(Items.Weird_Substance, substance)
		
	_init_maze()
	
	def _crawler():
		def _inner():
			count = 0
			 
			seen = set()
			stime = get_time()	
			
			
			SD = shuffled(DIRS)
			def _find(seen, last_dir):
				global count
				if get_entity_type() == Entities.Treasure:
					if get_time() - stime >= t:
						harvest()
						return True
					count += 1
					_init_maze()
					return False
				
				if get_entity_type() != Entities.Hedge:
					return False
					
				if (get_pos_x(), get_pos_y()) in seen:
					seen.remove((get_pos_x(), get_pos_y()))
					return False
					
					
				seen.add((get_pos_x(), get_pos_y()))
				
				
				for dir in SD:
					if measure() in seen:
						
						return False
				
					if get_entity_type() != Entities.Hedge:
						return False
					if dir == left(left(last_dir)):
						continue
					if move(dir):
						if not spawn_drone(_crawler()):
							if _find(seen, dir):
								return True
							if get_entity_type() != Entities.Hedge:
								return False
							move(left(left(dir)))

					if get_entity_type() == Entities.Treasure:
						if get_time() - stime >= t:
							harvest()
							return False
						count += 1
						_init_maze()
						return True
				
				return False
			
			while count < 2 and get_entity_type() == Entities.Hedge:
				SD = shuffled(DIRS)
				for dir in SD:
					seen = set()
					if get_entity_type() != Entities.Hedge:
						return False
					if _find(set(), dir):
						return
					
		return _inner
	
	_crawler()()
	
	while num_drones() > 1:
		pass
	#while get_entity_type() == Entities.Hedge:
	#	if not spawn_drone(_crawler()):
	#		pass
		
	
items = [
	(1, sunflower, Hats.Top_Hat), 
	(1, grass, Hats.Top_Hat),
	(1, tree, Hats.Top_Hat),
	(1, carrot, Hats.Top_Hat),
	(1, pumpkin, Hats.Top_Hat), 
	(1, cactus, Hats.Top_Hat),
	(1, maze, Hats.Top_Hat),
	(1, dinosaur, Hats.Top_Hat),
]

#change_hat(Hats.Wizard_Hat)  


def _clear_all():
	def _row(r):
		def _inner():
			for c in range(COLS):
				go_to(c, r)
				harvest()
				plant(Entities.Grass)
		return _inner
	 
	for i in range(ROWS):
		if not spawn_drone(_row(i)): 
			_row(i)()


def dinosaur2():
	#change_hat(Hats.Dinosaur_Hat)
	x, y = measure()
	while True:
		go_to2(x, y)
		if get_pos_x() != x or get_pos_y() != y:
			moved = False
			for dir in shuffled(DIRS):
				if move(dir):
					moved = True
					break
			
			if not moved:
				harvest()
				break
			continue

		if measure() == None:
			harvest()
		x, y = measure()
		
	


while num_items(Items.Bone) < 3348892800:
	dinosaur2()
	
	

while False:
	for (n, func, hat) in items:
		if n == 0:
			continue
		go_to(0, 0)
		print(str(func))
		change_hat(hat) 
		do_a_flip()
		for _ in range(n):
			go_to(0, 0)
			func()
			
		while num_drones() > 1:
			pass
			
	sleep(10)