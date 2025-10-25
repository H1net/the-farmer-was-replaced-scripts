# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement

# from plant_logic import create_maze, treasure_hunt

times = 30

#for i in range(times):
	
	#create_maze()
	#treasure_hunt()

while True:
	if plant_logic.create_maze():
		if plant_logic.treasure_hunt():
			continue
