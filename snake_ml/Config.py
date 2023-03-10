ASPECT_RATIO = 16/9

HEIGHT = 480
WIDTH = HEIGHT * ASPECT_RATIO

GRID_HEIGHT = 15
GRID_WIDTH = 15

SEG_SIZE = min(HEIGHT/GRID_HEIGHT, WIDTH/GRID_WIDTH)
LEFT_MARGIN = (WIDTH - GRID_WIDTH*SEG_SIZE)/2
TOP_MARGIN = (HEIGHT - GRID_HEIGHT*SEG_SIZE)/2

BODY_GAP = SEG_SIZE*0.03
FOOD_GAP = SEG_SIZE*0.2

SPEED = 100  # Grid squares per second
FPS = 602

snake_color = 0x788374
food_color = 0xaa644d
text_color = 0xf5e9bf
text_bg_color = 0x372a39
background_color = 0xf5e9bf


def gridToPixel(grid_pos) -> tuple[int, int]:
    x = grid_pos[0] * SEG_SIZE + LEFT_MARGIN
    y = grid_pos[1] * SEG_SIZE + TOP_MARGIN
    return (x, y)
