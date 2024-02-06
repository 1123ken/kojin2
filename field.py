# field.py
import pygame

# マップ表示のクラス
class Field:
    def __init__(self, map_data, tile_size, ground_tile_path, wall_tile_path, umi_tile_path, npc_positions):
        self.map_data = map_data
        self.tile_size = tile_size
        self.ground_tile_original = pygame.image.load(ground_tile_path)
        self.wall_tile_original = pygame.image.load(wall_tile_path)
        self.umi_tile_original = pygame.image.load(umi_tile_path)
        self.ground_tile = pygame.transform.scale(self.ground_tile_original, (tile_size, tile_size))
        self.wall_tile = pygame.transform.scale(self.wall_tile_original, (tile_size, tile_size))
        self.umi_tile = pygame.transform.scale(self.umi_tile_original, (tile_size, tile_size))
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
        self.characters = []  # charactersリストを初期化

    def add_character(self, character):
        self.characters.append(character)

    def draw(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.map_data[y][x]
                if tile_type == 0:  # 0なら砂場
                    tile_image = self.ground_tile
                elif tile_type == 1:  # 1ならタイル
                    tile_image = self.wall_tile
                elif tile_type == 2:   # 2なら海
                    tile_image = self.umi_tile
                else: tile_image = self.umi_tile
                screen.blit(tile_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))
    
    def draw_npcs(self, screen):
        for i, npc_pos in enumerate(self.npc_positions):
            x, y = npc_pos
            npc_image = pygame.transform.scale(self.npc_images[i], (self.tile_size, self.tile_size))
            screen.blit(npc_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

    def is_valid_move(self, x, y):
        # 移動先が有効な場合は True を返す
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        
        if 0 <= tile_y < self.map_height and 0 <= tile_x < self.map_width:
            return self.map_data[tile_y][tile_x] != 1  # 1は壁なので壁にぶつかる場合は False を返す
        else:
            return False
