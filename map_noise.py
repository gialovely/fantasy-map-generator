import numpy as np
from noise import pnoise2


def generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed):
    noise_map = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            nx = x / width * scale + seed
            ny = y / height * scale + seed
            noise_map[y][x] = pnoise2(nx, ny, octaves, persistence, lacunarity, repeatx=1024, repeaty=1024, base=seed)

    return noise_map

def normalize_noise_map(noise_map):
    min_val = np.min(noise_map)
    max_val = np.max(noise_map)
    return (noise_map - min_val) / (max_val - min_val)

