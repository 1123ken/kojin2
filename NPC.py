import pygame

class NPC:
    def __init__(self, x, y, tile_size, npc_image, field, npc_id):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        self.tile_size = tile_size
        self.npc_image = pygame.transform.scale(npc_image, (tile_size, tile_size))
        self.field = field
        self.npc_id = npc_id
        self.directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
        self.current_direction = 'down'
        self.current_frame = 0 
        self.npc_images = [
            pygame.image.load("charaIMG/ggi.gif"),
            pygame.image.load("charaIMG/arakure.gif"),
            pygame.image.load("charaIMG/nouhu.gif")
        ]

    def update(self, max_x, max_y):
        self.update_animation()

    def draw(self, screen, camera_x, camera_y):
        x_offset = (self.width - self.npc_image.get_width()) // 2
        y_offset = self.height - self.npc_image.get_height()
        screen.blit(self.npc_image, (self.x - camera_x * self.tile_size + x_offset, self.y - camera_y * self.tile_size + y_offset))

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
            messages = ["目の前のアラクレに話しかけた", "！？", "ただの　しかばねの　ようだ"]
        elif self.npc_id == 3:
            messages = ["ん？", "おらに話しかけても", "何もないど"]

        # メッセージをセットし、ウィンドウを表示
        self.field.message_window.set_messages(messages)
