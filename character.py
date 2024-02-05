import pygame

# キャラクター管理のクラス
class Character:
    # キャラクターの初期化
    def __init__(self, x, y, tile_size, speed, animation_images, field, npc_id=None):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.tile_size = tile_size
        self.speed = speed
        self.animation_images = animation_images
        self.directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
        self.current_frame = 0
        self.animation_speed = 60
        self.current_direction = 'down'
        self.last_animation_time = pygame.time.get_ticks()
        self.field = field
        self.npc_id = npc_id

    # キャラクターの更新
    def update(self, max_x, max_y):
        self.update_animation()

        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y

        if keys[pygame.K_LEFT] and self.x > 0:
            new_x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < max_x - self.width:
            new_x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            new_y -= self.speed
            if self.current_direction == 'up' and new_y % self.tile_size == 0:
                self.talk()
        if keys[pygame.K_DOWN] and self.y < max_y - self.height:
            new_y += self.speed

        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        wall_collision_rects = [
            pygame.Rect((x - self.field.camera_x) * self.tile_size, (y - self.field.camera_y) * self.tile_size,
                        self.tile_size, self.tile_size) for y in range(self.field.map_height) for x in range(self.field.map_width)
            if self.field.map_data[y][x] == 1
        ]

        if not any(new_rect.colliderect(wall_rect) for wall_rect in wall_collision_rects):
            npc_collision_rects = [
                pygame.Rect((npc_x - self.field.camera_x) * self.tile_size, (npc_y - self.field.camera_y) * self.tile_size,
                            self.tile_size, self.tile_size) for npc_x, npc_y in self.field.npc_positions
            ]
            if not any(new_rect.colliderect(npc_rect) for npc_rect in npc_collision_rects):
                self.x, self.y = new_x, new_y

        self.field.camera_x = max(0, min((self.x + self.width) // self.tile_size, max_x // self.tile_size))
        self.field.camera_y = max(0, min((self.y + self.height) // self.tile_size, max_y // self.tile_size))

    # キャラクターのアニメーションを更新
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.animation_images[self.current_direction]):
                self.current_frame = 0

    # キャラクターの描画
    def draw(self, screen):
        character_image = pygame.transform.scale(
            self.animation_images[self.current_direction][self.current_frame],
            (self.width, self.height)
        )
        screen.blit(character_image, (self.x - self.field.camera_x * self.tile_size,
                                      self.y - self.field.camera_y * self.tile_size))

    # キャラクターが話しかける
    def talk(self):
        if self.npc_id is not None:
            print(f"Talking to NPC {self.npc_id}...")
            # NPCごとの会話処理をここに追加
            if self.npc_id == 1:
                print("This is NPC 1.")
                # NPC 1 の会話処理を追加
                # 例：self.field.npc_positions[0]にいるNPCに対する処理
            elif self.npc_id == 2:
                print("This is NPC 2.")
                # NPC 2 の会話処理を追加
                # 例：self.field.npc_positions[1]にいるNPCに対する処理
            elif self.npc_id == 3:
                print("This is NPC 3.")
                # NPC 3 の会話処理を追加
                # 例：self.field.npc_positions[2]にいるNPCに対する処理
            else:
                print("Unknown NPC.")
        else:
            print("This character is not an NPC.")
