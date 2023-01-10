import os
import sys

import pygame

# settings
pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arcanoid')
# fon color
startScreen_color = ("#DDBEAA")
bg = ("#1950A0")
# blocks color
block_red = ("#F63232")
block_green = ("#58B822")
block_blue = ("#2681EB")
platform_color = ("#E5E3E4")
# shadow color
red_shadow = ("#BC3838")
green_shadow = ("#3E8317")
blue_shadow = ("#255996")
platform_shadow = ("#C1C1C1")

cols = 6
rows = 6

map_count = 0
score = 0

FPS = int(screen_height / 10 + 20)
clock = pygame.time.Clock()

game_over = None


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print("Can't load image")
        terminate()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["Arcanoid Pygame", "Начать игру", 'Выход']
    font = pygame.font.Font(None, 60)
    text_coord = 80
    text_x = screen_width // 2
    button = None
    button2 = None
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = text_x - (intro_rect.width // 2)
        font = pygame.font.Font(None, 40)
        screen.blit(string_rendered, intro_rect)
        text_coord += 100
        if intro_text.index(line) == 1:
            button = intro_rect
        elif intro_text.index(line) == 2:
            button2 = intro_rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.right >= event.pos[0] >= button.x:
                    if button.bottom >= event.pos[1] >= button.y:
                        return
                if button2.right >= event.pos[0] >= button2.x:
                    if button2.bottom >= event.pos[1] >= button2.y:
                        terminate()

        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    if game_over == 2:
        intro_text = ["Вы выиграли!", f"Ваш счет {score}", "Выход в главное меню", "Выход"]
    elif game_over == -1:
        intro_text = ["Вы проиграли!", f"Ваш счет: {score}", "Выход в главное меню", "Выход"]

    # screen.fill(startScreen_color)
    font = pygame.font.Font(None, 50)
    text_coord = screen_height / 2 - 80
    text_x = screen_width // 2
    button, button2 = None, None
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = text_x - (intro_rect.width // 2)
        font = pygame.font.Font(None, 40)
        screen.blit(string_rendered, intro_rect)
        text_coord += 50
        if intro_text.index(line) == 2:
            button = intro_rect
        elif intro_text.index(line) == 3:
            button2 = intro_rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.right >= event.pos[0] >= button.x:
                    if button.bottom >= event.pos[1] >= button.y:
                        return 'restart'
                if button2.right >= event.pos[0] >= button2.x:
                    if button2.bottom >= event.pos[1] >= button2.y:
                        return 'exit'

        pygame.display.flip()
        clock.tick(FPS)


def load_level(*maps):
    global cols, rows, map_count
    level_map_list = []
    for filename in maps:
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        cols = max(map(len, level_map))
        rows = len(level_map)
        level_map_list.append((level_map, cols, rows))
    map_count = len(level_map_list) - 1
    return level_map_list


class wall():
    def __init__(self):
        self.map_number = 0

    def create_wall(self, level_map_list):
        self.cols = level_map_list[self.map_number][1]
        self.rows = level_map_list[self.map_number][2]
        self.width = screen_width // self.cols
        self.height = 50
        self.map = level_map_list[self.map_number][0]
        self.blocks = []
        self.blocks_count = 0
        for row in self.map:
            for col in row:
                if col in ('1', '2', '3'):
                    self.blocks_count += 1
        for row in range(len(self.map)):
            block_row = []
            strength = 1
            for col in range(len(self.map[row])):
                try:
                    col_n = int(self.map[row][col])
                except ValueError:
                    col_n = 0
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x + 4, block_y + 4, self.width - 6, self.height - 6)
                shadow = pygame.Rect(block_x + 2, block_y + 2, self.width - 2, self.height - 2)
                if col_n == 3:
                    strength = 3
                elif col_n == 2:
                    strength = 2
                elif col_n == 1:
                    strength = 1
                elif col_n == 0:
                    rect = pygame.Rect(0, 0, 0, 0)
                    shadow = pygame.Rect(0, 0, 0, 0)
                block = [rect, shadow, strength]
                block_row.append(block)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[2] == 3:
                    block_col = block_blue
                    shadow = blue_shadow
                elif block[2] == 2:
                    block_col = block_green
                    shadow = green_shadow
                elif block[2] == 1:
                    block_col = block_red
                    shadow = red_shadow
                pygame.draw.rect(screen, shadow, block[1])
                pygame.draw.rect(screen, block_col, block[0])


class platform:
    def __init__(self):
        self.pl_width = 150
        self.pl_height = 30
        self.pl_x = screen_width // 2 - self.pl_width // 2
        self.pl_y = screen_height - 60
        self.platform = pygame.Rect(self.pl_x + 2, self.pl_y + 2, self.pl_width - 2, self.pl_height - 2)
        self.shadow = pygame.Rect(self.pl_x, self.pl_y, self.pl_width + 2, self.pl_height + 2)
        self.speed = 15
        self.direction = 0

    def draw_platform(self):
        pygame.draw.rect(screen, platform_shadow, self.shadow)
        pygame.draw.rect(screen, platform_color, self.platform)

    def update_platform(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.shadow.right < screen_width - 5:
            self.platform = self.platform.move(self.speed, 0)
            self.shadow = self.shadow.move(self.speed, 0)
            self.direction = 1
        if key[pygame.K_LEFT] and self.shadow.left > 5:
            self.platform = self.platform.move(-self.speed, 0)
            self.shadow = self.shadow.move(-self.speed, 0)
            self.direction = -1


class ball:
    def __init__(self, x, y):
        self.ball_radius = 12
        self.x = x - self.ball_radius
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 6
        self.speed_y = -6
        self.speed = 15
        self.speed_max = 8
        self.game_over = 0
        self.count = 0

    def draw_ball(self):
        pygame.draw.circle(screen, platform_shadow, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius + 2)
        pygame.draw.circle(screen, platform_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)

    def update_ball(self):
        global score
        collision = 7
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision and self.speed_x < 0:
                        self.speed_x *= -1

                    if wall.blocks[row_count][item_count][2] > 1:
                        wall.blocks[row_count][item_count][2] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = pygame.Rect(0, 0, 0, 0)
                        wall.blocks[row_count][item_count][1] = pygame.Rect(0, 0, 0, 0)
                        wall.blocks_count -= 1
                        score += item[2]

                item_count += 1
            row_count += 1

        font = pygame.font.Font(None, 40)
        text = 'Нажмите пробел чтобы начать'
        if not ball_running:
            font = font.render(text, 1, pygame.Color('white'))
            key = pygame.key.get_pressed()
            screen.blit(font, (100, screen_height / 2 - 20))
            if key[pygame.K_RIGHT] and self.rect.right < screen_width - 5:
                self.rect = self.rect.move(self.speed, 0)
            if key[pygame.K_LEFT] and self.rect.left > 5:
                self.rect = self.rect.move(-self.speed, 0)
        else:
            if self.rect.left < 0 or self.rect.right > screen_width:
                self.speed_x *= -1
            if self.rect.top < 0:
                self.speed_y *= -1

            if self.rect.bottom > screen_height:
                self.game_over = -1

            if self.rect.colliderect(platform.platform):
                if abs(self.rect.bottom - platform.platform.top) < collision and self.speed_y > 0:
                    self.speed_y *= -1
                    self.speed_x += platform.direction
                    if self.speed_x > self.speed_max:
                        self.speed_x = self.speed_max
                    elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                        self.speed_x = -self.speed_max
                else:
                    self.speed_x *= -1
            self.rect = self.rect.move(self.speed_x, self.speed_y)

            if wall.blocks_count == 0:
                if map_count != 0:
                    self.game_over = 1
                    wall.map_number += 1
                    self.rect.x = self.x
                    self.rect.y = self.y
                    if self.speed_y > 0:
                        self.speed_y *= -1
                else:
                    self.game_over = 2

            return self.game_over


level_map_list = load_level('lvl1.txt', 'lvl3.txt', 'lvl2.txt')

wall = wall()
platform = platform()

ball = ball(platform.pl_x + (platform.pl_width // 2), platform.pl_y - platform.pl_height)

while True:
    image = load_image('fon.bmp')
    image = pygame.transform.scale(image, (screen_width, screen_height))

    screen.blit(image, (0, 0))
    platform.draw_platform()
    ball.draw_ball()

    start_screen()

    map_count = len(level_map_list) - 1
    wall.create_wall(level_map_list)

    game_over = 0
    score = 0

    ball_running = False
    run = True
    counter_font = pygame.font.Font(None, 30)
    while run:
        wall.draw_wall()
        text = f'Ваш счет: {score}'
        counter = counter_font.render(text, 1, pygame.Color('white'))
        screen.blit(image, (0, 0))
        wall.draw_wall()
        platform.draw_platform()
        ball.draw_ball()
        screen.blit(counter, (40, screen_height - 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not ball_running:
                    ball_running = True
        platform.update_platform()
        game_over = ball.update_ball()

        if game_over == 1:
            wall.create_wall(level_map_list)
            ball.game_over = 0
            map_count -= 1
        elif game_over == 2 or game_over == -1:
            run = False

        clock.tick(FPS)
        pygame.display.update()
    try:
        ans = end_screen()
        if ans == 'exit':
            terminate()
        elif ans == 'restart':
            ball.rect.x = ball.x
            ball.rect.y = ball.y
            if ball.speed_y > 0:
                ball.speed_y *= -1
            ball.game_over = 0
            wall.map_number = 0
            platform.platform = pygame.Rect(platform.pl_x + 2, platform.pl_y + 2, platform.pl_width - 2,
                                            platform.pl_height - 2)
            platform.shadow = pygame.Rect(platform.pl_x, platform.pl_y, platform.pl_width + 2, platform.pl_height + 2)
    except UnboundLocalError:
        terminate()
