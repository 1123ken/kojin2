import pygame

class Character:
    def __init__(self, x, y, tile_size, speed, animation_images, field, npc_id=None):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.tile_size = tile_size
        self.speed = speed / 2
        self.animation_images = {
            direction: [pygame.transform.scale(image, (self.tile_size, self.tile_size)) for image in images]
            for direction, images in animation_images.items()}
        self.directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
        self.current_frame = 0
        self.animation_speed = 450
        self.current_direction = 'down'
        self.last_animation_time = pygame.time.get_ticks()
        self.field = field
        self.npc_id = npc_id

    def update(self, max_x, max_y):
        # キー入力の処理
        self.update_animation()
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y
        current_direction = None

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            new_x -= self.speed
            current_direction = self.directions[pygame.K_LEFT]

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            new_x += self.speed
            current_direction = self.directions[pygame.K_RIGHT]

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            new_y -= self.speed
            current_direction = self.directions[pygame.K_UP]

        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            new_y += self.speed
            current_direction = self.directions[pygame.K_DOWN]

        target_npc_position = (new_x // self.tile_size, new_y // self.tile_size)

        if current_direction == 'up' and keys[pygame.K_z] and self.y > 0:
            if target_npc_position in self.field.npc_positions:
                self.talk()

        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        wall_collision_rects = [
            pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
            for y in range(self.field.map_height) for x in range(self.field.map_width) if self.field.map_data[y][x] == 1
        ]

        # 壁との当たり判定
        if not any(new_rect.colliderect(wall_rect) for wall_rect in wall_collision_rects):
            npc_collision_rects = [
                pygame.Rect(npc_x * self.tile_size, npc_y * self.tile_size, self.tile_size, self.tile_size)
                for npc_x, npc_y in self.field.npc_positions
            ]

            # NPCとの当たり判定
            if not any(new_rect.colliderect(npc_rect) for npc_rect in npc_collision_rects):
                self.x, self.y = new_x, new_y

            # 移動方向があれば、それを設定
            if current_direction:
                self.current_direction = current_direction

            # カメラの位置更新
            self.field.camera_x = max(0, min((self.x + self.width) // self.tile_size, max_x // self.tile_size))
            self.field.camera_y = max(0, min((self.y + self.height) // self.tile_size, max_y // self.tile_size))
        else:
            # 壁に当たった場合もカメラの位置を更新
            self.field.camera_x = max(0, min((self.x + self.width) // self.tile_size, max_x // self.tile_size))
            self.field.camera_y = max(0, min((self.y + self.height) // self.tile_size, max_y // self.tile_size))

    def update_animation(self):
        # アニメーションの更新
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.animation_images[self.current_direction]):
                self.current_frame = 0

    def handle_key_release(self, key):
        # キーを離した際の処理
        if key in self.directions:
            self.current_direction = self.directions[key]
            self.current_frame = 0

    def draw(self, screen, camera_x, camera_y):
        # キャラクターの描画
        if self.current_direction in self.animation_images and self.animation_images[self.current_direction]:
            animation_list = self.animation_images[self.current_direction]
            if 0 <= self.current_frame < len(animation_list):
                frame = self.current_frame % len(animation_list)
                character_image = animation_list[frame]
                x_offset = (self.width - character_image.get_width()) // 2
                y_offset = self.height - character_image.get_height()
                screen.blit(character_image, (self.x - camera_x * self.tile_size + x_offset, self.y - camera_y * self.tile_size + y_offset))
        else:
            # 方向入力がない場合、デフォルトの方向を描画
            default_direction = 'down'
            default_animation_list = self.animation_images[default_direction]
            default_frame = self.current_frame % len(default_animation_list)
            default_character_image = default_animation_list[default_frame]
            x_offset = (self.width - default_character_image.get_width()) // 2
            y_offset = self.height - default_character_image.get_height()
            screen.blit(default_character_image, (self.x - camera_x * self.tile_size + x_offset, self.y - camera_y * self.tile_size + y_offset))

    def talk(self):
        # キャラクターとNPCとの対話
        if self.npc_id is not None:
            npc_id = self.npc_id
            messages = []
            
            # NPCごとの会話処理
            if npc_id == 1:
                messages = ["こんにちは！", "私はNPC1です。", "よろしくお願いします。"]
            elif npc_id == 2:
                messages = ["おい！", "NPC2だ！", "何か用か？"]
            elif npc_id == 3:
                messages = ["やあ！", "NPC3です。", "楽しい冒険を！"]

            # メッセージをセットし、ウィンドウを表示
            self.field.message_window.set_messages(messages)

    def is_near_npc(self):
        # NPCとの距離が一定以下かどうかを判定
        for npc_pos in self.field.npc_positions:
            npc_x, npc_y = npc_pos
            distance = ((self.x - npc_x) ** 2 + (self.y - npc_y) ** 2) ** 0.5
            if distance < self.tile_size:
                return True
        return False