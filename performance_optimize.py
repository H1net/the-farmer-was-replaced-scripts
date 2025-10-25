# ===== PERFORMANCE OPTIMIZATION SYSTEM =====
# Lazy evaluation, batch operations, and advanced performance monitoring

import config
import state_manager
import movement
import resource_manager

# ===== LAZY EVALUATION SYSTEM =====

# Growth timers for each tile (tick count when planted)
growth_timers = {}

# Minimum growth times for different plants (in ticks)
growth_times = {
	Entities.Grass: 100,      # Fast growing
	Entities.Carrot: 200,     # Medium growth
	Entities.Pumpkin: 300,    # Slow growing
	Entities.Sunflower: 250,  # Medium growth
	Entities.Tree: 500,       # Very slow growing
	Entities.Cactus: 400,     # Slow growing
}

# Check if a tile needs to be checked based on growth timer
def should_check_tile(x, y):
	current_tick = get_tick_count()
	
	# If we don't have a timer for this tile, it needs checking
	if (x, y) not in growth_timers:
		return True
	
	planted_tick = growth_timers[(x, y)]
	time_since_planted = current_tick - planted_tick
	
	# Get the plant type to determine growth time
	if (x, y) in state_manager.farm_state:
		state = state_manager.farm_state[(x, y)]
		plant_type = state['actual_plant']
		
		if plant_type and plant_type in growth_times:
			required_time = growth_times[plant_type]
			# Only check if enough time has passed
			return time_since_planted >= required_time
	
	# Default to checking if we can't determine growth time
	return True

# Update growth timer when a tile is planted
def update_growth_timer(x, y):
	global growth_timers
	growth_timers[(x, y)] = get_tick_count()

# Get tiles that are ready for harvest based on growth timers
def get_ready_for_harvest_tiles():
	ready_tiles = []
	current_tick = get_tick_count()
	
	# Get list of all tiles with timers
	timer_items = []
	for pos in growth_timers:
		timer_items.append(pos)
	
	for pos in timer_items:
		x, y = pos
		planted_tick = growth_timers[pos]
		time_since_planted = current_tick - planted_tick
		
		# Check if this tile should be ready
		if (x, y) in state_manager.farm_state:
			state = state_manager.farm_state[(x, y)]
			plant_type = state['actual_plant']
			
			if plant_type and plant_type in growth_times:
				required_time = growth_times[plant_type]
				if time_since_planted >= required_time:
					ready_tiles.append((x, y))
	
	return ready_tiles

# ===== BATCH OPERATIONS SYSTEM =====

# Batch similar operations together
def batch_harvest_operations():
	# Get all tiles ready for harvest
	ready_tiles = get_ready_for_harvest_tiles()
	
	if not ready_tiles:
		return
	
	# Group by plant type for efficient processing
	harvest_groups = {}
	
	for x, y in ready_tiles:
		if (x, y) in state_manager.farm_state:
			state = state_manager.farm_state[(x, y)]
			plant_type = state['actual_plant']
			
			if plant_type:
				if plant_type in harvest_groups:
					harvest_groups[plant_type].append((x, y))
				else:
					harvest_groups[plant_type] = [(x, y)]
	
	# Process each group efficiently
	# Get list of plant types in harvest_groups
	group_items = []
	for plant_type in harvest_groups:
		group_items.append(plant_type)
	
	for plant_type in group_items:
		positions = harvest_groups[plant_type]
		if positions:
			# Add batch harvest task
			movement.add_task('batch_harvest', positions, plant_type, 1)
			quick_print("Batch harvest: " + str(len(positions)) + " " + str(plant_type) + " tiles ready")

# Batch tilling operations for efficiency
def batch_tilling_operations():
	# Find tiles that need tilling
	tilling_needed = []
	
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if (x, y) in state_manager.farm_state:
				state = state_manager.farm_state[(x, y)]
				intended_plant = state['intended_plant']
				
				if intended_plant and intended_plant in config.ground_requirements:
					required_ground = config.ground_requirements[intended_plant]
					current_ground = get_ground_type()
					
					if current_ground != required_ground:
						tilling_needed.append((x, y))
	
	# Add batch tilling task
	if tilling_needed:
		movement.add_task('batch_till', tilling_needed, None, 2)
		quick_print("Batch tilling: " + str(len(tilling_needed)) + " tiles need tilling")

# Batch hat changes for efficiency
def batch_hat_operations():
	# Group operations by required hat color
	hat_groups = {}
	
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if (x, y) in state_manager.farm_state:
				state = state_manager.farm_state[(x, y)]
				intended_plant = state['intended_plant']
				
				if intended_plant and intended_plant in config.hat_colors:
					hat_color = config.hat_colors[intended_plant]
					
					if hat_color in hat_groups:
						hat_groups[hat_color].append((x, y))
					else:
						hat_groups[hat_color] = [(x, y)]
	
	# Add hat change tasks
	# Get list of hat colors in hat_groups
	hat_items = []
	for hat_color in hat_groups:
		hat_items.append(hat_color)
	
	for hat_color in hat_items:
		positions = hat_groups[hat_color]
		if positions:
			movement.add_task('batch_hat_change', positions, hat_color, 3)
			quick_print("Batch hat change: " + str(len(positions)) + " tiles need " + str(hat_color))

