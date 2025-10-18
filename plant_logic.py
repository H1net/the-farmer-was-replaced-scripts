# ===== PLANT LOGIC FUNCTIONS =====
# Import config for sunflower settings
import config

# Helper function to check if we can afford a plant
def can_afford_plant(entity):
	cost = get_cost(entity)
	if cost == None:
		return True  # No cost means we can afford it (like Grass)
	
	for item in cost:
		amount_needed = cost[item]
		if num_items(item) < amount_needed:
			return False
	return True

# Helper function to find missing resources
def get_missing_resource(entity):
	cost = get_cost(entity)
	if cost == None:
		return None  # No cost means we can afford it
	
	for item in cost:
		amount_needed = cost[item]
		if num_items(item) < amount_needed:
			return item
	return None

# Helper function to find plant for missing resource
def find_plant_for_missing_resource(missing_item):
	if missing_item in config.resource_producers:
		return config.resource_producers[missing_item]
	else:
		return Entities.Grass  # Fallback to grass

# Helper function to determine what to plant based on available resources
def get_plant_to_use(intended_plant, depth=0):
	# Prevent infinite recursion
	if depth > 10:
		print("Max recursion depth reached for", intended_plant, "- falling back to grass")
		return Entities.Grass
	
	# Special case: Grass has no cost
	if intended_plant == Entities.Grass:
		return Entities.Grass
	
	# Check if we can afford the intended plant
	if can_afford_plant(intended_plant):
		if depth > 0:
			print("Can afford", intended_plant, "after", depth, "fallbacks")
		return intended_plant
	
	# Find what resource we're missing
	missing_item = get_missing_resource(intended_plant)
	
	# Safety check: if we can't determine missing resource, fallback to grass
	if missing_item == None:
		print("Cannot determine missing resource for", intended_plant, "- falling back to grass")
		return Entities.Grass
	
	# Debug: Show what resource is missing
	if depth == 0:
		print("Cannot afford", intended_plant, "- missing", missing_item, "need", num_items(missing_item), "more")
	
	# Find what plant produces that resource
	fallback_plant = find_plant_for_missing_resource(missing_item)
	
	# Safety check: if fallback is the same as intended, we have a circular dependency
	if fallback_plant == intended_plant:
		print("Circular dependency detected for", intended_plant, "- falling back to grass")
		return Entities.Grass
	
	# Recursively check if we can afford the fallback
	return get_plant_to_use(fallback_plant, depth + 1)

# Helper function to harvest and plant a specific entity
def harvest_and_plant(intended_plant, required_ground_type=Grounds.Grassland):
	pos_x, pos_y = get_pos_x(), get_pos_y()
	
	# Only water trees (they grow slowly and need the help)
	if intended_plant == Entities.Tree:
		water_level = get_water()
		if water_level < 0.5 and num_items(Items.Water) > 0:
			use_item(Items.Water)
			#print("Watered tree at", pos_x, pos_y, "- water level:", water_level)
	
	# Disabled fertilizer to conserve resources
	# if num_items(Items.Fertilizer) > 0:
	#	use_item(Items.Fertilizer)
	#	#print("Used fertilizer at", pos_x, pos_y)
	
	# Determine what to actually plant based on available resources
	actual_plant = get_plant_to_use(intended_plant)
	
	# Debug: Show what we're planting vs what was intended
	if actual_plant != intended_plant:
		print("Resource fallback at", pos_x, pos_y, "- intended:", intended_plant, "planting:", actual_plant)
	
	# Check if ground needs to be changed to the required type for the ACTUAL plant
	if actual_plant in config.ground_requirements:
		actual_ground_required = config.ground_requirements[actual_plant]
	else:
		actual_ground_required = Grounds.Grassland
	
	current_ground = get_ground_type()
	if current_ground != actual_ground_required:
		till()  # Till to change ground type
		print("Tilled ground to", actual_ground_required, "for", actual_plant, "at", pos_x, pos_y)
	
	if can_harvest():
		harvest()
		#print("Harvested at", pos_x, pos_y)
		plant(actual_plant)
		if actual_plant != intended_plant:
			print("Planted", actual_plant, "instead of", intended_plant, "at", pos_x, pos_y)
		#else:
		#	print("Planted", actual_plant, "at", pos_x, pos_y)
	else:
		plant(actual_plant)
		if actual_plant != intended_plant:
			print("Planted", actual_plant, "instead of", intended_plant, "at", pos_x, pos_y)
		#else:
		#	print("Planted", actual_plant, "at", pos_x, pos_y)

# Helper function to process one column
def process_column(intended_plant, required_ground_type=Grounds.Grassland, hat_color=None):
	if hat_color:
		change_hat(hat_color)
		#print("Changed to", hat_color, "hat")
	
	for j in range(get_world_size()):
		harvest_and_plant(intended_plant, required_ground_type)
		move(North)

# Function to find and harvest the best sunflower (with most petals)
def find_and_harvest_best_sunflower():
	# Store current position
	start_x, start_y = get_pos_x(), get_pos_y()
	
	best_sunflower_pos = None
	best_petal_count = 0
	total_sunflowers = 0
	
	# Scan all sunflower columns
	for column in range(get_world_size()):
		if column in config.farm_config and config.farm_config[column] == Entities.Sunflower:
			# Move to this sunflower column
			current_x = get_pos_x()
			if current_x < column:
				for i in range(column - current_x):
					move(East)
			elif current_x > column:
				for i in range(current_x - column):
					move(West)
			
			# Check each row in this column for grown sunflowers
			for row in range(get_world_size()):
				entity_type = get_entity_type()
				
				# Check if it's a grown sunflower
				if entity_type == Entities.Sunflower and can_harvest():
					total_sunflowers += 1
					petal_count = measure()
					
					# Track the sunflower with most petals
					if petal_count > best_petal_count:
						best_petal_count = petal_count
						best_sunflower_pos = (get_pos_x(), get_pos_y())
				
				# Move to next row
				if row < get_world_size() - 1:
					move(North)
	
	# Return to starting position
	current_x, current_y = get_pos_x(), get_pos_y()
	for i in range(current_x):
		move(West)
	for i in range(current_y):
		move(South)
	
	# If we have enough sunflowers and found a best one, harvest it
	if total_sunflowers >= config.sunflower_harvest_threshold and best_sunflower_pos:
		# Move to the best sunflower
		target_x, target_y = best_sunflower_pos
		for i in range(target_x):
			move(East)
		for i in range(target_y):
			move(North)
		
		# Harvest the best sunflower (5x power bonus)
		harvest()
		print("Harvested best sunflower with", best_petal_count, "petals for 5x power bonus!")
		return True
	
	return False

# Function to process sunflower column with optimal harvesting
def process_sunflower_column():
	# First try to harvest the best sunflower if we have enough
	if find_and_harvest_best_sunflower():
		# If we harvested the best one, just plant new sunflowers in this column
		for j in range(get_world_size()):
			harvest_and_plant(Entities.Sunflower, Grounds.Soil)
			move(North)
	else:
		# Normal processing - harvest if ready, plant if not
		for j in range(get_world_size()):
			harvest_and_plant(Entities.Sunflower, Grounds.Soil)
			move(North)
