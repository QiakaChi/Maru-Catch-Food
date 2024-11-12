import pygame
import random
import os
import time

# 初始化Pygame
pygame.init()


# 设置游戏窗口
WIDTH, HEIGHT = 1200, 675
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("接食物游戏")

# 加载背景图片
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 加载字体（确保字体文件“msyh.ttf”在当前目录中）
font = pygame.font.Font("fonts/msyh.ttf", 24)
large_font = pygame.font.Font("fonts/msyh.ttf", 36)

# 设置角色图片的宽度
character_width = 300

# 加载角色图片
left_image = pygame.image.load("left.png")
right_image = pygame.image.load("right.png")

# 计算缩放后的高度，保持长宽比例不变
original_width, original_height = left_image.get_size()
character_height = int(original_height * (character_width / original_width))
left_image = pygame.transform.scale(left_image, (character_width, character_height))

original_width, original_height = right_image.get_size()
character_height = int(original_height * (character_width / original_width))
right_image = pygame.transform.scale(right_image, (character_width, character_height))


character_image = right_image  # 初始方向为右

# 定义食物和角色的参数
food_width, food_height = 40, 40
character_width, character_height = character_image.get_width(), character_image.get_height()
character_speed = 10


# 游戏状态和得分
score = 0
high_score = 0
time_limit = 30
is_paused = False
game_over = False

# 设置食物图片的宽度
food_width = 100
# 获取食物图片并生成分数规则
food_images = {}
for file in os.listdir("pics"):
    if file.endswith(".png"):
        image = pygame.image.load(os.path.join("pics", file))
        # 计算缩放后的高度，保持长宽比例不变
        original_width, original_height = image.get_size()
        food_height = int(original_height * (food_width / original_width))
        image = pygame.transform.scale(image, (food_width, food_height))
        food_images[file] = image

# 创建角色
character = pygame.Rect(WIDTH // 2 - character_width // 2, HEIGHT - character_height - 10, character_width, character_height)

# 创建食物
def create_food():
    x = random.randint(0, WIDTH - food_width)
    y = 0 - food_height
    speed = random.randint(10, 20)  
    image_name = random.choices(list(food_images.keys()), weights=[60, 30, 10], k=1)[0]
    return pygame.Rect(x, y, food_width, food_height), food_images[image_name], speed, int(image_name.split(".")[0])

foods = [create_food() for _ in range(10)]  # 同时生成10个食物

# 创建按钮
class Button:
    def __init__(self, text, pos, size, color=BLACK, bgcolor=(255, 255, 0)):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.bgcolor = bgcolor
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgcolor, self.rect)
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# 定义按钮
start_button = Button("开始游戏", (WIDTH // 2 - 50, HEIGHT // 2 - 80), (100, 40))
rules_button = Button("规则说明", (WIDTH // 2 - 50, HEIGHT // 2), (100, 40))
quit_button = Button("退出", (WIDTH // 2 - 50, HEIGHT // 2 + 80), (100, 40))

# 游戏首页
def game_home():
    screen.blit(background, (0, 0))
    title_text = large_font.render("接食物游戏", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    start_button.draw(screen)
    rules_button.draw(screen)
    quit_button.draw(screen)
    pygame.display.flip()

# 在规则说明界面中添加返回按钮
back_button = Button("返回", (WIDTH // 2 - 50, HEIGHT // 2 + 80), (100, 40))

# 修改规则说明函数 show_rules()
def show_rules():
    rule_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    rule_screen.blit(background, (0, 0))
    rules_text = font.render("规则说明：接住掉下的食物获得分数。10分食物最常见。", True, BLACK)
    rule_screen.blit(rules_text, (WIDTH // 2 - rules_text.get_width() // 2, HEIGHT // 2))
    
    # 显示返回按钮
    back_button.draw(rule_screen)
    pygame.display.flip()

    # 等待用户返回
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    waiting = False

    pygame.display.flip()


# 创建重新游戏按钮
restart_button = Button("重新游戏", (WIDTH // 2 - 50, HEIGHT // 2 + 120), (100, 40))

# 修改游戏结束界面
def game_over_screen():
    screen.fill(WHITE)
    over_text = large_font.render("游戏结束", True, BLACK)
    score_text = font.render(f"本局得分: {score}", True, BLACK)
    high_score_text = font.render(f"最高得分: {high_score}", True, BLACK)

    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 40))
    
    # 绘制重新游戏按钮
    restart_button.draw(screen)
    pygame.display.flip()

    # 等待用户重新游戏
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.is_clicked(mouse_pos):
                    waiting = False  # 点击重新游戏按钮，退出等待状态
                    game_loop()  # 重新开始游戏

# 加载音乐
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # 循环播放音乐

# 右上角的按钮
music_button = Button("音乐开关", (WIDTH - 220, 10), (100, 40))
pause_button = Button("暂停", (WIDTH - 110, 10), (100, 40))

# 在主循环中检测点击事件
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if music_button.is_clicked(mouse_pos):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()  # 暂停音乐
            else:
                pygame.mixer.music.unpause()  # 恢复音乐
        elif pause_button.is_clicked(mouse_pos):
            is_paused = not is_paused  # 切换暂停状态


# 初始化方向改变计数器和加载音频文件
direction_change_count = 0  # 记录方向改变次数
direction_sounds = [
    pygame.mixer.Sound("direction_change-1.mp3"),
    pygame.mixer.Sound("direction_change-2.mp3"),
    pygame.mixer.Sound("direction_change-3.mp3")
]

# 主游戏循环
def game_loop():
    music_button.draw(screen)
    pause_button.draw(screen)

    global score, high_score, game_over, is_paused, foods, character_image, direction_change_count

    score = 0
    start_time = time.time()
    game_over = False

    # 初始化当前方向为右
    current_direction = 'right'
    

    while not game_over:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                elif event.key == pygame.K_ESCAPE:
                    return  # 返回首页

        if not is_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and character.left > 0:
                # 角色向左移动
                if current_direction != 'left':  # 检查方向是否变化
                    current_direction = 'left'
                    # 播放音频并更新计数器
                    direction_sounds[direction_change_count % 3].play()
                    direction_change_count += 1
                character.x -= character_speed
                character_image = left_image
            elif keys[pygame.K_RIGHT] and character.right < WIDTH:
                # 角色向右移动
                if current_direction != 'right':  # 检查方向是否变化
                    current_direction = 'right'
                    # 播放音频并更新计数器
                    direction_sounds[direction_change_count % 3].play()
                    direction_change_count += 1
                character.x += character_speed
                character_image = right_image

            for i in range(len(foods)):
                food, food_image, food_speed, food_score = foods[i]
                food.y += food_speed

                if food.colliderect(character):
                    score += food_score
                    foods[i] = create_food()

                elif food.y > HEIGHT:
                    foods[i] = create_food()

                screen.blit(food_image, (food.x, food.y))

            screen.blit(character_image, (character.x, character.y))

            elapsed_time = int(time.time() - start_time)
            remaining_time = max(time_limit - elapsed_time, 0)
            score_text = font.render(f"Score: {score}", True, BLACK)
            time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(time_text, (10, 50))

            if remaining_time <= 0:
                game_over = True
                high_score = max(high_score, score)

        pygame.display.flip()
        pygame.time.delay(30)

    game_over_screen()

# 主程序
while True:
    game_home()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    game_loop()
                elif rules_button.is_clicked(mouse_pos):
                    show_rules()
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
