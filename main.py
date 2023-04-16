from map_noise import generate_noise_map, normalize_noise_map
from color import create_color_map, color_map_to_image
from erosion import erode_map
import numpy as np

width, height = 512, 512
scale = 6
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = 2

noise_map = generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
normalized_noise_map = normalize_noise_map(noise_map)

iterations = 10
water_amount = 0.01
evaporation_rate = 0.1
sediment_capacity = 0.1
eroded_map = erode_map(normalized_noise_map.copy(), iterations, water_amount, evaporation_rate, sediment_capacity)

water_threshold = 0.6
color_map = create_color_map(eroded_map, water_threshold)
img = color_map_to_image(color_map)
img.save("fantasy_map.png")

