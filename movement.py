# ===== INTELLIGENT MOVEMENT SYSTEM =====
# Task-based movement with pathfinding optimization

# Import config to access farm_config
import config
import state_manager
import plant_logic

# ===== TASK QUEUE SYSTEM =====

# Global task queue for efficient movement planning
task_queue = []

# Add a task to the queue
def add_task(task_type, positions, plant_type, priority):
	global task_queue
	task = {
		'type': task_type,
		'positions': positions,
		'plant_type': plant_type,
		'priority': priority
	}
	task_queue.append(task)

# Clear all tasks from the queue
def clear_task_queue():
	global task_queue
	task_queue = []

# Get all tasks of a specific type
def get_tasks_by_type(task_type):
	global task_queue
	matching_tasks = []
	for task in task_queue:
		if task['type'] == task_type:
			matching_tasks.append(task)
	return matching_tasks

# ===== PATHFINDING FUNCTIONS =====

# Calculate Manhattan distance between two positions
def manhattan_distance(pos1, pos2):
	x1, y1 = pos1
	x2, y2 = pos2
	return abs(x1 - x2) + abs(y1 - y2)

# Find the closest position to current location
def find_closest_position(target_positions):
	current_x, current_y = get_pos_x(), get_pos_y()
	closest_pos = None
	closest_distance = 999999  # Large number instead of float('inf')
	
	for pos in target_positions:
		distance = manhattan_distance((current_x, current_y), pos)
		if distance < closest_distance:
			closest_distance = distance
			closest_pos = pos
	
	return closest_pos

# Move to a specific position using optimal path
def move_to_position(target_x, target_y):
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# Move horizontally first
	if current_x < target_x:
		for i in range(target_x - current_x):
			move(East)
	elif current_x > target_x:
		for i in range(current_x - target_x):
			move(West)
	
	# Then move vertically
	if current_y < target_y:
		for i in range(target_y - current_y):
			move(North)
	elif current_y > target_y:
		for i in range(current_y - target_y):
			move(South)

# Function to move back to starting position (0,0)
def return_to_start():
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# Move west to get to x=0
	for i in range(current_x):
		move(West)
	
	# Move south to get to y=0  
	for i in range(current_y):
		move(South)

# ===== INTELLIGENT TASK EXECUTION =====

# Execute all tasks in the queue with optimal pathfinding
def execute_task_queue():
	global task_queue
	
	if not task_queue:
		quick_print("No tasks in queue")
		return
	
	quick_print("Executing " + str(len(task_queue)) + " tasks")
	
	# Sort tasks by priority (lower number = higher priority)
	# Simple bubble sort for compatibility
	for i in range(len(task_queue)):
		for j in range(len(task_queue) - 1 - i):
			if task_queue[j]['priority'] > task_queue[j + 1]['priority']:
				# Swap tasks
				temp = task_queue[j]
				task_queue[j] = task_queue[j + 1]
				task_queue[j + 1] = temp
	
	# Execute each task
	for task in task_queue:
		execute_task(task)
	
	# Clear the queue after execution
	clear_task_queue()

# Execute a single task with pathfinding optimization
def execute_task(task):
	task_type = task['type']
	positions = task['positions']
	plant_type = None
	if 'plant_type' in task:
		plant_type = task['plant_type']
	
	if not positions:
		quick_print("Task " + task_type + " has no positions, skipping")
		return
	
	# Find the closest position to current location
	closest_pos = find_closest_position(positions)
	if closest_pos:
		target_x, target_y = closest_pos
		quick_print("Executing " + task_type + " at " + str(target_x) + "," + str(target_y))
		move_to_position(target_x, target_y)
		
		# Execute the specific task
		if task_type == 'harvest_plant':
			execute_harvest_task(target_x, target_y, plant_type)
		elif task_type == 'replant_dead':
			execute_replant_task(target_x, target_y, plant_type)
		elif task_type == 'check_sunflowers':
			execute_sunflower_check(target_x, target_y)
		elif task_type == 'check_cactus':
			execute_cactus_check(target_x, target_y)
		elif task_type == 'plant_sunflower':
			execute_plant_sunflower_task(target_x, target_y, plant_type)
		elif task_type == 'plant_cactus':
			execute_plant_cactus_task(target_x, target_y, plant_type)
		elif task_type == 'plant_standard':
			execute_plant_standard_task(target_x, target_y, plant_type)
	else:
		quick_print("No closest position found for " + task_type)

