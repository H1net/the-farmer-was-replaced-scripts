# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement

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
	
	# Check and replant any dead pumpkins before main harvesting
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
		
		# Special handling for sunflowers
		if intended_plant == Entities.Sunflower:
			#print("Processing sunflower column", column)
			plant_logic.process_sunflower_column()
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
			
			#print("Processing column", column, "-", intended_plant)
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
	pumpkin_time = pumpkin_end_time - pumpkin_start_time
	column_time = column_end_time - column_start_time
	
	quick_print("Cycle completed in {:.2f}s, {} ticks, {:.1f} ticks/s".format(cycle_time, total_ticks, ticks_per_second))
	quick_print("Dead pumpkin scan: {:.3f}s, Column processing: {:.3f}s".format(pumpkin_time, column_time))