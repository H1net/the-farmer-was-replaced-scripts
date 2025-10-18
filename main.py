# Helper function to harvest and plant a specific entity
def harvest_and_plant(entity, needs_tilling=False):
	if can_harvest():
		harvest()
		if needs_tilling and get_ground_type() != Grounds.Soil:
			till()
		plant(entity)
	else:
		if needs_tilling and get_ground_type() != Grounds.Soil:
			till()
		plant(entity)

# Helper function to process one row
def process_row(entity, needs_tilling=False):
	for j in range(get_world_size()):
		harvest_and_plant(entity, needs_tilling)
		move(North)
	do_a_flip()

# Main farming loop
while True:
	# Row 0: Bushes (no tilling needed)
	process_row(Entities.Bush, False)
	move(East)
	
	# Row 1: Carrots (need tilling)
	process_row(Entities.Carrot, True)
	move(East)
	
	# Row 2: Grass (no tilling needed)
	process_row(Entities.Grass, False)
	move(East)
	
	# Row 3: Grass (no tilling needed)
	process_row(Entities.Grass, False)
	move(East)