# Execute harvest task at specific position
def execute_harvest_task(x, y, plant_type):
	entity_type = get_entity_type()
	if entity_type == plant_type and can_harvest():
		harvest()
		quick_print("Harvested " + str(plant_type) + " at " + str(x) + "," + str(y))

# Execute replant task at specific position
def execute_replant_task(x, y, plant_type):
	entity_type = get_entity_type()
	
	# Check if it's a dead version of the plant or can't be harvested
	if entity_type == Entities.Dead_Pumpkin or (entity_type == plant_type and not can_harvest()):
		quick_print("Found dead/dying " + str(plant_type) + " at " + str(x) + "," + str(y) + " - replanting")
		
		# Plant the intended plant
		if plant_type == Entities.Pumpkin and num_items(Items.Carrot) >= 1:
			plant(Entities.Pumpkin)
			state_manager.update_tile_state(x, y, Entities.Pumpkin, Entities.Pumpkin, Grounds.Soil, False)
		elif plant_type == Entities.Pumpkin:
			# No carrots available, plant carrot instead
			plant(Entities.Carrot)
			state_manager.update_tile_state(x, y, Entities.Pumpkin, Entities.Carrot, Grounds.Soil, True)
		else:
			plant(plant_type)
			state_manager.update_tile_state(x, y, plant_type, plant_type, Grounds.Soil, False)

# Execute sunflower check at specific position
def execute_sunflower_check(x, y):
	entity_type = get_entity_type()
	if entity_type == Entities.Sunflower:
		petal_count = measure()
		quick_print("Sunflower at " + str(x) + "," + str(y) + " has " + str(petal_count) + " petals")

# Execute cactus check at specific position
def execute_cactus_check(x, y):
	entity_type = get_entity_type()
	if entity_type == Entities.Cactus:
		size = measure()
		quick_print("Cactus at " + str(x) + "," + str(y) + " size: " + str(size))

# Execute sunflower planting task at specific position
def execute_plant_sunflower_task(x, y, plant_type):
	# Plant sunflower at current position (we're already at the target)
	plant_logic.harvest_and_plant(plant_type, Grounds.Soil)
	# Update state
	state_manager.update_tile_state(x, y, plant_type, plant_type, Grounds.Soil, False)
	quick_print("Planted sunflower at " + str(x) + "," + str(y))

# Execute cactus planting task at specific position
def execute_plant_cactus_task(x, y, plant_type):
	# Plant cactus at current position (we're already at the target)
	plant_logic.harvest_and_plant(plant_type, Grounds.Soil)
	# Update state
	state_manager.update_tile_state(x, y, plant_type, plant_type, Grounds.Soil, False)
	quick_print("Planted cactus at " + str(x) + "," + str(y))

# Execute standard planting task at specific position
def execute_plant_standard_task(x, y, plant_type):
	# Get required ground type
	if plant_type in config.ground_requirements:
		required_ground = config.ground_requirements[plant_type]
	else:
		required_ground = Grounds.Grassland
	
	# Plant at current position (we're already at the target)
	plant_logic.harvest_and_plant(plant_type, required_ground)
	# Update state
	state_manager.update_tile_state(x, y, plant_type, plant_type, required_ground, False)
	quick_print("Planted " + str(plant_type) + " at " + str(x) + "," + str(y))

# ===== TARGETED SCAN FUNCTIONS =====

