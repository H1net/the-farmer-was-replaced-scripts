# Helper function to harvest and plant a specific entity
def harvest_and_plant(entity, required_ground_type=Grounds.Grassland):
	pos_x, pos_y = get_pos_x(), get_pos_y()
	
	# Water the ground if water level is low (below 0.5 for good growth)
	water_level = get_water()
	if water_level < 0.5 and num_items(Items.Water) > 0:
		use_item(Items.Water)
		#print("Watered ground at", pos_x, pos_y, "- water level:", water_level)
	
	# Check if ground needs to be changed to the required type
	current_ground = get_ground_type()
	if current_ground != required_ground_type:
		till()  # Till to change ground type
		#print("Changed ground to", required_ground_type, "at", pos_x, pos_y)
	
	if can_harvest():
		harvest()
		#print("Harvested at", pos_x, pos_y)
		plant(entity)
		#print("Planted", entity, "at", pos_x, pos_y)
	else:
		plant(entity)
		#print("Planted", entity, "at", pos_x, pos_y)

# Helper function to process one column
def process_column(entity, required_ground_type=Grounds.Grassland, hat_color=None):
	if hat_color:
		change_hat(hat_color)
		#print("Changed to", hat_color, "hat")
	
	for j in range(get_world_size()):
		harvest_and_plant(entity, required_ground_type)
		move(North)

# Function to move back to starting position (0,0)
def return_to_start():
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# Move west to get to x=0
	for i in range(current_x):
		move(West)
	
	# Move south to get to y=0  
	for i in range(current_y):
		move(South)

# Main farming loop
while True:
	#print("Starting new farming cycle")
	
	# Return to starting position (0,0) at the beginning of each cycle
	return_to_start()
	
	# Column 0: Pumpkins (need soil)
	#print("Processing Pumpkin column")
	process_column(Entities.Pumpkin, Grounds.Soil, Hats.Purple_Hat)
	move(East)
	
	# Column 1: Pumpkins (need soil)
	#print("Processing Pumpkin column")
	process_column(Entities.Pumpkin, Grounds.Soil, Hats.Purple_Hat)
	move(East)
	
	# Column 2: Carrots (need soil)
	#print("Processing Carrot column")
	process_column(Entities.Carrot, Grounds.Soil, Hats.Purple_Hat)
	move(East)
	
	# Column 3: Trees (grow on grassland)
	#print("Processing Tree column")
	process_column(Entities.Tree, Grounds.Grassland, Hats.Gray_Hat)
	move(East)
	
	# Column 4: Bushes (grow on grassland)
	#print("Processing Bush column")
	process_column(Entities.Bush, Grounds.Grassland, Hats.Brown_Hat)
	move(East)
	
	# Column 5: Grass (grow on grassland)
	#print("Processing Grass column")
	process_column(Entities.Grass, Grounds.Grassland, Hats.Green_Hat)
	move(East)
	
	# Do a flip at the end of each complete cycle
	do_a_flip()