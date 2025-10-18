# ===== MOVEMENT FUNCTIONS =====

# Import config to access farm_config
import config

# Function to move back to starting position (0,0)
def return_to_start():
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# Move west to get to x=0
	for i in range(current_x):
		move(West)
	
	# Move south to get to y=0  
	for i in range(current_y):
		move(South)

# Function to check and replant dead pumpkins
def replant_dead_pumpkins():
	# Store current position
	start_x, start_y = get_pos_x(), get_pos_y()
	
	# Quick scan of all pumpkin columns for dead pumpkins
	for column in range(get_world_size()):
		# Check if this column is configured for pumpkins
		if column in config.farm_config and config.farm_config[column] == Entities.Pumpkin:
			# Move to this pumpkin column
			current_x = get_pos_x()
			if current_x < column:
				for i in range(column - current_x):
					move(East)
			elif current_x > column:
				for i in range(current_x - column):
					move(West)
			
			# Check each row in this column for dead pumpkins
			for row in range(get_world_size()):
				entity_type = get_entity_type()
				
				# Check if it's a dead pumpkin (can't harvest but is a pumpkin entity)
				# Also check if it's a regular pumpkin that can't be harvested (might be dead)
				if entity_type == Entities.Dead_Pumpkin or (entity_type == Entities.Pumpkin and not can_harvest()):
					print("Found dead/dying pumpkin at", get_pos_x(), get_pos_y(), "- replanting")
					# Plant a new pumpkin (this automatically removes the dead one)
					if num_items(Items.Carrot) >= 1:
						plant(Entities.Pumpkin)
						print("Replanted pumpkin at", get_pos_x(), get_pos_y())
					else:
						# No carrots available, plant carrot instead
						plant(Entities.Carrot)
						print("Planted carrot (no carrots for pumpkin) at", get_pos_x(), get_pos_y())
				
				# Move to next row
				if row < get_world_size() - 1:
					move(North)
	
	# Return to starting position
	return_to_start()
