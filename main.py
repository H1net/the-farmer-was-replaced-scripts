# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement

def create_maze():
	clear()
	
	for i in range(get_world_size()):
		plant(Entities.Bush)
		
		while get_water()<0.9:
			use_item(Items.Water)
		
		move(North)
	
	for i in range(get_world_size()):
		while can_harvest()==False:
			pass
		
		while get_entity_type()==Entities.Bush:
			if num_items(Items.Fertilizer)==0:
				trade(Items.Fertilizer)
				#if num_items(Items.Fertilizer)==0:
					#main()
			
			use_item(Items.Fertilizer)

	treasure_hunt()