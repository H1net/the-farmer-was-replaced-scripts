# ===== PLANT LOGIC FUNCTIONS =====

# Helper function to determine what to plant based on available resources
def get_plant_to_use(intended_plant):
	# Check what resources we have
	wood_count = num_items(Items.Wood)
	hay_count = num_items(Items.Hay)
	carrot_count = num_items(Items.Carrot)
	
	# Resource requirements for each plant
	if intended_plant == Entities.Grass:
		# Grass grows automatically, but we can plant it
		return Entities.Grass
	elif intended_plant == Entities.Tree:
		# Trees need wood and hay
		if wood_count >= 1 and hay_count >= 1:
			return Entities.Tree
		elif wood_count < 1:
			# Need wood, but bushes also need wood and hay - check if we can plant bushes
			if wood_count >= 1 and hay_count >= 1:
				return Entities.Bush
			else:
				return Entities.Grass  # Plant grass to get hay, then bushes for wood
		else:
			return Entities.Grass  # Plant grass to get hay
	elif intended_plant == Entities.Carrot:
		# Carrots need wood and hay
		if wood_count >= 1 and hay_count >= 1:
			return Entities.Carrot
		elif wood_count < 1:
			# Need wood, but bushes also need wood and hay - check if we can plant bushes
			if wood_count >= 1 and hay_count >= 1:
				return Entities.Bush
			else:
				return Entities.Grass  # Plant grass to get hay, then bushes for wood
		else:
			return Entities.Grass  # Plant grass to get hay
	elif intended_plant == Entities.Pumpkin:
		# Pumpkins need carrots
		if carrot_count >= 1:
			return Entities.Pumpkin
		else:
			# Need carrots, but carrots need wood and hay - check if we can plant carrots
			if wood_count >= 1 and hay_count >= 1:
				return Entities.Carrot
			elif wood_count < 1:
				# Need wood for carrots, but bushes also need wood and hay
				if wood_count >= 1 and hay_count >= 1:
					return Entities.Bush
				else:
					return Entities.Grass  # Plant grass to get hay, then bushes for wood
			else:
				return Entities.Grass  # Plant grass to get hay for carrots
	else:
		# Default fallback
		return Entities.Grass

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
	
	# Check if ground needs to be changed to the required type
	current_ground = get_ground_type()
	if current_ground != required_ground_type:
		till()  # Till to change ground type
		#print("Changed ground to", required_ground_type, "at", pos_x, pos_y)
	
	# Determine what to actually plant based on available resources
	actual_plant = get_plant_to_use(intended_plant)
	
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
