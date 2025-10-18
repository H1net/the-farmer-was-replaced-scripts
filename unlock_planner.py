# ===== UNLOCK PLANNER =====
# Manages unlock progression and resource planning

# Unlock priority list (configurable)
unlock_priority = [
	Unlocks.Speed,      # Faster farming = faster everything
	Unlocks.Expand,     # More tiles = more production
	Unlocks.Speed,      # Stack speed upgrades
	Unlocks.Carrots,    # Unlock new crops as needed
	# Add more as needed
]

# Current unlock goal
current_unlock_goal = None
current_unlock_index = 0

# Initialize unlock planner
def initialize_unlock_planner():
	global current_unlock_goal, current_unlock_index
	current_unlock_index = 0
	if len(unlock_priority) > 0:
		current_unlock_goal = unlock_priority[0]
	else:
		current_unlock_goal = None

# Get the current unlock goal
def get_current_unlock_goal():
	return current_unlock_goal

# Move to next unlock in priority list
def advance_to_next_unlock():
	global current_unlock_goal, current_unlock_index
	current_unlock_index += 1
	if current_unlock_index < len(unlock_priority):
		current_unlock_goal = unlock_priority[current_unlock_index]
	else:
		current_unlock_goal = None
	return current_unlock_goal

# Check if we can afford a specific unlock
def can_afford_unlock(unlock_name):
	if unlock_name == None:
		return False
	
	cost = get_cost(unlock_name)
	if cost == None:
		return True  # No cost means we can afford it
	
	# Check if we have all required resources
	for item in cost:
		amount_needed = cost[item]
		if num_items(item) < amount_needed:
			return False
	
	return True

# Attempt to purchase an unlock
def attempt_unlock(unlock_name):
	if unlock_name == None:
		return False
	
	if can_afford_unlock(unlock_name):
		quick_print("Attempting to unlock: " + str(unlock_name))
		success = unlock(unlock_name)
		if success:
			quick_print("Successfully unlocked: " + str(unlock_name))
		else:
			quick_print("Failed to unlock: " + str(unlock_name))
		return success
	else:
		quick_print("Cannot afford unlock: " + str(unlock_name))
		return False

# Get total resource requirements for current unlock goal
def get_current_unlock_requirements():
	if current_unlock_goal == None:
		return {}
	
	cost = get_cost(current_unlock_goal)
	if cost == None:
		return {}
	
	return cost

# Check if we should try to unlock current goal
def should_attempt_current_unlock():
	if current_unlock_goal == None:
		return False
	
	return can_afford_unlock(current_unlock_goal)

# Get progress toward current unlock (percentage)
def get_unlock_progress():
	if current_unlock_goal == None:
		return 100.0
	
	requirements = get_current_unlock_requirements()
	if not requirements:
		return 100.0
	
	total_needed = 0
	total_have = 0
	
	for item in requirements:
		needed = requirements[item]
		have = num_items(item)
		total_needed += needed
		total_have += min(have, needed)  # Don't count excess
	
	if total_needed == 0:
		return 100.0
	
	return (total_have / total_needed) * 100.0

# Optimize farm layout for current unlock requirements
def optimize_farm_for_current_unlock():
	import config
	
	if current_unlock_goal == None:
		return config.farm_config
	
	requirements = get_current_unlock_requirements()
	if not requirements:
		return config.farm_config
	
	# Simple optimization: prioritize resources needed for unlock
	# This is a basic implementation - could be much more sophisticated
	
	# Count how many columns we have for each resource
	resource_columns = {}
	for item in requirements:
		resource_columns[item] = 0
	
	# Count current allocation
	for column in range(get_world_size()):
		if column in config.farm_config:
			plant = config.farm_config[column]
			# Check what this plant produces
			if plant == Entities.Grass and Items.Hay in requirements:
				resource_columns[Items.Hay] += 1
			elif plant == Entities.Tree and Items.Wood in requirements:
				resource_columns[Items.Wood] += 1
			elif plant == Entities.Carrot and Items.Carrot in requirements:
				resource_columns[Items.Carrot] += 1
	
	# For now, return the current config
	# TODO: Implement more sophisticated optimization
	return config.farm_config

# Check and attempt to unlock current goal
def check_and_attempt_unlock():
	if should_attempt_current_unlock():
		success = attempt_unlock(current_unlock_goal)
		if success:
			# Move to next unlock
			advance_to_next_unlock()
			quick_print("Moved to next unlock goal: " + str(current_unlock_goal))
		return success
	return False

# Get debug info about current unlock status
def get_unlock_debug_info():
	if current_unlock_goal == None:
		return "No unlock goal set"
	
	requirements = get_current_unlock_requirements()
	progress = get_unlock_progress()
	
	info = "Goal: " + str(current_unlock_goal) + " Progress: " + str(progress) + "%"
	
	if requirements:
		info += " Requirements: "
		for item in requirements:
			needed = requirements[item]
			have = num_items(item)
			info += str(item) + "(" + str(have) + "/" + str(needed) + ") "
	
	return info