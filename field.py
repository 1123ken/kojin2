# field.py

import pygame

# マップ表示のクラス
class Field:
    def __init__(self, map_data, tile_size, ground_tile_path, wall_tile_path, npc_positions):
        self.map_data = map_data
        self.tile_size = tile_size
        self.ground_tile_original = pygame.image.load(ground_tile_path)
        self.wall_tile_original = pygame.image.load(wall_tile_path)
        self.ground_tile = pygame.transform.scale(self.ground_tile_original, (tile_size, tile_size))
        self.wall_tile = pygame.transform.scale(self.wall_tile_original, (tile_size, tile_size))
        self.map_width = len(map_data[0])
        self.map_height = len(map_data)
        self.camera_x = 0
        self.camera_y = 0
        self.npc_images = [
            pygame.image.load("charaIMG/ggi.gif"),
            pygame.image.load("charaIMG/arakure.gif"),
            pygame.image.load("charaIMG/nouhu.gif")
        ]
        self.npc_positions = npc_positions

    def draw(self, screen):  # 修正: screen引数を受け取る
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.map_data[y][x]
                tile_image = self.ground_tile if tile_type == 0 else self.wall_tile
                screen.blit(tile_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

    def draw_npcs(self, screen):  # 修正: screen引数を受け取る
        for i, npc_pos in enumerate(self.npc_positions):
            x, y = npc_pos
            npc_image = pygame.transform.scale(self.npc_images[i], (self.tile_size, self.tile_size))
            screen.blit(npc_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))
