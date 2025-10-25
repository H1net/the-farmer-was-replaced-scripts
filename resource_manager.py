# ===== ADVANCED RESOURCE MANAGEMENT =====
# Proactive resource buffering and multi-crop optimization

import config
import state_manager
import unlock_planner

# ===== RESOURCE BUFFER SYSTEM =====

# Minimum resource thresholds to maintain
resource_buffers = {
	Items.Hay: 50,      # Minimum hay to maintain
	Items.Wood: 25,      # Minimum wood to maintain
	Items.Carrot: 10,    # Minimum carrots to maintain
	Items.Power: 5,      # Minimum power to maintain
}

# Emergency fallback thresholds (when resources are critically low)
emergency_thresholds = {
	Items.Hay: 10,
	Items.Wood: 5,
	Items.Carrot: 3,
	Items.Power: 1,
}

# Resource production rates (estimated)
production_rates = {
	Items.Hay: 1.0,      # Grass produces hay
	Items.Wood: 0.5,      # Trees produce wood
	Items.Carrot: 0.8,    # Carrots produce carrots
	Items.Power: 0.3,     # Sunflowers produce power
}

# Check if we have sufficient resources for current needs
def check_resource_adequacy():
	adequate = True
	low_resources = []
	
	# Check buffer thresholds
	# Get list of items in resource_buffers dictionary
	buffer_items = []
	for item in resource_buffers:
		buffer_items.append(item)
	
	for item in buffer_items:
		required = resource_buffers[item]
		available = num_items(item)
		if available < required:
			adequate = False
			low_resources.append((item, available, required))
	
	return adequate, low_resources

# Check for emergency resource situations
def check_emergency_resources():
	emergencies = []
	
	# Get list of items in emergency_thresholds dictionary
	emergency_items = []
	for item in emergency_thresholds:
		emergency_items.append(item)
	
	for item in emergency_items:
		threshold = emergency_thresholds[item]
		available = num_items(item)
		if available < threshold:
			emergencies.append((item, available, threshold))
	
	return emergencies

# Get resource production recommendations
def get_production_recommendations():
	recommendations = []
	
	# Check current unlock requirements
	current_unlock = unlock_planner.get_current_unlock_goal()
	if current_unlock:
		requirements = unlock_planner.get_current_unlock_requirements()
		if requirements:
			# Get list of required items
			req_items = []
			for item in requirements:
				req_items.append(item)
			
			for item in req_items:
				needed = requirements[item]
				have = num_items(item)
				if have < needed:
					recommendation = {
						'item': item,
						'needed': needed,
						'have': have,
						'priority': 'high',
						'reason': 'unlock_requirement'
					}
					recommendations.append(recommendation)
	
	# Check buffer requirements
	adequate, low_resources = check_resource_adequacy()
	if not adequate:
		for item, available, required in low_resources:
			recommendation = {
				'item': item,
				'needed': required,
				'have': available,
				'priority': 'medium',
				'reason': 'buffer_maintenance'
			}
			recommendations.append(recommendation)
	
	# Check emergency situations
	emergencies = check_emergency_resources()
	for item, available, threshold in emergencies:
		recommendation = {
			'item': item,
			'needed': threshold,
			'have': available,
			'priority': 'critical',
			'reason': 'emergency_threshold'
		}
		recommendations.append(recommendation)
	
	return recommendations

# ===== MULTI-CROP OPTIMIZATION =====

# Calculate polyculture bonus potential
def calculate_polyculture_potential():
	# Count different plant types on farm
	plant_counts = {}
	
	# Get all planted positions
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if (x, y) in state_manager.farm_state:
				state = state_manager.farm_state[(x, y)]
				actual_plant = state['actual_plant']
				if actual_plant:
					if actual_plant in plant_counts:
						plant_counts[actual_plant] += 1
					else:
						plant_counts[actual_plant] = 1
	
	# Calculate diversity score
	diversity_score = len(plant_counts)
	
	# Check for polyculture bonus potential
	polyculture_bonus = 0
	if diversity_score >= 3:
		polyculture_bonus = 0.1  # 10% bonus for 3+ different crops
	if diversity_score >= 5:
		polyculture_bonus = 0.2  # 20% bonus for 5+ different crops
	
	return {
		'diversity_score': diversity_score,
		'polyculture_bonus': polyculture_bonus,
		'plant_counts': plant_counts
	}

