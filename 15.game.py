import pygame
import time
import random

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_red = (139, 0, 0)
grey = (169, 169, 169)

dis_width = 700
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка 100см')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

try:
    background_image_intro = pygame.image.load('files/HD-wallpaper-classic-snake-adventures-snake-game.jpg')
    background_image_intro = pygame.transform.scale(background_image_intro, (dis_width, dis_height))
except Exception as e:
    background_image_intro = None

try:
    background_image_game = pygame.image.load('files/891ee9a180d14aa4cb2f71100d7b3a987215d384.jpg')
    background_image_game = pygame.transform.scale(background_image_game, (dis_width, dis_height))
except Exception as e:
    background_image_game = None

try:
    snake_image = pygame.image.load('files/194210.png')
    snake_image = pygame.transform.scale(snake_image, (snake_block, snake_block))
except Exception as e:
    snake_image = None

try:
    food_image = pygame.image.load('files/—Pngtree—fresh red apple on transparent_5738625.png')
    food_image = pygame.transform.scale(food_image, (snake_block, snake_block))
except Exception as e:
    food_image = None

try:
    death_sound = pygame.mixer.Sound('files/male-scream-in-fear-123079.mp3')
    eat_sound = pygame.mixer.Sound('files/cartoon-voice-yummy-6.mp3')
except Exception as e:
    death_sound = None
    eat_sound = None

try:
    pygame.mixer.music.load('files/4b243785232586e.mp3')
    pygame.mixer.music.play(-1)
except Exception as e:
    pass

def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))

    button_text = font_style.render(text, True, white)
    dis.blit(button_text, [x + (w / 6), y + (h / 6)])

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    while intro:
        dis.fill(black)
        if background_image_intro:
            dis.blit(background_image_intro, (0, 0))

        message("Добро пожаловать в Змейка 100см", yellow)
        draw_button("Начать", 150, 400, 150, 50, red, dark_red, gameLoop)
        draw_button("Выйти", 400, 400, 150, 50, red, dark_red, quit_game)
        draw_button("Помощь", 275, 470, 150, 50, red, dark_red, show_help)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def show_help():
    help_screen = True
    while help_screen:
        dis.fill(black)
        message("Используйте стрелки для управления змейкой", yellow)
        draw_button("Назад", 300, 400, 150, 50, red, dark_red, game_intro)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def Your_score(score):
    value = score_font.render("Ваш см: " + str(score), True, black)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        if snake_image:
            dis.blit(snake_image, (x[0], x[1]))
        else:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def generate_random_barriers(num_barriers, barrier_width, barrier_height):
    barriers = []
    for _ in range(num_barriers):
        x = round(random.randrange(0, dis_width - barrier_width) / 10.0) * 10.0
        y = round(random.randrange(0, dis_height - barrier_height) / 10.0) * 10.0
        barrier = pygame.Rect(x, y, barrier_width, barrier_height)
        barriers.append(barrier)

    # Добавляем барьеры по краям
    barriers.append(pygame.Rect(0, 0, dis_width, 10))  # верхняя граница
    barriers.append(pygame.Rect(0, dis_height - 10, dis_width, 10))  # нижняя граница
    barriers.append(pygame.Rect(0, 0, 10, dis_height))  # левая граница
    barriers.append(pygame.Rect(dis_width - 10, 0, 10, dis_height))  # правая граница
    return barriers

def check_collision_with_barrier(x, y, barriers):
    for barrier in barriers:
        if barrier.collidepoint(x, y):
            return True
    return False

def draw_barriers(barriers):
    for barrier in barriers:
        pygame.draw.rect(dis, grey, barrier)

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    num_barriers = 7
    barrier_width = 200
    barrier_height = 20
    barriers = generate_random_barriers(num_barriers, barrier_width, barrier_height)

    while not game_over:
        while game_close:
            dis.fill(white)
            if background_image_game:
                dis.blit(background_image_game, (0, 0))

            message("лошок", red)
            Your_score(Length_of_snake - 1)
            draw_button("Заново", 150, 400, 150, 50, red, dark_red, gameLoop)
            draw_button("Выйти", 400, 400, 150, 50, red, dark_red, quit_game)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0 or check_collision_with_barrier(x1, y1, barriers):
            game_close = True
            if death_sound:
                death_sound.play()

        dis.fill(blue)
        if background_image_game:
            dis.blit(background_image_game, (0, 0))

        if food_image:
            dis.blit(food_image, (foodx, foody))
        else:
            pygame.draw.circle(dis, green, (int(foodx + snake_block / 2), int(foody + snake_block / 2)), snake_block // 2)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                if death_sound:
                    death_sound.play()

        our_snake(snake_block, snake_List)
        draw_barriers(barriers)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            if eat_sound:
                eat_sound.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_intro()
