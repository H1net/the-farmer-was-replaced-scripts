# ===== UNLOCK PLANNER =====
# Manages unlock progression and resource planning

# Comprehensive unlock priority system
unlock_priority = [
	# Phase 1: Speed and Expansion (Core efficiency)
	Unlocks.Speed,      # Faster farming = faster everything
	Unlocks.Expand,     # More tiles = more production
	Unlocks.Speed,      # Stack speed upgrades for maximum efficiency
	Unlocks.Expand,     # More expansion for larger farms
	
	# Phase 2: Essential Crops (Resource diversity)
	Unlocks.Carrots,    # Unlock carrots for pumpkin production
	Unlocks.Pumpkins,   # Unlock pumpkins for mega-pumpkin bonuses
	Unlocks.Sunflowers, # Unlock sunflowers for power generation
	
	# Phase 3: Advanced Crops (Specialized production)
	Unlocks.Trees,      # Unlock trees for wood production
	Unlocks.Cactus,     # Unlock cactus for specialized farming
	
	# Phase 4: Additional Speed/Expansion (Scaling)
	Unlocks.Speed,      # More speed upgrades
	Unlocks.Expand,     # More expansion
	Unlocks.Speed,      # Final speed upgrade
	Unlocks.Expand,     # Final expansion
]

# Current unlock goal
current_unlock_goal = None
current_unlock_index = 0

# Initialize unlock planner
def initialize_unlock_planner():
	global current_unlock_goal
	global current_unlock_index
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
	global current_unlock_goal
	global current_unlock_index
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
	# Get list of items in cost dictionary
	cost_items = []
	for item in cost:
		cost_items.append(item)
	
	for item in cost_items:
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

# Recursively calculate total resource requirements for an unlock
def get_total_unlock_requirements(unlock_name, depth):
	# Prevent infinite recursion
	if depth > 5:
		quick_print("Max recursion depth reached for unlock requirements")
		return {}
	
	if unlock_name == None:
		return {}
	
	cost = get_cost(unlock_name)
	if cost == None:
		return {}
	
	total_requirements = {}
	
	# Get list of items in cost dictionary
	cost_items = []
	for item in cost:
		cost_items.append(item)
	
	# Add direct requirements
	for item in cost_items:
		amount_needed = cost[item]
		if item in total_requirements:
			total_requirements[item] += amount_needed
		else:
			total_requirements[item] = amount_needed
	
	# Check if any of these items require other unlocks
	# For now, we'll assume basic resources (Hay, Wood, Carrot) are available
	# This could be expanded to check for unlock dependencies
	
	return total_requirements

# Wrapper function to call get_total_unlock_requirements with depth 0
def get_total_unlock_requirements_simple(unlock_name):
	return get_total_unlock_requirements(unlock_name, 0)

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
	
	# Get list of items in requirements dictionary
	req_items = []
	for item in requirements:
		req_items.append(item)
	
	for item in req_items:
		needed = requirements[item]
		have = num_items(item)
		total_needed += needed
		if have < needed:
			total_have += have
		else:
			total_have += needed  # Don't count excess
	
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
	
	# Get list of required items
	req_items = []
	for item in requirements:
		req_items.append(item)
	
	# Count current allocation for each resource
	resource_columns = {}
	for item in req_items:
		resource_columns[item] = 0
	
	# Count current allocation
	for column in range(get_world_size()):
		if column in config.farm_config:
			plant = config.farm_config[column]
			# Check what this plant produces
			if plant == Entities.Grass and Items.Hay in req_items:
				resource_columns[Items.Hay] += 1
			elif plant == Entities.Tree and Items.Wood in req_items:
				resource_columns[Items.Wood] += 1
			elif plant == Entities.Carrot and Items.Carrot in req_items:
				resource_columns[Items.Carrot] += 1
	
	# Simple optimization: if we need more of a resource, suggest more columns
	optimization_suggestions = []
	for item in req_items:
		current_columns = resource_columns[item]
		needed_amount = requirements[item]
		# Simple heuristic: need at least 1 column per 10 resources needed
		suggested_columns = max(1, needed_amount // 10)
		if current_columns < suggested_columns:
			optimization_suggestions.append("Need more " + str(item) + " production (have " + str(current_columns) + " columns, need ~" + str(suggested_columns) + ")")
	
	if optimization_suggestions:
		quick_print("Unlock optimization suggestions:")
		for suggestion in optimization_suggestions:
			quick_print("  - " + suggestion)
	
	# For now, return the current config
	# TODO: Implement dynamic farm layout adjustment
	return config.farm_config

# Check and attempt to unlock current goal
def check_and_attempt_unlock():
	if current_unlock_goal == None:
		return False
	
	# Check if we can afford the current unlock
	if can_afford_unlock(current_unlock_goal):
		quick_print("Attempting to unlock: " + str(current_unlock_goal))
		success = unlock(current_unlock_goal)
		if success:
			quick_print("Successfully unlocked: " + str(current_unlock_goal) + "! Moving to next goal.")
			# Move to next unlock
			advance_to_next_unlock()
			return True
		else:
			quick_print("Failed to unlock: " + str(current_unlock_goal) + " (insufficient resources)")
			return False
	else:
		# Show progress toward current unlock
		progress = get_unlock_progress()
		if progress > 50:  # Only show progress if we're making good progress
			quick_print("Progress toward " + str(current_unlock_goal) + ": " + str(progress) + "%")
		return False

# Get debug info about current unlock status
def get_unlock_debug_info():
	if current_unlock_goal == None:
		return "All unlocks completed! 🎉"
	
	requirements = get_current_unlock_requirements()
	progress = get_unlock_progress()
	
	info = "🎯 Goal: " + str(current_unlock_goal) + " | Progress: " + str(progress) + "%"
	
	if requirements:
		info += " | Requirements: "
		req_items = []
		for item in requirements:
			req_items.append(item)
		
		for item in req_items:
			needed = requirements[item]
			have = num_items(item)
			if needed > 0:
				percentage = (have / needed) * 100
			else:
				percentage = 100
			info += str(item) + "(" + str(have) + "/" + str(needed) + "=" + str(percentage) + "%) "
	
	# Add next unlock preview
	next_unlock = get_next_unlock_preview()
	if next_unlock:
		info += " | Next: " + next_unlock
	
	return info

# Get preview of next unlock in queue
def get_next_unlock_preview():
	if current_unlock_index + 1 < len(unlock_priority):
		next_unlock = unlock_priority[current_unlock_index + 1]
		next_cost = get_cost(next_unlock)
		if next_cost:
			cost_str = ""
			next_items = []
			for item in next_cost:
				next_items.append(item)
			for item in next_items:
				cost_str += str(item) + "(" + str(next_cost[item]) + ") "
			return str(next_unlock) + "[" + cost_str + "]"
		else:
			return str(next_unlock)
	return None