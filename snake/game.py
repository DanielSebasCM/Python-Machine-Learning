import pygame
import time
from Snake import Snake
from Food import Food
import random


check_errors = pygame.init()

ASPECT_RATIO = 16/9

HEIGHT = 480
WIDTH = HEIGHT * ASPECT_RATIO

GRID_HEIGHT = 15
GRID_WIDTH = 15

SEG_SIZE = min(HEIGHT/GRID_HEIGHT, WIDTH/GRID_WIDTH)
LEFT_MARGIN = (WIDTH - GRID_WIDTH*SEG_SIZE)/2
TOP_MARGIN = (HEIGHT - GRID_HEIGHT*SEG_SIZE)/2


BODY_GAP = SEG_SIZE*0.03

SPEED = 3  # Grid squares per second
FPS = 60

snake_color = 0x788374
food_color = 0xaa644d
text_color = 0xf5e9bf
text_bg_color = 0x372a39
background_color = 0xf5e9bf


def drawBackground():
    game_window.fill(text_bg_color)
    rect = (LEFT_MARGIN, TOP_MARGIN, WIDTH - 2 *
            LEFT_MARGIN, HEIGHT - 2*TOP_MARGIN)
    pygame.draw.rect(game_window, background_color, rect)


def drawSnake():
    for segment in snake.body:
        x = segment[0] * SEG_SIZE + BODY_GAP/2 + LEFT_MARGIN
        y = segment[1] * SEG_SIZE + BODY_GAP/2 + TOP_MARGIN
        width = SEG_SIZE - BODY_GAP
        height = SEG_SIZE - BODY_GAP
        rect = (x, y, width, height)
        pygame.draw.rect(game_window, snake_color, rect)


def drawFood():
    x = food.pos[0] * SEG_SIZE + BODY_GAP/2 + LEFT_MARGIN
    y = food.pos[1] * SEG_SIZE + BODY_GAP/2 + TOP_MARGIN
    width = SEG_SIZE - BODY_GAP
    height = SEG_SIZE - BODY_GAP
    rect = (x, y, width, height)
    pygame.draw.rect(game_window, food_color, rect)


def renderFrame():
    drawBackground()
    drawSnake()
    drawFood()


def getRandFood():
    x = random.randint(0, GRID_WIDTH-1)
    y = random.randint(0, GRID_HEIGHT-1)
    if snake.contains((x, y)):
        return getRandFood()
    return Food(x, y)


def restart():
    global snake
    snake = Snake((GRID_WIDTH, GRID_HEIGHT))


def gameOver():
    font = pygame.font.SysFont("monospace", 72)
    game_window.fill(text_bg_color)
    label = font.render("GAME OVER", 1, text_color)
    game_window.blit(label, (WIDTH/2 - label.get_width()/2,
                             HEIGHT/2 - label.get_height()/2))
    pygame.display.update()
    time.sleep(3)
    restart()


fps_controller = pygame.time.Clock()
fps_controller.tick(FPS)

game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKEE")

running = True
snake = Snake((GRID_WIDTH, GRID_HEIGHT))

score = 0

food = getRandFood()

start_time = time.time()
prev_time = start_time

while running:
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = [0, -1]
            elif event.key == pygame.K_DOWN:
                snake.direction = [0, 1]
            elif event.key == pygame.K_LEFT:
                snake.direction = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                snake.direction = [1, 0]

    current_time = time.time()

    if current_time - prev_time > 1/SPEED:
        prev_time = current_time
        try:
            snake.move()
        except Exception as e:
            print(e)
            gameOver()

        if snake.head == food.pos:
            snake.size += 1
            score += 1
            food = getRandFood()

    renderFrame()
    pygame.display.update()
    fps_controller.tick(FPS)
