import pygame

character_images = {
        'up': [pygame.image.load("charaIMG/83_back.gif"), pygame.image.load("charaIMG/83_back2.gif")],
        'down': [pygame.image.load("charaIMG/83_front.gif"), pygame.image.load("charaIMG/83_front2.gif")],
        'left': [pygame.image.load("charaIMG/83_left.gif"), pygame.image.load("charaIMG/83_left2.gif")],
        'right': [pygame.image.load("charaIMG/83_right.gif"), pygame.image.load("charaIMG/83_right2.gif")],
        None: []  # None キーを追加し、空の画像リストを設定
    }

class Character:
    def __init__(self, x, y, tile_size, speed, animation_images, field, npc_id=None):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.tile_size = tile_size
        self.speed = speed
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
        # Fieldに自分を追加
        self.field.add_character(self)

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

        # is_valid_move メソッドを使って移動の可否を確認
        if self.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            target_npc_position = (self.x // self.tile_size, self.y // self.tile_size)

        if keys[pygame.K_z] and self.is_near_npc():
            self.talk()

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

    def is_near_npc(self):
        # NPCとの距離が一定以下かどうかを判定
        for npc_pos in self.field.npc_positions:
            npc_x, npc_y = npc_pos
            distance = ((self.x - npc_x) ** 2 + (self.y - npc_y) ** 2) ** 0.5
            if distance < self.tile_size:
                return True
        return False

    def is_valid_move(self, new_x, new_y):
        # 移動先が有効な場合は True を返す
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # 壁との当たり判定
        umi_collision_rects = [
            pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
            #2のumi.gifは接触すると壁判定になる
            for y in range(self.field.map_height)
            for x in range(self.field.map_width)
            if self.field.map_data[y][x] == 2
        ]
        if any(new_rect.colliderect(umi_rect) for umi_rect in umi_collision_rects):
            return False  # 壁に当たる場合は移動不可

        # NPCとの接触判定
        for npc_pos in self.field.npc_positions:
            npc_x, npc_y = npc_pos
            npc_rect = pygame.Rect(npc_x * self.tile_size, npc_y * self.tile_size, self.tile_size, self.tile_size)
            if new_rect.colliderect(npc_rect):
                return False  # NPCに当たる場合は移動不可

        # 他のキャラクターとの当たり判定
        for other_character in self.field.characters:
            if other_character != self:  # 自分以外のキャラクターとの衝突判定
                other_rect = pygame.Rect(other_character.x, other_character.y, other_character.width, other_character.height)
                if new_rect.colliderect(other_rect):
                    return False  # 他のキャラクターに当たる場合は移動不可

        return True  # 移動可能な場合は True を返す