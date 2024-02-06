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

    # スペースキーが押されたら話しかけるアクションを実行
    if keys[pygame.K_SPACE] and character.is_near_npc():
        character.talk()
        # メッセージウィンドウにメッセージをセット
        message_window.set_message("テストメッセージ２")

def main():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # 画面のサイズを設定
    TILE_SIZE = 32

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ハッサンを操作するゲームみたいなの")

    # マップの表示イメージ　0が砂場 1がタイル 2が海（侵入不可）
    map_data = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,1,1,1,2,2,2,2,2,1,1,1,2,2,2,2,2,1,1,1,2,2,2],
        [2,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,2],
        [2,1,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ]

    npc_positions = [(4, 10), (12, 10), (20, 10)]

    # MusicPlayer クラスのインスタンスを作成
    music_player = MusicPlayer("bgm/DQ6 木漏れ日の中で.mp3")
    music_player.play()

    # フィールドに使用する画像データの設定
    field = Field(map_data, TILE_SIZE, "field/sand.gif", "field/tile.gif", "field\\umi.gif", npc_positions)

    # 操作キャラクターの初期位置 サイズの設定
    character = Character(12, 12, TILE_SIZE, 4, character_images, field)
    font = pygame.font.Font(None, 36)
    message_window = MessageWindow(screen, font)

    running = True
    clock = pygame.time.Clock()

    while running:
        handle_events(character, message_window)
        character.update(SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.fill((255, 255, 255))  # 背景を白でクリア

        field.draw(screen)
        field.draw_npcs(screen)
        character.update_animation()
        character.draw(screen, field.camera_x, field.camera_y)
        pygame.display.flip()
        clock.tick(60)

    music_player.stop()
    pygame.quit()

if __name__ == "__main__":
    main()