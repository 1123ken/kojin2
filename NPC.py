import pygame

# character.py

class NPC:
    def __init__(self, x, y, tile_size, speed, field, npc_id):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.tile_size = tile_size
        self.speed = speed
        self.animation_images = {
            'ggi': [pygame.image.load("charaIMG/ggi.gif"), pygame.image.load("charaIMG/ggi2.gif")],
            'arakure': [pygame.image.load("charaIMG/arakure.gif"), pygame.image.load("charaIMG/arakure2.gif")],
            'nouhu': [pygame.image.load("charaIMG/nouhu.gif"), pygame.image.load("charaIMG/nouhu2.gif")]
        }
        self.current_frame = 0
        self.animation_speed = 450
        self.current_direction = 'down'
        self.last_animation_time = pygame.time.get_ticks()
        self.field = field
        self.npc_id = npc_id

    def update_animation(self):
        # アニメーションの更新
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.animation_images[self.npc_id]):
                self.current_frame = 0

    def draw(self, screen, camera_x, camera_y):
        # NPCの描画
        if self.current_direction in self.animation_images and self.animation_images[self.current_direction]:
            animation_list = self.animation_images[self.npc_id]
            if 0 <= self.current_frame < len(animation_list):
                frame = self.current_frame % len(animation_list)
                npc_image = animation_list[frame]
                x_offset = (self.width - npc_image.get_width()) // 2
                y_offset = self.height - npc_image.get_height()
                screen.blit(npc_image, (self.x - camera_x * self.tile_size + x_offset, self.y - camera_y * self.tile_size + y_offset))

    def handle_key_release(self, key):
        if key in self.directions:
            self.current_direction = self.directions[key]
            self.current_frame = 0

    def talk(self):
        messages = []

        # NPCごとの会話処理
        if self.npc_id == 1:
            messages = ["ふがふが", "私は戦うことはできませんが。", "治療の杖を使うことが出来ます。"]
        elif self.npc_id == 2:
            messages = ["目の前のアラクレに話しかけた", "！？", "ただの しかばねの ようだ"]
        elif self.npc_id == 3:
            messages = ["ん？", "おらに話しかけても", "何もないど"]

        # メッセージをセットし、ウィンドウを表示
        self.field.message_window.set_messages(messages)