# ===== PERFORMANCE MONITORING =====

# Performance metrics tracking
performance_metrics = {
	'tiles_checked': 0,
	'tiles_skipped': 0,
	'harvest_operations': 0,
	'plant_operations': 0,
	'movement_operations': 0,
	'batch_operations': 0,
	'total_cycles': 0,
	'average_cycle_time': 0,
	'efficiency_score': 0
}

# Update performance metrics
def update_performance_metrics(metric_name, value):
	global performance_metrics
	if metric_name in performance_metrics:
		performance_metrics[metric_name] += value
	else:
		performance_metrics[metric_name] = value

# Calculate efficiency score
def calculate_efficiency_score():
	global performance_metrics
	
	total_operations = performance_metrics['tiles_checked'] + performance_metrics['tiles_skipped']
	if total_operations == 0:
		return 0
	
	# Efficiency = percentage of operations that were necessary
	efficiency = (performance_metrics['tiles_checked'] / total_operations) * 100
	performance_metrics['efficiency_score'] = efficiency
	
	return efficiency

# Get comprehensive performance statistics
def get_performance_stats():
	global performance_metrics
	
	# Calculate current efficiency
	efficiency = calculate_efficiency_score()
	
	stats = {
		'total_cycles': performance_metrics['total_cycles'],
		'tiles_checked': performance_metrics['tiles_checked'],
		'tiles_skipped': performance_metrics['tiles_skipped'],
		'harvest_operations': performance_metrics['harvest_operations'],
		'plant_operations': performance_metrics['plant_operations'],
		'movement_operations': performance_metrics['movement_operations'],
		'batch_operations': performance_metrics['batch_operations'],
		'efficiency_score': efficiency,
		'average_cycle_time': performance_metrics['average_cycle_time']
	}
	
	return stats

# ===== OPTIMIZATION FUNCTIONS =====

# Optimize farm operations for current cycle
def optimize_farm_operations():
	# Check for batch operations
	batch_harvest_operations()
	batch_tilling_operations()
	batch_hat_operations()
	
	# Update performance metrics
	update_performance_metrics('batch_operations', 1)

# Skip unnecessary tile checks
def should_skip_tile_check(x, y):
	# Skip if tile was recently planted
	if not should_check_tile(x, y):
		update_performance_metrics('tiles_skipped', 1)
		return True
	
	# Skip if tile is in a stable state
	if (x, y) in state_manager.farm_state:
		state = state_manager.farm_state[(x, y)]
		# Skip if tile has been checked recently and is stable
		current_tick = get_tick_count()
		if current_tick - state['last_checked'] < 100:  # Skip if checked within last 100 ticks
			update_performance_metrics('tiles_skipped', 1)
			return True
	
	update_performance_metrics('tiles_checked', 1)
	return False

# Optimize movement patterns
def optimize_movement_pattern():
	# Get current position
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# Find the most efficient path through all pending tasks
	# This would integrate with the movement system's pathfinding
	# For now, we'll use the existing movement optimization
	
	# Update performance metrics
	update_performance_metrics('movement_operations', 1)

# ===== INTEGRATION FUNCTIONS =====

# Initialize performance optimization system
def initialize_performance_optimizer():
	global performance_metrics
	performance_metrics = {
		'tiles_checked': 0,
		'tiles_skipped': 0,
		'harvest_operations': 0,
		'plant_operations': 0,
		'movement_operations': 0,
		'batch_operations': 0,
		'total_cycles': 0,
		'average_cycle_time': 0,
		'efficiency_score': 0
	}
	quick_print("Performance Optimizer initialized")

# Update cycle metrics
def update_cycle_metrics(cycle_time):
	global performance_metrics
	performance_metrics['total_cycles'] += 1
	
	# Update average cycle time
	total_cycles = performance_metrics['total_cycles']
	current_avg = performance_metrics['average_cycle_time']
	new_avg = ((current_avg * (total_cycles - 1)) + cycle_time) / total_cycles
	performance_metrics['average_cycle_time'] = new_avg

# Get optimization recommendations
def get_optimization_recommendations():
	recommendations = []
	
	# Check efficiency score
	efficiency = calculate_efficiency_score()
	if efficiency < 70:
		recommendations.append("Low efficiency: Consider adjusting growth timers")
	
	# Check batch operation opportunities
	if performance_metrics['batch_operations'] < performance_metrics['total_cycles'] * 0.5:
		recommendations.append("More batch operations could improve performance")
	
	# Check movement optimization
	if performance_metrics['movement_operations'] > performance_metrics['total_cycles'] * 10:
		recommendations.append("High movement operations: Consider pathfinding optimization")
	
	return recommendations
	