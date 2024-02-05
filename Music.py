# Music.py

import pygame

class MusicPlayer:
    def __init__(self, music_path):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
