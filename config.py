# ===== FARM CONFIGURATION =====
# Configure which columns get which plants
# Any columns not specified will default to Grass
farm_config = {
	1: Entities.Tree,      # Column 1: Trees
	2: Entities.Carrot,    # Column 2: Carrots
	3: Entities.Carrot,    # Column 3: Carrots
	4: Entities.Carrot,    # Column 4: Carrots
	5: Entities.Pumpkin,   # Column 5: Pumpkins
	6: Entities.Pumpkin,   # Column 6: Pumpkins
	7: Entities.Pumpkin,   # Column 7: Pumpkins
}

# Hat colors for each plant type
hat_colors = {
	Entities.Grass: Hats.Green_Hat,
	Entities.Tree: Hats.Gray_Hat,
	Entities.Carrot: Hats.Purple_Hat,
	Entities.Pumpkin: Hats.Purple_Hat
}

# Ground type requirements for each plant
ground_requirements = {
	Entities.Grass: Grounds.Grassland,
	Entities.Tree: Grounds.Grassland,
	Entities.Carrot: Grounds.Soil,
	Entities.Pumpkin: Grounds.Soil
}
