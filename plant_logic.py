def create_maze():
	clear()
	plant(Entities.Bush)
	while get_entity_type()==Entities.Bush:
			if num_items(Items.Weird_Substance) > get_world_size():
				use_item(Items.Weird_Substance, get_world_size())
				return 1
			if can_harvest():
				harvest()
				plant(Entities.Bush)
			if num_items(Items.Fertilizer)==0:
				# I do not have trade unlocked
				#trade(Items.Fertilizer)
				return 0
			
			use_item(Items.Fertilizer)

	return 1

def treasure_hunt():
	dir = West
	x = get_pos_x()
	y = get_pos_y()
	while True:
		move(dir)
		
		x2 = get_pos_x()
		y2 = get_pos_y()
		
		if x==x2 and y==y2:
			if dir==West:
				dir = North
			elif dir==North:
				dir = East
			elif dir==East:
				dir = South
			elif dir==South:
				dir = West
		else:
			x = get_pos_x()
			y = get_pos_y()
			
			if dir==West:
				dir = South
			elif dir==North:
				dir = West
			elif dir==East:
				dir = North
			elif dir==South:
				dir = East
		
		if get_entity_type()==Entities.Treasure:
			harvest()
			return 1