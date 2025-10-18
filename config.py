# ===== FARM CONFIGURATION =====
# Configure which columns get which plants
# Any columns not specified will default to Grass
farm_config = {
	0: Entities.Grass,     # Column 0: Grass (foundation resource)
	1: Entities.Grass,     # Column 1: Grass (hay production)
	2: Entities.Tree,      # Column 2: Trees
	3: Entities.Tree,      # Column 3: Trees
	4: Entities.Carrot,    # Column 4: Carrots
	5: Entities.Carrot,    # Column 5: Carrots
	6: Entities.Sunflower, # Column 6: Sunflowers
	7: Entities.Sunflower, # Column 7: Sunflowers
	8: Entities.Pumpkin,   # Column 8: Pumpkins
	9: Entities.Pumpkin,   # Column 9: Pumpkins
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
