import pygame
import sys
from character import NPC
from window import MessageWindow

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ドラクエ風会話")

tile_size = 32
speed = 5
npc_id = 1  # NPCのID（仮に1とする）
field = None  # フィールドオブジェクト

# フィールドオブジェクトを初期化
def init_field():
    global field
    field = Field(screen)

# ゲームループ
def main():
    init_field()  # フィールドを初期化

    npc = NPC(5, 5, tile_size, speed, field, npc_id)  # NPCのインスタンスを作成
    message_window = MessageWindow(SCREEN_WIDTH, SCREEN_HEIGHT // 4)  # メッセージウィンドウを作成

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # キャラクターやウィンドウの更新処理
        npc.update_animation()
        npc.draw(screen)
        message_window.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
