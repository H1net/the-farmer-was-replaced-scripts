# ===== MAIN FARMING SCRIPT =====
# Import configuration and helper modules
import config
import plant_logic
import movement
import state_manager
import unlock_planner
import resource_manager
import performance_optimize

# Initialize systems
state_manager.initialize_farm_state()
unlock_planner.initialize_unlock_planner()
resource_manager.initialize_resource_manager()
performance_optimize.initialize_performance_optimizer()

# ===== MAIN FARMING LOOP =====
while True:
	# Start timing measurements
	start_time = get_time()
	start_ticks = get_tick_count()
	
	#print("Starting new farming cycle")
	
	# Do a flip at the beginning of each cycle
	do_a_flip()
	
	# Return to starting position (0,0) at the beginning of each cycle
	movement.return_to_start()
	
	# Check and attempt to unlock current goal
	unlock_start_time = get_time()
	unlock_success = unlock_planner.check_and_attempt_unlock()
	unlock_end_time = get_time()
	
	# If we successfully unlocked something, optimize farm layout
	if unlock_success:
		unlock_planner.optimize_farm_for_current_unlock()
	
	# Check for resource management needs
	resource_start_time = get_time()
	resource_emergency = resource_manager.implement_emergency_production()
	resource_end_time = get_time()
	
	# Check and replant any dead pumpkins using intelligent movement
	pumpkin_start_time = get_time()
	movement.replant_dead_pumpkins()
	pumpkin_end_time = get_time()
	
	# Execute all pending tasks with pathfinding optimization
	task_start_time = get_time()
	movement.execute_all_pending_tasks()
	task_end_time = get_time()
	
	# Optimize farm operations for performance
	optimization_start_time = get_time()
	performance_optimize.optimize_farm_operations()
	optimization_end_time = get_time()
	
	# The new intelligent task-based system handles all farming operations
	# The old column-by-column approach is now replaced by:
	# 1. Task queue system (movement.py) - handles all harvesting and planting
	# 2. State management (state_manager.py) - tracks what's planted where
	# 3. Resource management (resource_manager.py) - handles resource needs
	# 4. Performance optimization (performance_optimize.py) - optimizes operations
	# 5. Unlock planning (unlock_planner.py) - manages progression
	
	# The system now works by:
	# - Adding tasks to the queue based on farm state
	# - Executing tasks with optimal pathfinding
	# - Managing resources proactively
	# - Optimizing performance with lazy evaluation
	
	# No more manual column processing needed!
	column_start_time = get_time()
	# Task-based system handles everything automatically
	column_end_time = get_time()
	
	# Pet the piggy at the end of each complete cycle
	pet_the_piggy()
	
	# End timing measurements and report
	end_time = get_time()
	end_ticks = get_tick_count()
	
	cycle_time = end_time - start_time
	total_ticks = end_ticks - start_ticks
	if cycle_time > 0:
		ticks_per_second = total_ticks / cycle_time
	else:
		ticks_per_second = 0
	unlock_time = unlock_end_time - unlock_start_time
	resource_time = resource_end_time - resource_start_time
	pumpkin_time = pumpkin_end_time - pumpkin_start_time
	task_time = task_end_time - task_start_time
	optimization_time = optimization_end_time - optimization_start_time
	column_time = column_end_time - column_start_time
	
	quick_print("Cycle completed in " + str(cycle_time) + "s, " + str(total_ticks) + " ticks, " + str(ticks_per_second) + " ticks/s")
	quick_print("Unlock: " + str(unlock_time) + "s, Resources: " + str(resource_time) + "s, Dead pumpkins: " + str(pumpkin_time) + "s, Tasks: " + str(task_time) + "s, Optimization: " + str(optimization_time) + "s, Columns: " + str(column_time) + "s")
	
	# Show unlock progress with enhanced information
	unlock_info = unlock_planner.get_unlock_debug_info()
	quick_print("🚀 " + unlock_info)
	
	# Show resource management status
	if resource_emergency:
		quick_print("⚠️  EMERGENCY: Resource production boost activated")
	
	# Show resource statistics every 10 cycles
	cycle_count = get_tick_count() // 1000  # Approximate cycle count
	if cycle_count % 10 == 0:
		resource_stats = resource_manager.get_resource_stats()
		quick_print("📊 Resource Status: Hay=" + str(resource_stats['current_resources'][Items.Hay]) + 
					" Wood=" + str(resource_stats['current_resources'][Items.Wood]) + 
					" Carrot=" + str(resource_stats['current_resources'][Items.Carrot]) + 
					" Power=" + str(resource_stats['current_resources'][Items.Power]))
	
	# Show performance statistics every 20 cycles
	if cycle_count % 20 == 0:
		performance_stats = performance_optimize.get_performance_stats()
		quick_print("⚡ Performance: Efficiency=" + str(performance_stats['efficiency_score']) + 
					"% TilesChecked=" + str(performance_stats['tiles_checked']) + 
					" TilesSkipped=" + str(performance_stats['tiles_skipped']) + 
					" BatchOps=" + str(performance_stats['batch_operations']))
		
		# Update cycle metrics
		performance_optimize.update_cycle_metrics(cycle_time)