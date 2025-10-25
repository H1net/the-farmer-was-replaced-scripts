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
			create_maze()