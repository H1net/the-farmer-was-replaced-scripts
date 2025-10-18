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

# Function to check and replant dead pumpkins (state-aware version)
def replant_dead_pumpkins():
	import state_manager
	
	# Store current position
	start_x, start_y = get_pos_x(), get_pos_y()
	
	# Get all known pumpkin positions from state
	pumpkin_positions = state_manager.get_tiles_by_plant(Entities.Pumpkin)
	
	# Also check intended pumpkin positions that might not be in state yet
	intended_pumpkin_positions = state_manager.get_tiles_by_intended_plant(Entities.Pumpkin)
	
	# Combine and deduplicate positions
	all_pumpkin_positions = list(set(pumpkin_positions + intended_pumpkin_positions))
	
	quick_print("Checking " + str(len(all_pumpkin_positions)) + " known pumpkin positions for dead pumpkins")
	
	# Check each known pumpkin position
	for (x, y) in all_pumpkin_positions:
		# Move to this position
		move_to_position(x, y)
		
		entity_type = get_entity_type()
		
		# Check if it's a dead pumpkin (can't harvest but is a pumpkin entity)
		# Also check if it's a regular pumpkin that can't be harvested (might be dead)
		if entity_type == Entities.Dead_Pumpkin or (entity_type == Entities.Pumpkin and not can_harvest()):
			quick_print("Found dead/dying pumpkin at " + str(x) + "," + str(y) + " - replanting")
			# Plant a new pumpkin (this automatically removes the dead one)
			if num_items(Items.Carrot) >= 1:
				plant(Entities.Pumpkin)
				quick_print("Replanted pumpkin at " + str(x) + "," + str(y))
				# Update state
				state_manager.update_tile_state(x, y, actual_plant=Entities.Pumpkin, needs_attention=False)
			else:
				# No carrots available, plant carrot instead
				plant(Entities.Carrot)
				quick_print("Planted carrot (no carrots for pumpkin) at " + str(x) + "," + str(y))
				# Update state
				state_manager.update_tile_state(x, y, actual_plant=Entities.Carrot, needs_attention=True)
	
	# Return to starting position
	return_to_start()

# Helper function to move to a specific position
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