# Efficient dead pumpkin scanning using state management
def replant_dead_pumpkins():
	# Get all known pumpkin positions from state
	pumpkin_positions = state_manager.get_tiles_by_plant(Entities.Pumpkin)
	intended_pumpkin_positions = state_manager.get_tiles_by_intended_plant(Entities.Pumpkin)
	
	# Combine and deduplicate positions
	all_pumpkin_positions = pumpkin_positions + intended_pumpkin_positions
	# Remove duplicates manually
	unique_positions = []
	for pos in all_pumpkin_positions:
		if pos not in unique_positions:
			unique_positions.append(pos)
	all_pumpkin_positions = unique_positions
	
	quick_print("Checking " + str(len(all_pumpkin_positions)) + " known pumpkin positions for dead pumpkins")
	
	# Add replant tasks to the queue
	if all_pumpkin_positions:
		add_task('replant_dead', all_pumpkin_positions, Entities.Pumpkin, 1)
	
	# Execute all tasks
	execute_task_queue()

# ===== ADDITIONAL INTELLIGENT MOVEMENT FUNCTIONS =====

# Add harvest tasks for specific plant types
def add_harvest_tasks(plant_type):
	positions = state_manager.get_tiles_by_plant(plant_type)
	if positions:
		add_task('harvest_plant', positions, plant_type, 2)
		quick_print("Added harvest tasks for " + str(plant_type) + ": " + str(len(positions)) + " positions")

# Add sunflower optimization tasks
def add_sunflower_tasks():
	positions = state_manager.get_tiles_by_plant(Entities.Sunflower)
	if positions:
		add_task('check_sunflowers', positions, None, 3)

# Add cactus optimization tasks
def add_cactus_tasks():
	positions = state_manager.get_tiles_by_plant(Entities.Cactus)
	if positions:
		add_task('check_cactus', positions, None, 4)

# Add planting tasks based on farm configuration
def add_planting_tasks():
	# Get all columns that need planting based on config
	planting_positions = []
	
	for column in range(get_world_size()):
		# Get intended plant for this column
		if column in config.farm_config:
			intended_plant = config.farm_config[column]
		else:
			intended_plant = Entities.Grass
		
		# Check each row in this column
		for row in range(get_world_size()):
			pos = (column, row)
			
			# Check if this tile needs the intended plant
			state = state_manager.get_tile_state(column, row)
			if state == None:
				# No state recorded, needs initial planting
				planting_positions.append((pos, intended_plant))
			else:
				if state['intended_plant'] != intended_plant or state['actual_plant'] != intended_plant:
					# Tile has wrong plant or no plant, needs replanting
					planting_positions.append((pos, intended_plant))
	
	# Add planting tasks for each position
	if planting_positions:
		quick_print("Adding " + str(len(planting_positions)) + " planting tasks")
		for pos, plant_type in planting_positions:
			if plant_type == Entities.Sunflower:
				add_task('plant_sunflower', [pos], plant_type, 5)
			elif plant_type == Entities.Cactus:
				add_task('plant_cactus', [pos], plant_type, 5)
			else:
				add_task('plant_standard', [pos], plant_type, 5)
	else:
		quick_print("No planting tasks needed - farm is up to date")

# Execute all pending tasks efficiently
def execute_all_pending_tasks():
	quick_print("Starting task execution cycle")
	
	# Add harvest tasks for all plant types
	add_harvest_tasks(Entities.Grass)
	add_harvest_tasks(Entities.Tree)
	add_harvest_tasks(Entities.Carrot)
	add_harvest_tasks(Entities.Pumpkin)
	add_harvest_tasks(Entities.Sunflower)
	add_harvest_tasks(Entities.Cactus)
	
	# Add optimization tasks
	add_sunflower_tasks()
	add_cactus_tasks()
	
	# Add planting tasks based on farm configuration
	add_planting_tasks()
	
	# Execute all tasks with pathfinding
	execute_task_queue()
	
	quick_print("Task execution cycle complete")

# Get movement efficiency statistics
def get_movement_stats():
	global task_queue
	total_tasks = len(task_queue)
	
	# Count unique task types manually
	task_types = []
	for task in task_queue:
		task_type = task['type']
		if task_type not in task_types:
			task_types.append(task_type)
	
	return {
		'total_tasks': total_tasks,
		'task_types': len(task_types)
	}
