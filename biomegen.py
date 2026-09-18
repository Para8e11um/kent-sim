from perlin_noise import PerlinNoise
import math

BIOMES_ARRAY = [
    {"name": "Поле", "color": "#7CB342"},
    {"name": "Лес", "color": "#2E7D32"},
    {"name": "Город", "color": "#8e9675"}
]

class BiomeMap:
    def __init__(self,size: int, biomes: list, seed: int):
        self.size = size
        self.biomes = biomes

        self.noise = PerlinNoise(octaves=3,seed=seed)
        self.grid = []

        self.noise_scale = 0.05

        self.generate_map()

    def generate_map(self):
        number_of_biomes = len(self.biomes)

        for x in range(self.size):
            row = []
            for y in range(self.size):
                noise_value = self.noise([x*self.noise_scale,y*self.noise_scale]) + 0.5
                noise_value = max(0.0,min(0.999,noise_value))
                biome_index = math.floor(noise_value*number_of_biomes)
                row.append(self.biomes[biome_index])
            self.grid.append(row)

    def get_biome(self, x: int, y: int):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y]
        return {"name": "None", "color": "#000000"}
