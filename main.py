import numpy as np
from PIL import Image

from map_noise import generate_noise_map, normalize_noise_map
from erosion import erode_map
from color import create_color_map, color_map_to_image, create_difference_color_map

# Erosion parameters
water_amount = 0.01
evaporation_rate = 0.002
sediment_capacity = 0.01

if __name__ == "__main__":
    width, height = 512, 512
    scale = 6
    octaves = 6
    persistence = 0.5
    lacunarity = 2
    seed = 2

    noise_map = generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
    normalized_noise_map = normalize_noise_map(noise_map)
    
    # Save the original map
    initial_color_map = create_color_map(normalized_noise_map, 0.6)
    initial_img = color_map_to_image(initial_color_map)
    initial_img.save("original_map.png")
    
    current_map = normalized_noise_map.copy()
    for iteration in range(100):
        current_map = erode_map(current_map, 1, water_amount, evaporation_rate, sediment_capacity)
        
        # Save the map after each iteration
        color_map = create_color_map(current_map, 0.6)
        img = color_map_to_image(color_map)
        img.save(f"map_after_iteration_{iteration + 1}.png")
    
    # Calculate and save the difference image
    difference_map = current_map - normalized_noise_map
    difference_color_map = create_difference_color_map(difference_map)
    diff_img = color_map_to_image(difference_color_map)
    diff_img.save("difference_map.png")
