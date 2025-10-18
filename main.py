# Helper function to harvest and plant a specific entity
def harvest_and_plant(entity, needs_tilling=False):
	pos_x, pos_y = get_pos_x(), get_pos_y()
	
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
			print("Tilled soil at", pos_x, pos_y)
		plant(entity)
		#print("Planted", entity, "at", pos_x, pos_y)

# Helper function to process one row
def process_row(entity, needs_tilling=False, hat_color=None):
	if hat_color:
		change_hat(hat_color)
		#print("Changed to", hat_color, "hat")
	
	for j in range(get_world_size()):
		harvest_and_plant(entity, needs_tilling)
		move(North)
	do_a_flip()

# Main farming loop
while True:
	print("Starting new farming cycle")
	
	# Row 0: Bushes (no tilling needed)
	print("Processing Bush row")
	process_row(Entities.Bush, False, Hats.Brown_Hat)
	move(East)
	
	# Row 1: Carrots (need tilling)
	print("Processing Carrot row")
	process_row(Entities.Carrot, True, Hats.Purple_Hat)
	move(East)
	
	# Row 2: Grass (no tilling needed)
	print("Processing Grass row")
	process_row(Entities.Grass, False, Hats.Green_Hat)
	move(East)
	
	# Row 3: Grass (no tilling needed)
	print("Processing Grass row")
	process_row(Entities.Grass, False, Hats.Green_Hat)
	move(East)