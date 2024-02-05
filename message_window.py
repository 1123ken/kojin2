import pygame

#メッセージウィンドウの管理のクラス
class MessageWindow:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.message = ""

    def set_message(self, message):
        self.message = message

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 500, 800, 100))  # メッセージウィンドウの描画領域
        text = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(text, (10, 510))  # メッセージの描画位置