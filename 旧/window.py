# window.py
import pygame

class MessageWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)  # フォントの設定
        self.text_color = (255, 255, 255)  # テキストの色
        self.background_color = (0, 0, 0)  # 背景色
        self.messages = []

    def set_messages(self, messages):
        self.messages = messages

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, (0, 0, self.width, self.height))  # 背景を描画
        y_offset = 10
        for message in self.messages:
            text_surface = self.font.render(message, True, self.text_color)  # テキストをレンダリング
            screen.blit(text_surface, (10, y_offset))  # テキストを画面に描画
            y_offset += 40  # メッセージ間の間隔を調整
