import numpy as np

def erode_map(elevation_map, iterations, water_amount, evaporation_rate, sediment_capacity_factor):
    height, width = elevation_map.shape
    sediment_map = np.zeros_like(elevation_map)
    
    for _ in range(iterations):
        # Rainfall
        water_map = np.full_like(elevation_map, water_amount)
        
        for _ in range(5):  # Multiple smaller steps for stability
            # Calculate Flow Direction & Water Flow
            flow_directions = calculate_flow_direction(elevation_map + water_map)
            
            new_water_map = np.zeros_like(water_map)
            for y in range(1, height-1):
                for x in range(1, width-1):
                    dx, dy = flow_directions[y, x]
                    if dx != 0 or dy != 0:
                        flow_amount = water_map[y, x] * 0.1  # 10% of the water flows
                        new_water_map[y+dy, x+dx] += flow_amount
                        new_water_map[y, x] -= flow_amount
            
                        # Erosion & Deposition
                        slope = elevation_map[y, x] - elevation_map[y+dy, x+dx]
                        sediment_capacity = slope * flow_amount * sediment_capacity_factor
                        sediment_difference = sediment_capacity - sediment_map[y, x]
                        erosion_amount = min(water_map[y, x], sediment_difference, slope)
                        
                        elevation_map[y, x] -= erosion_amount
                        elevation_map[y+dy, x+dx] += erosion_amount

                        sediment_map[y, x] += erosion_amount
                        sediment_map[y, x] -= erosion_amount * 0.1  # Some sediment is left behind
            
            water_map = new_water_map * (1 - evaporation_rate)
            
    return elevation_map

def calculate_flow_direction(elevation_map):
    height, width = elevation_map.shape
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # N, W, S, E
    flow_directions = np.zeros((height, width, 2), dtype=int)
    
    for y in range(1, height-1):
        for x in range(1, width-1):
            min_height = elevation_map[y, x]
            min_dir = (0, 0)
            for dx, dy in directions:
                if elevation_map[y+dy, x+dx] < min_height:
                    min_height = elevation_map[y+dy, x+dx]
                    min_dir = (dx, dy)
            flow_directions[y, x] = min_dir
            
    return flow_directions


