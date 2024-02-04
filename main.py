import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 32
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Character Animation")

character_width, character_height = 128, 128  # 64 * 2
character_x, character_y = 100, 100
character_speed = 4

# 4方向のアニメーションGIFの読み込みとサイズ変更
character_images = {
    'up': [
        pygame.transform.scale(pygame.image.load("charaImg/83_back.gif").convert(), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("charaImg/83_back2.gif").convert(), (character_width, character_height))
    ],
    'down': [
        pygame.transform.scale(pygame.image.load("charaImg/83_front.gif").convert(), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("charaImg/83_front2.gif").convert(), (character_width, character_height))
    ],
    'left': [
        pygame.transform.scale(pygame.image.load("charaImg/83_left.gif").convert(), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("charaImg/83_left2.gif").convert(), (character_width, character_height))
    ],
    'right': [
        pygame.transform.scale(pygame.image.load("charaImg/83_right.gif").convert(), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("charaImg/83_right2.gif").convert(), (character_width, character_height))
    ]
}
direction = 'down'

# 音楽の読み込みと再生
pygame.mixer.music.load("bgm/DQ6 木漏れ日の中で.mp3")
pygame.mixer.music.play(-1)

# 背景画像の読み込みとサイズ変更
background_image = pygame.transform.scale(pygame.image.load("back_img/map.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# キャラクターのアニメーション設定
animation_speed = 750
frame_count = 2
current_frame = 0
last_frame_time = pygame.time.get_ticks()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    max_x = SCREEN_WIDTH - character_width
    max_y = SCREEN_HEIGHT - character_height

    if keys[pygame.K_LEFT] and character_x > 0:
        character_x -= character_speed
        direction = 'left'
    if keys[pygame.K_RIGHT] and character_x < max_x:
        character_x += character_speed
        direction = 'right'
    if keys[pygame.K_UP] and character_y > 0:
        character_y -= character_speed
        direction = 'up'
    if keys[pygame.K_DOWN] and character_y < max_y:
        character_y += character_speed
        direction = 'down'

    # 背景画像の表示
    screen.blit(background_image, (0, 0))

    # アニメーションの速度に合わせてフレームを変更
    current_time = pygame.time.get_ticks()
    if current_time - last_frame_time > animation_speed:
        last_frame_time = current_time
        current_frame = (current_frame + 1) % frame_count

    # キャラクターのアニメーション表示
    screen.blit(character_images[direction][current_frame], (character_x, character_y))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
