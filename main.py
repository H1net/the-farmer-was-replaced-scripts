seed = Entities.Bush
do_till = False
while True:
	for i in range(get_world_size()):
		if(i==0):
			seed = Entities.Bush
			do_till = False
		elif(i==1):
			seed = Entities.Carrot
			do_till = True
		elif(i==2):
			seed = Entities.Carrot
			do_till = True
		else:
			seed = Entities.Grass
			do_till = False
		for j in range(get_world_size()):
			if can_harvest():
				harvest()
				if(do_till):
					till()
				plant(seed)
			else:
				plant(seed)
			move(North)
		do_a_flip()
		move(East)