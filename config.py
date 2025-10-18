# ===== FARM CONFIGURATION =====
# Configure which columns get which plants
# Any columns not specified will default to Grass
farm_config = {
	0: Entities.Grass,
	1: Entities.Grass, 
	2: Entities.Pumpkin,
	3: Entities.Pumpkin,
	4: Entities.Tree,
	5: Entities.Tree,
	6: Entities.Carrot,
	7: Entities.Carrot, 
	8: Entities.Pumpkin,  
	9: Entities.Pumpkin,   
	10: Entities.Pumpkin,   
	11: Entities.Sunflower,   
	# Any additional columns default to Grass for hay production
}

# Hat colors for each plant type
hat_colors = {
	Entities.Grass: Hats.Green_Hat,
	Entities.Tree: Hats.Gray_Hat,
	Entities.Carrot: Hats.Purple_Hat,
	Entities.Sunflower: Hats.Brown_Hat,
	Entities.Pumpkin: Hats.Purple_Hat
}

# Ground type requirements for each plant
ground_requirements = {
	Entities.Grass: Grounds.Grassland,
	Entities.Tree: Grounds.Grassland,
	Entities.Carrot: Grounds.Soil,
	Entities.Sunflower: Grounds.Soil,
	Entities.Pumpkin: Grounds.Soil
}

# Sunflower harvesting configuration
sunflower_harvest_threshold = 10  # Minimum sunflowers before optimal harvesting

# Maps items to plants that produce them
resource_producers = {
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Bush,  # Could also be Tree, but Bush is simpler
	Items.Carrot: Entities.Carrot
}
