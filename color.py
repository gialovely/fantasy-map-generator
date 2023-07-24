import numpy as np
from PIL import Image

def create_color_map(normalized_noise_map, water_threshold):
    height, width = normalized_noise_map.shape
    color_map = np.zeros((height, width, 3), dtype=np.uint8)

    water_color = np.array([0, 0, 255])

    for y in range(height):
        for x in range(width):
            value = normalized_noise_map[y][x]
            if value < water_threshold:
                color_map[y][x] = water_color
            else:
                # Introduce gradation for land based on height
                shade = int(255 * (value - water_threshold) / (1 - water_threshold))
                color_map[y][x] = np.array([0, shade, 0])

    return color_map

def create_difference_color_map(difference_map):
    height, width = difference_map.shape
    color_map = np.zeros((height, width, 3), dtype=np.uint8)
    
    eroded_color = np.array([255, 0, 0])  # Red for eroded areas
    deposited_color = np.array([0, 0, 255])  # Blue for deposited areas

    for y in range(height):
        for x in range(width):
            if difference_map[y][x] > 0:
                color_map[y][x] = eroded_color
            elif difference_map[y][x] < 0:
                color_map[y][x] = deposited_color
            
    return color_map



def color_map_to_image(color_map):
    return Image.fromarray(color_map, mode='RGB')


