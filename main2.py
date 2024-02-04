
import pygame
import sys

class Music:
    def __init__(self, music_path):
        pygame.mixer.music.load(music_path)

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

class Character:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

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
        self.npc_positions = npc_positions

    # 以下略


    def draw(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.map_data[y][x]
                tile_image = self.ground_tile if tile_type == 0 else self.wall_tile
                screen.blit(tile_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

    def draw_npcs(self, screen):
        for npc_pos in self.npc_positions:
            x, y = npc_pos
            pygame.draw.rect(screen, (0, 0, 255), ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size, self.tile_size, self.tile_size))

class Main:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.TILE_SIZE = 32

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Town Exploration Example")

        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.npc_positions = [(2, 2), (5, 5), (8, 8)]  # 仮のNPC位置

        self.music = Music("bgm/DQ6 木漏れ日の中で.mp3")
        self.character = Character(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, 32, 32, 4)
        self.field = Field(self.map_data, self.TILE_SIZE, "field/sand.gif", "field/tile.gif", self.npc_positions)


        self.running = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_character_position(self):
        keys = pygame.key.get_pressed()

        max_x = self.field.map_width * self.TILE_SIZE - self.SCREEN_WIDTH
        max_y = self.field.map_height * self.TILE_SIZE - self.SCREEN_HEIGHT

        if keys[pygame.K_LEFT] and self.character.x > 0:
            self.character.x -= self.character.speed
            self.field.camera_x = max(0, min(self.field.camera_x - self.character.speed, max_x // self.TILE_SIZE))
        if keys[pygame.K_RIGHT] and self.character.x < self.SCREEN_WIDTH - self.character.width:
            self.character.x += self.character.speed
            self.field.camera_x = max(0, min(self.field.camera_x + self.character.speed, max_x // self.TILE_SIZE))
        if keys[pygame.K_UP] and self.character.y > 0:
            self.character.y -= self.character.speed
            self.field.camera_y = max(0, min(self.field.camera_y - self.character.speed, max_y // self.TILE_SIZE))
        if keys[pygame.K_DOWN] and self.character.y < self.SCREEN_HEIGHT - self.character.height:
            self.character.y += self.character.speed
            self.field.camera_y = max(0, min(self.field.camera_y + self.character.speed, max_y // self.TILE_SIZE))

    def run(self):
        self.music.play()

        while self.running:
            self.handle_events()
            self.update_character_position()

            self.screen.fill((255, 255, 255))  # 背景を白でクリア

            self.field.draw(self.screen)
            self.field.draw_npcs(self.screen)

            pygame.draw.rect(self.screen, (255, 0, 0), (self.character.x, self.character.y, self.character.width, self.character.height))

            pygame.display.flip()
            self.clock.tick(60)

        self.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()
