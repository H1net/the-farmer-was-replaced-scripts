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
			print("Tilled soil at", pos_x, pos_y)
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

# Main farming loop
while True:
	#print("Starting new farming cycle")
	
	# Column 0: Bushes (no tilling needed)
	#print("Processing Bush column")
	process_column(Entities.Bush, False, Hats.Brown_Hat)
	move(East)
	
	# Column 1: Carrots (need tilling)
	#print("Processing Carrot column")
	process_column(Entities.Carrot, True, Hats.Purple_Hat)
	move(East)
	
	# Column 2: Grass (no tilling needed)
	#print("Processing Grass column")
	process_column(Entities.Grass, False, Hats.Green_Hat)
	move(East)
	
	# Column 3: Grass (no tilling needed)
	#print("Processing Grass column")
	process_column(Entities.Grass, False, Hats.Green_Hat)
	move(East)
	
	# Do a flip at the end of each complete cycle
	do_a_flip()