import numpy as np

def erode_map(elevation_map, iterations, water_amount, evaporation_rate, sediment_capacity):
    height, width = elevation_map.shape
    water_map = np.zeros((height, width))
    sediment_map = np.zeros((height, width))

    for _ in range(iterations):
        # Add water
        water_map += water_amount

        # Calculate flow direction
        flow_dir = np.zeros((height, width, 2))
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                min_height = elevation_map[y][x] + water_map[y][x]
                min_pos = (0, 0)

                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue

                        height_neighbor = elevation_map[y + dy][x + dx] + water_map[y + dy][x + dx]
                        if height_neighbor < min_height:
                            min_height = height_neighbor
                            min_pos = (dy, dx)

                flow_dir[y][x] = min_pos

        # Move water and sediment
        new_water_map = np.zeros((height, width))
        new_sediment_map = np.zeros((height, width))
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                dy, dx = flow_dir[y][x]
                new_y, new_x = y + int(dy), x + int(dx)

                # Move water
                water_to_move = water_map[y][x] * (1 - evaporation_rate)
                new_water_map[new_y][new_x] += water_to_move
                new_water_map[y][x] -= water_to_move

                # Move sediment
                sediment_capacity_here = water_to_move * sediment_capacity
                sediment_to_move = min(sediment_map[y][x], sediment_capacity_here)
                new_sediment_map[new_y][new_x] += sediment_to_move
                new_sediment_map[y][x] -= sediment_to_move
                elevation_map[y][x] += sediment_map[y][x] - sediment_to_move

        water_map = new_water_map
        sediment_map = new_sediment_map

    return elevation_map
