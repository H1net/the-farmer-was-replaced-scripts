# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement
import state_manager
import unlock_planner

# Initialize systems
state_manager.initialize_farm_state()
unlock_planner.initialize_unlock_planner()

# ===== MAIN FARMING LOOP =====
while True:
	# Start timing measurements
	start_time = get_time()
	start_ticks = get_tick_count()
	
	#print("Starting new farming cycle")
	
	# Do a flip at the beginning of each cycle
	do_a_flip()
	
	# Return to starting position (0,0) at the beginning of each cycle
	movement.return_to_start()
	
	# Check and attempt to unlock current goal
	unlock_start_time = get_time()
	unlock_success = unlock_planner.check_and_attempt_unlock()
	unlock_end_time = get_time()
	
	# If we successfully unlocked something, optimize farm layout
	if unlock_success:
		unlock_planner.optimize_farm_for_current_unlock()
	
	# Check and replant any dead pumpkins before main harvesting (now state-aware!)
	pumpkin_start_time = get_time()
	movement.replant_dead_pumpkins()
	pumpkin_end_time = get_time()
	
	# Process each column based on configuration
	column_start_time = get_time()
	for column in range(get_world_size()):
		# Get the intended plant for this column, default to Grass if not specified
		if column in config.farm_config:
			intended_plant = config.farm_config[column]
		else:
			intended_plant = Entities.Grass
		
		#print("DEBUG: Processing column", column, "intended plant:", intended_plant)
		
		# Special handling for sunflowers
		if intended_plant == Entities.Sunflower:
			#print("DEBUG: Using special sunflower processing for column", column)
			plant_logic.process_sunflower_column()
		# Special handling for cacti
		elif intended_plant == Entities.Cactus:
			#print("DEBUG: Using special cactus processing for column", column)
			plant_logic.process_cactus_column()
		else:
			# Standard processing for other plants
			if intended_plant in config.ground_requirements:
				required_ground = config.ground_requirements[intended_plant]
			else:
				required_ground = Grounds.Grassland
				
			if intended_plant in config.hat_colors:
				hat_color = config.hat_colors[intended_plant]
			else:
				hat_color = Hats.Green_Hat
			
			#print("DEBUG: Using standard processing for column", column, "-", intended_plant)
			plant_logic.process_column(intended_plant, required_ground, hat_color)
		
		move(East)
	
	column_end_time = get_time()
	
	# Pet the piggy at the end of each complete cycle
	pet_the_piggy()
	
	# End timing measurements and report
	end_time = get_time()
	end_ticks = get_tick_count()
	
	cycle_time = end_time - start_time
	total_ticks = end_ticks - start_ticks
	if cycle_time > 0:
		ticks_per_second = total_ticks / cycle_time
	else:
		ticks_per_second = 0
	unlock_time = unlock_end_time - unlock_start_time
	pumpkin_time = pumpkin_end_time - pumpkin_start_time
	column_time = column_end_time - column_start_time
	
	quick_print("Cycle completed in " + str(cycle_time) + "s, " + str(total_ticks) + " ticks, " + str(ticks_per_second) + " ticks/s")
	quick_print("Unlock check: " + str(unlock_time) + "s, Dead pumpkin scan: " + str(pumpkin_time) + "s, Column processing: " + str(column_time) + "s")
	
	# Show unlock progress with enhanced information
	unlock_info = unlock_planner.get_unlock_debug_info()
	quick_print("🚀 " + unlock_info)