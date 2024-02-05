# main.py

import pygame
from character import Character
from message_window import MessageWindow
from field import Field
from Music import MusicPlayer
import sys
from character import Character, character_images

# main.py の handle_events メソッド
def handle_events(character, message_window):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    for key, direction in character.directions.items():
        if keys[key]:
            character.current_direction = direction

    # Zキーが押されたら話しかけるアクションを実行
    if keys[pygame.K_z] and character.is_near_npc():
        character.talk()
        # メッセージウィンドウにメッセージをセット
        message_window.set_message("テストメッセージ２")

    # Xキーが押されたらメッセージウィンドウをクリア
    if keys[pygame.K_x]:
        message_window.clear()

# MessageWindow クラスの draw メソッド
# MessageWindow クラスの draw メソッド
def draw(self):
    if self.messages and 0 <= self.current_page < len(self.messages) and self.font:
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 400, 800, 200), 0)
        message = self.messages[self.current_page]
        text_surface = self.font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(10, 420))
        self.screen.blit(text_surface, text_rect)

        page_text = f"Page: {self.current_page + 1}/{len(self.messages)}"
        page_surface = self.font.render(page_text, True, (0, 0, 0))
        page_rect = page_surface.get_rect(topleft=(600, 580))
        self.screen.blit(page_surface, page_rect)
    else:
        # メッセージが空の場合はウィンドウを閉じる
        self.clear()

# MessageWindow クラスに clear メソッドを追加
def clear(self):
    self.messages = []
    self.current_page = 0

def update_character_position(character, field, SCREEN_WIDTH, SCREEN_HEIGHT):
    max_x = field.map_width * field.tile_size - SCREEN_WIDTH
    max_y = field.map_height * field.tile_size - SCREEN_HEIGHT

    character.update(max_x, max_y)

    keys = pygame.key.get_pressed()
    new_x, new_y = character.x, character.y

    if keys[pygame.K_LEFT] and character.x > 0:
        new_x -= character.speed
    if keys[pygame.K_RIGHT] and character.x < SCREEN_WIDTH - character.width:
        new_x += character.speed
    if keys[pygame.K_UP] and character.y > 0:
        new_y -= character.speed
        # 上方向を向いているかつ座標条件を満たす場合にtalkメソッドを呼び出す
        if character.current_direction == 'up' and new_y % character.tile_size == 0:
            character.talk()
    if keys[pygame.K_DOWN] and character.y < SCREEN_HEIGHT - character.height:
        new_y += character.speed

    # 移動先が壁やNPCとの衝突しないか確認
    new_rect = pygame.Rect(new_x, new_y, character.width, character.height)

    # 壁との衝突判定
    wall_collision_rects = [
        pygame.Rect((x - field.camera_x) * character.tile_size, (y - field.camera_y) * character.tile_size,
                    character.tile_size, character.tile_size) for y in range(field.map_height) for x in range(field.map_width)
        if field.map_data[y][x] == 1
    ]
    if not any(new_rect.colliderect(wall_rect) for wall_rect in wall_collision_rects):
        # NPCとの衝突判定 NPCの画像サイズ ＝ 壁判定
        npc_collision_rects = [
            pygame.Rect((npc_x - field.camera_x) * character.tile_size, (npc_y - field.camera_y) * character.tile_size,
                        character.tile_size, character.tile_size) for npc_x, npc_y in field.npc_positions
        ]
        if not any(new_rect.colliderect(npc_rect) for npc_rect in npc_collision_rects):
            character.x, character.y = new_x, new_y

    # カメラ位置の更新
    field.camera_x = max(0, min((character.x + character.width) // character.tile_size, max_x // character.tile_size))
    field.camera_y = max(0, min((character.y + character.height) // character.tile_size, max_y // character.tile_size))

def main():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # 画面のサイズを設定
    TILE_SIZE = 32

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ハッサンを操作するゲームみたいなの")

    # マップの表示イメージ
    map_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0,0, 1, 1, 1, 0, 0, 0, 0, 0, 1,1,1,0,0,0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0,0, 1, 0, 1, 0, 0, 0, 0, 0, 1,0,1,0,0,0],
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

    npc_positions = [(4, 2), (12, 2), (20, 2)]

    # MusicPlayer クラスのインスタンスを作成
    music_player = MusicPlayer("bgm/DQ6 木漏れ日の中で.mp3")
    music_player.play()

    # フィールドに使用する画像データの設定
    field = Field(map_data, TILE_SIZE, "field/sand.gif", "field/tile.gif", npc_positions)

    # 操作キャラクターの初期位置 サイズの設定
    character = Character(5, 5, TILE_SIZE, 4, character_images, field)
    font = pygame.font.Font(None, 36)
    message_window = MessageWindow(screen, font)

    running = True
    clock = pygame.time.Clock()

    while running:
        handle_events(character, message_window)
        update_character_position(character, field, SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.fill((255, 255, 255))  # 背景を白でクリア

        field.draw(screen)
        field.draw_npcs(screen)  # 追加
        character.update_animation()
        character.draw(screen, field.camera_x, field.camera_y)
        pygame.display.flip()
        clock.tick(60)


    music_player.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
