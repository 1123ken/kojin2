# message_window.py

import pygame

class MessageWindow:
    def __init__(self, screen, font=None):
        self.font = font
        self.messages = []
        self.current_page = 0
        self.screen = screen  # スクリーンへの参照を保存

    def set_messages(self, messages):
        self.messages = messages
        self.current_page = 0

    def draw(self):
        if 0 <= self.current_page < len(self.messages) and self.font:
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 400, 800, 200), 0)
            message = self.messages[self.current_page]
            text_surface = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(text_surface, (10, 420))
            page_text = f"Page: {self.current_page + 1}/{len(self.messages)}"
            page_surface = self.font.render(page_text, True, (0, 0, 0))
            self.screen.blit(page_surface, (600, 580))

    def next_page(self):
        if self.current_page < len(self.messages) - 1:
            self.current_page += 1

    # 追加: メッセージウィンドウをクリアするメソッド
    def clear(self):
        self.messages = []
        self.current_page = 0
