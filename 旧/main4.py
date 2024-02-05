import pygame
import sys

#音楽再生のクラス（ループ再生）
class Music:
    def __init__(self, music_path):
        pygame.mixer.music.load(music_path)

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

#キャラクター管理のクラス
class Character:
    def __init__(self, x, y, tile_size, speed, animation_images, field, npc_id=None):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size  # キャラクターの幅を1倍に変更
        self.height = tile_size  # キャラクターの高さを1倍に変更
        self.speed = speed
        self.animation_images = animation_images
        self.directions = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}
        self.current_frame = 0
        self.animation_speed = 60  # 60フレームごとに1回画像を更新
        self.current_direction = 'down'
        self.last_animation_time = pygame.time.get_ticks()
        self.field = field  # キャラクターが属するフィールドを保持
        self.npc_id = npc_id
    #ドット絵のアニメーションの設定
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > 1000:
            self.last_animation_time = current_time
            self.current_frame += 1
            if self.current_frame >= len(self.animation_images[self.current_direction]):
                self.current_frame = 0

    def draw(self, screen):
        character_image = pygame.transform.scale(
            self.animation_images[self.current_direction][self.current_frame],
            (self.width, self.height)
        )
        screen.blit(character_image, (self.x - self.field.camera_x * self.field.tile_size,
                                      self.y - self.field.camera_y * self.field.tile_size))
    def talk(self):
        if self.npc_id is not None:
            print(f"Talking to NPC {self.npc_id}...")
            # NPCごとの会話処理をここに追加
            if self.npc_id == 1:
                print("This is NPC 1.")
                # NPC 1 の会話処理を追加
                # 例：self.field.npc_positions[0]にいるNPCに対する処理
            elif self.npc_id == 2:
                print("This is NPC 2.")
                # NPC 2 の会話処理を追加
                # 例：self.field.npc_positions[1]にいるNPCに対する処理
            elif self.npc_id == 3:
                print("This is NPC 3.")
                # NPC 3 の会話処理を追加
                # 例：self.field.npc_positions[2]にいるNPCに対する処理
            else:
                print("Unknown NPC.")
        else:
            print("This character is not an NPC.")

# NPCの初期位置(Y軸、X軸)とID
npc_positions = [(4, 2, 1), (12, 2, 2), (20, 2, 3)]


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

