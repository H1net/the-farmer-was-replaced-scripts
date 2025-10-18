# ===== FARM CONFIGURATION =====
# Configure which columns get which plants
# Any columns not assigned will default to Bushes
farm_config = {
	Entities.Carrot: [1, 2],  # Carrots in columns 1 and 2
	Entities.Grass: [4, 5],    # Grass in columns 4 and 5
	# Columns 0 and 3 will default to Bushes
}

# Hat colors for each plant type
hat_colors = {
	Entities.Bush: Hats.Brown_Hat,
	Entities.Carrot: Hats.Purple_Hat,
	Entities.Grass: Hats.Green_Hat
}

# ===== HELPER FUNCTIONS =====
# Helper function to harvest and plant a specific entity
def harvest_and_plant(entity, needs_tilling=False):
	pos_x, pos_y = get_pos_x(), get_pos_y()
	
	# Water the ground if water level is low (below 0.5 for good growth)
	water_level = get_water()
	if water_level < 0.5 and num_items(Items.Water) > 0:
		use_item(Items.Water)
		#print("Watered ground at", pos_x, pos_y, "- water level:", water_level)
	
	if can_harvest():
		harvest()
		#print("Harvested at", pos_x, pos_y)
		if needs_tilling and get_ground_type() != Grounds.Soil:
			till()
			#print("Tilled soil at", pos_x, pos_y)
		plant(entity)
		#print("Planted", entity, "at", pos_x, pos_y)
	else:
		if needs_tilling and get_ground_type() != Grounds.Soil:
			till()
			#print("Tilled soil at", pos_x, pos_y)
		plant(entity)
		#print("Planted", entity, "at", pos_x, pos_y)

# Helper function to process one column
def process_column(entity, needs_tilling=False, hat_color=None):
	if hat_color:
		change_hat(hat_color)
		#print("Changed to", hat_color, "hat")
	
	for j in range(get_world_size()):
		harvest_and_plant(entity, needs_tilling)
		move(North)

# Function to determine what plant goes in each column
def get_plant_for_column(column):
	for entity, columns in farm_config.items():
		if column in columns:
			return entity
	return Entities.Bush  # Default to Bush

# Function to check if a plant needs tilling
def needs_tilling(entity):
	return entity == Entities.Carrot

# ===== MAIN FARMING LOOP =====
while True:
	#print("Starting new farming cycle")
	
	# Process each column based on configuration
	for column in range(get_world_size()):
		entity = get_plant_for_column(column)
		needs_till = needs_tilling(entity)
		hat_color = hat_colors.get(entity, Hats.Brown_Hat)
		
		#print("Processing column", column, "-", entity)
		process_column(entity, needs_till, hat_color)
		move(East)
	
	# Do a flip at the end of each complete cycle
	do_a_flip()