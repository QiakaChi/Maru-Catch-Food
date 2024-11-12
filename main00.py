import pygame
import random
import os
import time

# 初始化Pygame
pygame.init()


# 设置游戏窗口
WIDTH, HEIGHT = 1200, 675
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Margarete Catch Food")

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
character_speed = 15


# 游戏状态和得分
score = 0
high_score = 0
time_limit = 30
is_paused = False
game_over = False

# 设置食物图片的宽度
food_width = 150
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
    image_name = random.choices(list(food_images.keys()), weights=[70, 20, 10], k=1)[0]
    
    
    
    return pygame.Rect(x, y, food_width, food_height), food_images[image_name], speed, int(image_name.split(".")[0])

foods = [create_food() for _ in range(10)]  # 同时生成10个食物

# 创建按钮
class Button:
    def __init__(self, text, pos, size, color=BLACK, bgcolor=(205, 205, 100, 200)):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.bgcolor = bgcolor
        self.font = font

    def draw(self, screen):
        button_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)  # 创建透明背景的表面
        button_surface.fill(self.bgcolor)  # 填充背景色
        screen.blit(button_surface, self.rect.topleft)  # 绘制按钮背景
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# 定义按钮
start_button = Button("Start Game", (WIDTH // 2 - 100, HEIGHT // 2 - 80), (200, 40))
rules_button = Button("Game Rules", (WIDTH // 2 - 100, HEIGHT // 2), (200, 40))
quit_button = Button("Exit", (WIDTH // 2 - 50, HEIGHT // 2 + 80), (100, 40))

# 游戏首页
def game_home():
    screen.blit(background, (0, 0))
    title_text = large_font.render("Margarete Catch Food", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    start_button.draw(screen)
    rules_button.draw(screen)
    quit_button.draw(screen)
    pygame.display.flip()

# 在规则说明界面中添加返回按钮
back_button = Button("Back", (WIDTH // 2 - 50, HEIGHT // 2 + 80), (100, 40))

# 修改规则说明函数 show_rules()
def show_rules():
    # 创建一个新的规则窗口
    rule_screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # 加载背景图片
    background_image = pygame.image.load('rules_background.png')

    # 获取背景图片的尺寸
    background_width, background_height = background_image.get_size()

    # 计算缩放后的尺寸，保持长宽比例不变
    scale_factor = min(WIDTH / background_width, HEIGHT / background_height)
    background_width = int(background_width * scale_factor)
    background_height = int(background_height * scale_factor)

    # 缩放背景图片
    background_image = pygame.transform.scale(background_image, (background_width, background_height))

    # 在屏幕上绘制背景图片
    rule_screen.blit(background_image, (0, 0))

    # 获取按钮的尺寸
    button_width, button_height = back_button.rect.size

    # 计算按钮的位置
    button_x = WIDTH - button_width - 10  # 10 是按钮与屏幕右边缘的距离
    button_y = HEIGHT - button_height - 10  # 10 是按钮与屏幕下边缘的距离

    # 在屏幕上绘制按钮
    back_button.rect.topleft = (button_x, button_y)
    back_button.draw(rule_screen)


    # 显示返回按钮
    back_button.draw(rule_screen)
    pygame.display.flip()

    # 在新窗口中等待用户点击返回按钮
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    waiting = False  # 退出当前规则界面的循环
                    game_home()  # 返回首页
                    pygame.display.flip()  # 确保返回时刷新显示




def reset_game():
    global score, foods
    score = 0
    foods = [create_food() for _ in range(10)]  # 清空食物并重新生成


game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")  # 通关音效
game_over_background = pygame.image.load("end_background.png") # 通关背景图
bg_width, bg_height = game_over_background.get_size()

# 设定弹窗的宽度或高度，根据比例计算另一个维度
target_width = 800
target_height = int(bg_height * (target_width / bg_width))

# 确保弹窗窗口的大小和背景图片保持比例
popup_width, popup_height = target_width, target_height
game_over_background = pygame.transform.scale(game_over_background, (popup_width, popup_height))


# 游戏结束界面
def game_over_screen():
    global game_over
    global score, start_time, elapsed_pause_time, is_paused

    # 设置弹窗窗口的位置
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    
    # 创建弹窗窗口
    popup_screen = pygame.Surface((popup_width, popup_height))
    # 将拉伸后的背景图片绘制在弹窗窗口中
    popup_screen.blit(game_over_background, (0, 0))
    
    
    # 显示游戏结束信息和分数
    over_text = large_font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Score in this game: {score}", True, BLACK)
    high_score_text = font.render(f"All-time high: {high_score}", True, BLACK)

    popup_screen.blit(over_text, (popup_width // 2 - over_text.get_width() // 2, 60))
    popup_screen.blit(score_text, (popup_width // 2 - score_text.get_width() // 2, 120))
    popup_screen.blit(high_score_text, (popup_width // 2 - high_score_text.get_width() // 2, 160))
    
    # 创建重新游戏按钮
    restart_button = Button("Play Again", (WIDTH // 2 - 50, HEIGHT // 2 + 120), (140, 40))
    restart_button.rect.topleft = (popup_width // 2 - 70, 220)  # 将按钮定位在弹窗内
    restart_button.draw(popup_screen)

    # 定义退出按钮
    exit_button = Button("Exit", (WIDTH // 2 - 50, HEIGHT // 2 + 80), (100, 40))
    exit_button.rect.topleft = (popup_width // 2 - 50, 300)  # 将按钮定位在弹窗内
    exit_button.draw(popup_screen)

    # 播放通关音效
    game_over_sound.play()

    # 显示弹窗内容
    screen.blit(popup_screen, (popup_x, popup_y))
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
                # 调整鼠标坐标相对于弹窗窗口的位置
                popup_mouse_pos = (mouse_pos[0] - popup_x, mouse_pos[1] - popup_y)
                if restart_button.is_clicked(popup_mouse_pos):
                     # 重置倒计时相关变量
                    score = 0
                    start_time = time.time()  # 重新设置游戏开始时间
                    elapsed_pause_time = 0  # 清除累积的暂停时间
                    is_paused = False  # 解除暂停状态
                    game_loop()  # 重新开始游戏
                    waiting = False  # 退出等待状态
                elif exit_button.is_clicked(popup_mouse_pos):
                    print("退出游戏")
                    pygame.quit()  # 退出Pygame
                    exit()  # 退出程序
                    
        # 主窗口和弹窗窗口的显示更新
        screen.blit(background, (0, 0))  # 更新主窗口的背景
        screen.blit(popup_screen, (popup_x, popup_y))  # 保持弹窗窗口显示
        pygame.display.flip()

# 加载音乐
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # 循环播放音乐
# pygame.mixer.music.set_volume(0.3)  # 设置背景音乐音量，0.3表示稍微调小音量

# 右上角的暂停按钮
pause_button = Button("Pause", (WIDTH - 110, 10), (100, 40))



# 加载音频文件
direction_sounds = [
    pygame.mixer.Sound("direction_change-1.mp3"),
    pygame.mixer.Sound("direction_change-2.mp3"),
    pygame.mixer.Sound("direction_change-3.mp3")
]
sound_index = 0  # 音频播放索引
previous_direction = None  # 上一次的方向（'left' or 'right'）
movement_in_progress = False  # 标记是否在进行移动
# 在主游戏界面上方增加一个工具栏高度
TOOLBAR_HEIGHT = 50
TOOLBAR_COLOR = (220, 220, 220, 180)  # RGBA格式，A代表透明度（0-255）



# 绘制工具栏，带透明背景
def draw_toolbar():
    # 创建带透明度的工具栏
    toolbar_surface = pygame.Surface((WIDTH, TOOLBAR_HEIGHT), pygame.SRCALPHA)  # 允许透明度
    toolbar_surface.fill(TOOLBAR_COLOR)
    screen.blit(toolbar_surface, (0, 0))

   
    # 绘制暂停按钮
    pause_button.draw(screen)

# 暂停窗口，包含“返回游戏”按钮
def show_pause_menu():
    popup_width, popup_height = 300, 200
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    
    # 创建暂停弹窗
    popup_screen = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_screen.fill(WHITE)
    pause_text = font.render("Settings", True, BLACK)
    volume_text = font.render("Music Volume", True, BLACK)

    # 音量调节滑块初始值
    volume_level = int(pygame.mixer.music.get_volume() * 100)

    # 创建返回游戏按钮
    resume_button = Button("Continue", (popup_x + popup_width // 2 - 70, popup_y + popup_height - 60), (140, 40))

    def draw_volume_slider():
        pygame.draw.line(popup_screen, BLACK, (50, 120), (250, 120), 3)  # 滑块背景线
        pygame.draw.circle(popup_screen, (0, 0, 255), (50 + 2 * volume_level, 120), 10)  # 音量滑块点
        

    # 在弹窗上绘制内容
    popup_screen.blit(pause_text, (popup_width // 2 - pause_text.get_width() // 2, 20))
    popup_screen.blit(volume_text, (30, 80))
    draw_volume_slider()
    screen.blit(popup_screen, (popup_x, popup_y))
    resume_button.draw(screen)  # 绘制返回游戏按钮
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # 检查是否点击了返回游戏按钮
                if resume_button.is_clicked(mouse_pos):
                    waiting = False  # 关闭暂停窗口并返回游戏
                
                # 检查是否在滑块范围内点击调整音量
                elif popup_x + 50 <= mouse_pos[0] <= popup_x + 250 and popup_y + 110 <= mouse_pos[1] <= popup_y + 130:
                    adjusting_volume = True
                    while adjusting_volume:
                        for evt in pygame.event.get():
                            if evt.type == pygame.MOUSEBUTTONUP:
                                adjusting_volume = False
                            elif evt.type == pygame.MOUSEMOTION:
                                mouse_x = pygame.mouse.get_pos()[0]
                                volume_level = min(max((mouse_x - popup_x - 50) // 2, 0), 100)
                                pygame.mixer.music.set_volume(volume_level / 100)
                                # 保持透明背景
                                popup_screen.fill(WHITE)
                                # 绘制文本和音量滑块
                                popup_screen.blit(pause_text, (popup_width // 2 - pause_text.get_width() // 2, 20))
                                popup_screen.blit(volume_text, (30, 80))
                                draw_volume_slider()  # 更新音量滑块
                                screen.blit(popup_screen, (popup_x, popup_y))  # 绘制更新后的弹窗
                                resume_button.draw(screen)  # 绘制返回游戏按钮

                                pygame.display.flip()

pause_start_time = 0  # 记录暂停开始的时间
elapsed_pause_time = 0  # 累积暂停时间
# 主游戏循环
def game_loop():
    reset_game()
    global score, high_score, game_over, is_paused, foods, character_image, sound_index, previous_direction, movement_in_progress, elapsed_pause_time

    score = 0
    start_time = time.time()
    game_over = False

    # 初始化当前方向为右
    current_direction = 'right'


    while not game_over:
        screen.blit(background, (0, 0))  # 绘制游戏背景
        draw_toolbar()  # 绘制顶部工具栏
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                elif event.key == pygame.K_ESCAPE:
                    return  # 返回首页
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_button.is_clicked(mouse_pos):
                    is_paused = True
                    pause_start_time = time.time()  # 记录暂停开始的时间
                    show_pause_menu()  # 显示暂停菜单
                    elapsed_pause_time += time.time() - pause_start_time  # 累加暂停时间
                    is_paused = False

        if not is_paused:  # 只有在未暂停的情况下，才继续更新计时
            
            # print(f"剩余时间: {remaining_time}s")  # 打印倒计时

            keys = pygame.key.get_pressed()
            current_direction = None  # 用来记录当前方向
            
            if keys[pygame.K_LEFT] and character.left > 0:
                # 角色向左移动
                if current_direction != 'left':  # 检查方向是否变化
                    current_direction = 'left'
                    # 播放音频并更新计数器
                    # direction_sounds[direction_change_count % 3].play()
                    # direction_change_count += 1
                character.x -= character_speed
                character_image = left_image

            elif keys[pygame.K_RIGHT] and character.right < WIDTH:
                # 角色向右移动
                if current_direction != 'right':  # 检查方向是否变化
                    current_direction = 'right'
                    # 播放音频并更新计数器
                    # direction_sounds[direction_change_count % 3].play()
                    # direction_change_count += 1
                character.x += character_speed
                character_image = right_image

            # 检查方向变化
            if current_direction:
                if current_direction != previous_direction:
                    # 播放当前索引的音频
                    direction_sounds[sound_index].play()

                    # 更新音频索引，以在下一次播放不同的音频
                    sound_index = (sound_index + 1) % len(direction_sounds)
                    
                    # 更新方向和长按状态
                    previous_direction = current_direction
                    movement_in_progress = True

                elif not movement_in_progress:
                    # 在当前方向上首次长按，不重复播放音频
                    movement_in_progress = True

            else:
                # 停止移动，重置长按状态
                movement_in_progress = False
                previous_direction = None



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

            elapsed_time = int(time.time() - start_time - elapsed_pause_time)  # 扣除暂停时间
            remaining_time = max(time_limit - elapsed_time, 0)
            score_text = font.render(f"Score: {score}", True, BLACK)
            time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(time_text, (200, 10))

            if remaining_time <= 0:
                game_over = True
                high_score = max(high_score, score)

        pygame.display.flip()
        pygame.time.delay(10)

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
