import numpy as np
from PIL import Image

def create_color_map(normalized_noise_map, water_threshold):
    height, width = normalized_noise_map.shape
    color_map = np.zeros((height, width, 3), dtype=np.uint8)

    water_color = np.array([0, 0, 255])
    land_color = np.array([0, 255, 0])

    for y in range(height):
        for x in range(width):
            if normalized_noise_map[y][x] < water_threshold:
                color_map[y][x] = water_color
            else:
                color_map[y][x] = land_color

    return color_map

def color_map_to_image(color_map):
    return Image.fromarray(color_map, mode='RGB')


