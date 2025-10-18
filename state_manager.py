# ===== FARM STATE MANAGEMENT =====
# Tracks what's planted where and farm state for efficient operations

# Global farm state dictionary
farm_state = {}

# Initialize farm state for all tiles
def initialize_farm_state():
	global farm_state
	farm_state = {}
	
	# Initialize all tiles in the farm
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			farm_state[(x, y)] = {
				'intended_plant': None,
				'actual_plant': None,
				'last_checked': 0,
				'needs_attention': False,
				'ground_type': None
			}

# Update state for a specific tile
def update_tile_state(x, y, intended_plant, actual_plant, ground_type, needs_attention):
	global farm_state
	
	if (x, y) not in farm_state:
		farm_state[(x, y)] = {
			'intended_plant': None,
			'actual_plant': None,
			'last_checked': 0,
			'needs_attention': False,
			'ground_type': None
		}
	
	current_tick = get_tick_count()
	
	# Update all provided values
	farm_state[(x, y)]['intended_plant'] = intended_plant
	farm_state[(x, y)]['actual_plant'] = actual_plant
	farm_state[(x, y)]['ground_type'] = ground_type
	farm_state[(x, y)]['last_checked'] = current_tick
	farm_state[(x, y)]['needs_attention'] = needs_attention

# Get all tiles with a specific plant type
def get_tiles_by_plant(plant_type):
	positions = []
	for (x, y), state in farm_state.items():
		if state['actual_plant'] == plant_type:
			positions.append((x, y))
	return positions

# Get all tiles that need attention (resource fallbacks)
def get_tiles_needing_attention():
	positions = []
	for (x, y), state in farm_state.items():
		if state['needs_attention']:
			positions.append((x, y))
	return positions

# Get tiles with specific intended plant
def get_tiles_by_intended_plant(plant_type):
	positions = []
	for (x, y), state in farm_state.items():
		if state['intended_plant'] == plant_type:
			positions.append((x, y))
	return positions

# Check if a tile needs attention (resource fallback)
def tile_needs_attention(x, y):
	if (x, y) in farm_state:
		return farm_state[(x, y)]['needs_attention']
	return False

# Mark a tile as needing attention
def mark_tile_attention(x, y, needs_attention=True):
	if (x, y) in farm_state:
		farm_state[(x, y)]['needs_attention'] = needs_attention

# Get state for a specific tile
def get_tile_state(x, y):
	if (x, y) in farm_state:
		return farm_state[(x, y)]
	return None

# Scan and update state for a specific tile (verify what's actually there)
def scan_tile_state(x, y):
	# This would require moving to the tile and checking
	# For now, return the stored state
	# TODO: Implement actual scanning when at the tile
	return get_tile_state(x, y)

# Get all tiles that haven't been checked recently
def get_stale_tiles(max_age_ticks=1000):
	current_tick = get_tick_count()
	stale_tiles = []
	
	for (x, y), state in farm_state.items():
		if current_tick - state['last_checked'] > max_age_ticks:
			stale_tiles.append((x, y))
	
	return stale_tiles

# Clear all state (for fresh start)
def clear_farm_state():
	global farm_state
	farm_state = {}

# Debug: Print current farm state
def debug_print_state():
	quick_print("=== FARM STATE DEBUG ===")
	for (x, y), state in farm_state.items():
		if state['actual_plant'] != None or state['needs_attention']:
			quick_print("(" + str(x) + "," + str(y) + ") intended:" + str(state['intended_plant']) + 
						" actual:" + str(state['actual_plant']) + 
						" attention:" + str(state['needs_attention']))
