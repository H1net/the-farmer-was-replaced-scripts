# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement

# ===== MAIN FARMING LOOP =====
while True:
	#print("Starting new farming cycle")
	
	# Do a flip at the beginning of each cycle
	do_a_flip()
	
	# Return to starting position (0,0) at the beginning of each cycle
	movement.return_to_start()
	
	# Check and replant any dead pumpkins before main harvesting
	movement.replant_dead_pumpkins()
	
	# Process each column based on configuration
	for column in range(get_world_size()):
		# Get the intended plant for this column, default to Grass if not specified
		if column in config.farm_config:
			intended_plant = config.farm_config[column]
		else:
			intended_plant = Entities.Grass
		
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
	
	# Pet the piggy at the end of each complete cycle
	pet_the_piggy()