# Optimize farm layout for resource production
def optimize_farm_for_resources():
	recommendations = get_production_recommendations()
	
	if not recommendations:
		return config.farm_config
	
	# Sort recommendations by priority
	priority_order = {'critical': 1, 'high': 2, 'medium': 3, 'low': 4}
	
	# Simple bubble sort for compatibility
	for i in range(len(recommendations)):
		for j in range(len(recommendations) - 1 - i):
			# Get priority values manually
			priority1 = 5  # Default
			if recommendations[j]['priority'] in priority_order:
				priority1 = priority_order[recommendations[j]['priority']]
			
			priority2 = 5  # Default
			if recommendations[j + 1]['priority'] in priority_order:
				priority2 = priority_order[recommendations[j + 1]['priority']]
			
			if priority1 > priority2:
				# Swap recommendations
				temp = recommendations[j]
				recommendations[j] = recommendations[j + 1]
				recommendations[j + 1] = temp
	
	# Generate optimized farm layout
	optimized_config = {}
	
	# Start with current config
	for column in config.farm_config:
		optimized_config[column] = config.farm_config[column]
	
	# Adjust based on highest priority needs
	for rec in recommendations:
		if rec['priority'] == 'critical':
			# Emergency: prioritize this resource
			item = rec['item']
			plant = get_best_plant_for_resource(item)
			if plant:
				# Find empty columns to prioritize this plant
				for column in range(get_world_size()):
					if column not in optimized_config:
						optimized_config[column] = plant
						break
	
	return optimized_config

# Get the best plant for producing a specific resource
def get_best_plant_for_resource(resource):
	if resource == Items.Hay:
		return Entities.Grass
	elif resource == Items.Wood:
		return Entities.Tree
	elif resource == Items.Carrot:
		return Entities.Carrot
	elif resource == Items.Power:
		return Entities.Sunflower
	else:
		return Entities.Grass  # Default fallback

# ===== RESOURCE STARVATION PREVENTION =====

# Check for resource starvation risks
def check_starvation_risks():
	risks = []
	
	# Check if we're running low on essential resources
	essential_resources = [Items.Hay, Items.Wood, Items.Carrot]
	
	for resource in essential_resources:
		available = num_items(resource)
		if available < 5:  # Very low threshold
			risks.append({
				'resource': resource,
				'available': available,
				'risk_level': 'high',
				'action': 'immediate_production_boost'
			})
	
	return risks

# Implement emergency resource production
def implement_emergency_production():
	risks = check_starvation_risks()
	
	if not risks:
		return False
	
	quick_print("EMERGENCY: Implementing resource production boost")
	
	# For each risk, boost production of that resource
	for risk in risks:
		resource = risk['resource']
		plant = get_best_plant_for_resource(resource)
		
		if plant:
			quick_print("Boosting " + str(resource) + " production with " + str(plant))
			# This would trigger immediate planting of the resource plant
			# Implementation would depend on integration with main farming loop
	
	return True

# ===== RESOURCE STATISTICS =====

# Get comprehensive resource statistics
def get_resource_stats():
	stats = {
		'current_resources': {},
		'buffer_status': {},
		'production_recommendations': [],
		'polyculture_info': {},
		'starvation_risks': []
	}
	
	# Current resource levels
	all_items = [Items.Hay, Items.Wood, Items.Carrot, Items.Power]
	for item in all_items:
		stats['current_resources'][item] = num_items(item)
	
	# Buffer status
	# Get list of items in resource_buffers dictionary
	buffer_items = []
	for item in resource_buffers:
		buffer_items.append(item)
	
	for item in buffer_items:
		required = resource_buffers[item]
		available = num_items(item)
		status_info = {
			'required': required,
			'available': available,
			'adequate': available >= required
		}
		stats['buffer_status'][item] = status_info
	
	# Production recommendations
	stats['production_recommendations'] = get_production_recommendations()
	
	# Polyculture information
	stats['polyculture_info'] = calculate_polyculture_potential()
	
	# Starvation risks
	stats['starvation_risks'] = check_starvation_risks()
	
	return stats

# Initialize resource management system
def initialize_resource_manager():
	quick_print("Resource Manager initialized")
	quick_print("Buffer thresholds: " + str(resource_buffers))
	quick_print("Emergency thresholds: " + str(emergency_thresholds))
