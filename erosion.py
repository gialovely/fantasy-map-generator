import numpy as np

def compute_flow_direction(elevation_map, water_map):
    """
    Compute the flow direction for each cell in the elevation map using vectorized operations.
    The function returns a flow direction map where each entry is a tuple (dy, dx).
    """
    height, width = elevation_map.shape
    
    # Extend the elevation map and water map by padding zeros around them
    extended_elevation = np.pad(elevation_map + water_map, pad_width=1, mode='constant', constant_values=0)
    
    # Create slices for each neighbor
    central = extended_elevation[1:-1, 1:-1]
    top = extended_elevation[:-2, 1:-1]
    bottom = extended_elevation[2:, 1:-1]
    left = extended_elevation[1:-1, :-2]
    right = extended_elevation[1:-1, 2:]
    top_left = extended_elevation[:-2, :-2]
    top_right = extended_elevation[:-2, 2:]
    bottom_left = extended_elevation[2:, :-2]
    bottom_right = extended_elevation[2:, 2:]
    
    # Find the minimum neighboring elevation for each cell
    min_neighbor = np.min(np.array([top, bottom, left, right, top_left, top_right, bottom_left, bottom_right]), axis=0)
    
    # Compute the flow direction based on the minimum neighbor
    flow_dir = np.zeros((height, width, 2), dtype=int)
    flow_dir[(top == min_neighbor) & (central > top)] = (-1, 0)
    flow_dir[(bottom == min_neighbor) & (central > bottom)] = (1, 0)
    flow_dir[(left == min_neighbor) & (central > left)] = (0, -1)
    flow_dir[(right == min_neighbor) & (central > right)] = (0, 1)
    flow_dir[(top_left == min_neighbor) & (central > top_left)] = (-1, -1)
    flow_dir[(top_right == min_neighbor) & (central > top_right)] = (-1, 1)
    flow_dir[(bottom_left == min_neighbor) & (central > bottom_left)] = (1, -1)
    flow_dir[(bottom_right == min_neighbor) & (central > bottom_right)] = (1, 1)
    
    return flow_dir

def move_water_and_sediment(elevation_map, water_map, sediment_map, flow_dir, evaporation_rate, sediment_capacity):
    """
    Move water and sediment based on the flow directions using vectorized operations.
    """
    height, width = elevation_map.shape
    
    # Initialize new water and sediment maps
    new_water_map = np.zeros((height, width))
    new_sediment_map = np.zeros((height, width))
    
    # Calculate coordinates for source and destination
    y_coords, x_coords = np.indices((height, width))
    dest_y_coords = np.clip(y_coords + flow_dir[..., 0], 0, height - 1)
    dest_x_coords = np.clip(x_coords + flow_dir[..., 1], 0, width - 1)
    
    # Move water
    water_to_move = water_map * (1 - evaporation_rate)
    np.add.at(new_water_map, (dest_y_coords, dest_x_coords), water_to_move)
    new_water_map -= water_to_move
    
    # Move sediment
    sediment_capacity_here = water_to_move * sediment_capacity
    sediment_to_move = np.minimum(sediment_map, sediment_capacity_here)
    np.add.at(new_sediment_map, (dest_y_coords, dest_x_coords), sediment_to_move)
    new_sediment_map -= sediment_to_move
    elevation_map = elevation_map.astype(float)  # Convert to float for the operation
    elevation_map += sediment_map - sediment_to_move
    
    return new_water_map, new_sediment_map

def erode_map(elevation_map, iterations, water_amount, evaporation_rate, sediment_capacity):
    """
    Simulate the erosion of an elevation map using water and sediment movement with optimized vectorized operations.
    """
    height, width = elevation_map.shape
    water_map = np.zeros((height, width))
    sediment_map = np.zeros((height, width))
    
    for _ in range(iterations):
        # Add water
        water_map += water_amount
        
        # Calculate flow direction
        flow_dir = compute_flow_direction(elevation_map, water_map)
        
        # Move water and sediment
        water_map, sediment_map = move_water_and_sediment(elevation_map, water_map, sediment_map, 
                                                          flow_dir, evaporation_rate, sediment_capacity)
    
    return elevation_map
