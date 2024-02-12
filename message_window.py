# message_window.py

import pygame
from pygame.locals import *
import os
import codecs

class MessageWindow:
    EDGE_WIDTH = 4  # 白枠の幅
    def __init__(self, screen, font=None):
        self.font = font
        self.messages = []
        self.current_page = 0
        self.screen = screen  # スクリーンへの参照を保存

        # 外側の白い矩形
        self.rect = screen.get_rect()
        
        # 内側の黒い矩形
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH*2, -self.EDGE_WIDTH*2)

        self.is_visible = False  # ウィンドウを表示中か？

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

    def show(self):
        """ウィンドウを表示"""
        self.is_visible = True

    def hide(self):
        """ウィンドウを隠す"""
        self.is_visible = False

    def set_messages(self, messages):
        self.messages = messages
        self.current_page = 0

