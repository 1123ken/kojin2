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
    def __init__(self, x, y, tile_size, speed, animation_images, field):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size  # キャラクターの幅を1倍に変更
        self.height = tile_size  # キャラクターの高さを1倍に変更
        self.speed = speed
        self.animation_images = animation_images
        self.directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
        self.current_frame = 0
        self.animation_speed = 60  # 60フレームごとに1回画像を更新
        self.current_direction = 'down'
        self.last_animation_time = pygame.time.get_ticks()
        self.field = field  # キャラクターが属するフィールドを保持

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > 1000:
            self.last_animation_time = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.animation_images[self.current_direction]):
                self.current_frame = 0

    def draw(self, screen):
        character_image = pygame.transform.scale(
            self.animation_images[self.current_direction][self.current_frame],
            (self.width, self.height)
        )
        screen.blit(character_image, (self.x - self.field.camera_x * self.field.tile_size,
                                      self.y - self.field.camera_y * self.field.tile_size))


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
            pygame.image.load("charaIMG\ggi.gif"),
            pygame.image.load("charaIMG/arakure.gif"),
            pygame.image.load("charaIMG/nouhu.gif")
        ]
        self.npc_positions = npc_positions

    def draw(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.map_data[y][x]
                tile_image = self.ground_tile if tile_type == 0 else self.wall_tile
                screen.blit(tile_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

    def draw_npcs(self, screen):
        for i, npc_pos in enumerate(self.npc_positions):
            x, y = npc_pos
            npc_image = pygame.transform.scale(self.npc_images[i], (self.tile_size, self.tile_size))
            screen.blit(npc_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

class Main:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.TILE_SIZE = 32

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Town Exploration Example")

        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],

        ]

        self.npc_positions = [(2, 2), (2, 4), (2, 6)]  # 仮のNPC位置

        self.character_images = {
            'up': [pygame.image.load("charaIMG/83_back.gif"), pygame.image.load("charaIMG/83_back2.gif")],
            'down': [pygame.image.load("charaIMG/83_front.gif"), pygame.image.load("charaIMG/83_front2.gif")],
            'left': [pygame.image.load("charaIMG/83_left.gif"), pygame.image.load("charaIMG/83_left2.gif")],
            'right': [pygame.image.load("charaIMG/83_right.gif"), pygame.image.load("charaIMG/83_right2.gif")],
        }

        self.music = Music("bgm/DQ6 木漏れ日の中で.mp3")
        self.field = Field(self.map_data, self.TILE_SIZE, "field/sand.gif", "field/tile.gif", self.npc_positions)
        self.character = Character(5, 5, self.TILE_SIZE, 4, self.character_images, self.field)

        self.running = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for key, direction in self.character.directions.items():
            if keys[key]:
                self.character.current_direction = direction

    def update_character_position(self):
        max_x = self.field.map_width * self.TILE_SIZE - self.SCREEN_WIDTH
        max_y = self.field.map_height * self.TILE_SIZE - self.SCREEN_HEIGHT
    
        keys = pygame.key.get_pressed()
        new_x, new_y = self.character.x, self.character.y
    
        if keys[pygame.K_LEFT] and self.character.x > 0:
            new_x -= self.character.speed
        if keys[pygame.K_RIGHT] and self.character.x < self.SCREEN_WIDTH - self.character.width:
            new_x += self.character.speed
        if keys[pygame.K_UP] and self.character.y > 0:
            new_y -= self.character.speed
        if keys[pygame.K_DOWN] and self.character.y < self.SCREEN_HEIGHT - self.character.height:
            new_y += self.character.speed
    
        # 移動先が壁やNPCとの衝突しないか確認
        new_rect = pygame.Rect(new_x, new_y, self.character.width, self.character.height)
    
        # 壁との衝突判定
        wall_collision_rects = [
            pygame.Rect((x - self.field.camera_x) * self.TILE_SIZE, (y - self.field.camera_y) * self.TILE_SIZE,
                        self.TILE_SIZE, self.TILE_SIZE) for y in range(self.field.map_height) for x in range(self.field.map_width)
            if self.field.map_data[y][x] == 1
        ]
        if not any(new_rect.colliderect(wall_rect) for wall_rect in wall_collision_rects):
            # NPCとの衝突判定
            npc_collision_rects = [
                pygame.Rect((npc_x - self.field.camera_x) * self.TILE_SIZE, (npc_y - self.field.camera_y) * self.TILE_SIZE,
                            self.TILE_SIZE * 2, self.TILE_SIZE * 2) for npc_x, npc_y in self.field.npc_positions
            ]
            if not any(new_rect.colliderect(npc_rect) for npc_rect in npc_collision_rects):
                self.character.x, self.character.y = new_x, new_y
    
        # カメラ位置の更新
        self.field.camera_x = max(0, min((self.character.x + self.character.width) // self.TILE_SIZE, max_x // self.TILE_SIZE))
        self.field.camera_y = max(0, min((self.character.y + self.character.height) // self.TILE_SIZE, max_y // self.TILE_SIZE))
    





    def run(self):
        self.music.play()

        while self.running:
            self.handle_events()
            self.update_character_position()

            self.screen.fill((255, 255, 255))  # 背景を白でクリア

            self.field.draw(self.screen)
            self.field.draw_npcs(self.screen)

            self.character.update_animation()
            self.character.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        self.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()