#マップ表示のクラス
class Field:
    def __init__(self, map_data, tile_size, ground_tile_path, wall_tile_path, npc_positions):
        self.map_data = map_data
        self.tile_size = tile_size
        self.ground_tile_original = pygame.image.load(ground_tile_path)     #地面の画像の読み込み(sand.gif)
        self.wall_tile_original = pygame.image.load(wall_tile_path)         #接触判定ありの壁画像(tile)
        self.ground_tile = pygame.transform.scale(self.ground_tile_original, (tile_size, tile_size))    #地面画像のサイズの設定
        self.wall_tile = pygame.transform.scale(self.wall_tile_original, (tile_size, tile_size))        #壁画像のサイズ設定
        self.map_width = len(map_data[0]) 
        self.map_height = len(map_data)
        self.camera_x = 0
        self.camera_y = 0
        #NPCの画像
        self.npc_images = [
            pygame.image.load("charaIMG\ggi.gif"),          #じいさんのNPC
            pygame.image.load("charaIMG/arakure.gif"),      #アラクレのNPC
            pygame.image.load("charaIMG/nouhu.gif")         #農夫のNPC
        ]
        self.npc_positions = npc_positions

    def draw(self, screen):
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile_type = self.map_data[y][x]
                tile_image = self.ground_tile if tile_type == 0 else self.wall_tile
                screen.blit(tile_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

    def draw_npcs(self, screen):
        for i, npc_pos in enumerate(self.npc_positions):
            x, y = npc_pos
            npc_image = pygame.transform.scale(self.npc_images[i], (self.tile_size, self.tile_size))
            screen.blit(npc_image, ((x - self.camera_x) * self.tile_size, (y - self.camera_y) * self.tile_size))

#Mainクラス
class Main:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.TILE_SIZE = 32

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("ハッサンを操作するゲームみたいなの")

        #マップの表示イメージ　0なら砂　１なら壁タイル
        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0,0, 1, 1, 1, 0, 0, 0, 0, 0, 1,1,1,0,0,0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1,1, 1, 0, 1, 1, 1, 1, 1, 1, 1,0,1,1,1,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,1],
        ]
        #NPCの初期位置(Y軸、X軸)
        self.npc_positions = [(4, 2), (12, 2), (20, 2)]  # 仮のNPC位置

        #操作キャラクターの画像　各２パターンを交互に動かす
        self.character_images = {
            'up': [pygame.image.load("charaIMG/83_back.gif"), pygame.image.load("charaIMG/83_back2.gif")],
            'down': [pygame.image.load("charaIMG/83_front.gif"), pygame.image.load("charaIMG/83_front2.gif")],
            'left': [pygame.image.load("charaIMG/83_left.gif"), pygame.image.load("charaIMG/83_left2.gif")],
            'right': [pygame.image.load("charaIMG/83_right.gif"), pygame.image.load("charaIMG/83_right2.gif")],
        }

        #再生する音楽の設定
        self.music = Music("bgm/DQ6 木漏れ日の中で.mp3")
        #フィールドに使用する画像データの設定
        self.field = Field(self.map_data, self.TILE_SIZE, "field/sand.gif", "field/tile.gif", self.npc_positions)
        #操作キャラクターの初期位置　サイズの設定
        self.character = Character(5, 5, self.TILE_SIZE, 4, self.character_images, self.field)
        self.message_window = MessageWindow(self.screen, pygame.font.Font(None, 36))

        self.running = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        for key, direction in self.character.directions.items():
            if keys[key]:
                self.character.current_direction = direction

        # Zキーが押されたら話しかけるアクションを実行
        if keys[pygame.K_z]:
            self.character.talk()
            # メッセージウィンドウにメッセージをセット
            self.message_window.set_message("テストメッセージ２")

        # Xキーが押されたらメッセージウィンドウをクリア
        if keys[pygame.K_x]:
            self.message_window.set_message("またな！")

    def update_character_position(self):
        max_x = self.field.map_width * self.TILE_SIZE - self.SCREEN_WIDTH
        max_y = self.field.map_height * self.TILE_SIZE - self.SCREEN_HEIGHT

        keys = pygame.key.get_pressed()
        new_x, new_y = self.character.x, self.character.y

        if keys[pygame.K_LEFT] and self.character.x > 0:
            new_x -= self.character.speed
        if keys[pygame.K_RIGHT] and self.character.x < self.SCREEN_WIDTH - self.character.width:
            new_x += self.character.speed
        if keys[pygame.K_UP] and self.character.y > 0:
            new_y -= self.character.speed
            # 上方向を向いているかつ座標条件を満たす場合にtalkメソッドを呼び出す
            if self.character.current_direction == 'up' and new_y % self.TILE_SIZE == 0:
                self.character.talk()
        if keys[pygame.K_DOWN] and self.character.y < self.SCREEN_HEIGHT - self.character.height:
            new_y += self.character.speed
    
        # 移動先が壁やNPCとの衝突しないか確認
        new_rect = pygame.Rect(new_x, new_y, self.character.width, self.character.height)
    
        # 壁との衝突判定
        wall_collision_rects = [
            pygame.Rect((x - self.field.camera_x) * self.TILE_SIZE, (y - self.field.camera_y) * self.TILE_SIZE,
                        self.TILE_SIZE, self.TILE_SIZE) for y in range(self.field.map_height) for x in range(self.field.map_width)
            if self.field.map_data[y][x] == 1
        ]
        if not any(new_rect.colliderect(wall_rect) for wall_rect in wall_collision_rects):
            # NPCとの衝突判定 NPCの画像サイズ　＝　壁判定
            npc_collision_rects = [
                pygame.Rect((npc_x - self.field.camera_x) * self.TILE_SIZE, (npc_y - self.field.camera_y) * self.TILE_SIZE,
                            self.TILE_SIZE, self.TILE_SIZE) for npc_x, npc_y in self.field.npc_positions
            ]
            if not any(new_rect.colliderect(npc_rect) for npc_rect in npc_collision_rects):
                self.character.x, self.character.y = new_x, new_y
    
        # カメラ位置の更新
        self.field.camera_x = max(0, min((self.character.x + self.character.width) // self.TILE_SIZE, max_x // self.TILE_SIZE))
        self.field.camera_y = max(0, min((self.character.y + self.character.height) // self.TILE_SIZE, max_y // self.TILE_SIZE))
    
    def run(self):
        self.music.play()

        while self.running:
            self.handle_events()
            self.update_character_position()

            self.screen.fill((255, 255, 255))  # 背景を白でクリア

            self.field.draw(self.screen)
            self.field.draw_npcs(self.screen)

            self.character.update_animation()
            self.character.draw(self.screen)

            self.message_window.draw()  # メッセージウィンドウの描画

            pygame.display.flip()
            self.clock.tick(60)

        self.music.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()