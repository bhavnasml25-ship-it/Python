import os
import sys
import time
import random

try:
    import msvcrt
except ImportError:
    print("This game uses 'msvcrt' and must be run on Windows in Command Prompt.")
    sys.exit(1)

WIDTH = 30
HEIGHT = 20
BORDER_CHAR = "#"
SNAKE_HEAD_CHAR = "O"
SNAKE_BODY_CHAR = "o"
FOOD_CHAR = "*"
EMPTY_CHAR = " "


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def choose_speed():
    print("=" * 40)
    print("        SNAKE GAME - CHOOSE SPEED")
    print("=" * 40)
    print("1. Slow")
    print("2. Medium")
    print("3. Fast")
    print("=" * 40)

    speed_map = {
        "1": 0.20,
        "2": 0.12,
        "3": 0.07,
    }

    while True:
        choice = input("Enter choice (1/2/3): ").strip()
        if choice in speed_map:
            return speed_map[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def create_snake_and_food():
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = (1, 0)
    food = place_food(snake)
    return snake, direction, food


def place_food(snake):
    while True:
        fx = random.randint(1, WIDTH - 2)
        fy = random.randint(1, HEIGHT - 2)
        if (fx, fy) not in snake:
            return (fx, fy)


def take_keyboard_input(current_direction):
    new_direction = current_direction

    while msvcrt.kbhit():
        key = msvcrt.getch()

        if key in (b"\xe0", b"\x00"):
            key2 = msvcrt.getch()
            if key2 == b"H":
                candidate = (0, -1)
            elif key2 == b"P":
                candidate = (0, 1)
            elif key2 == b"K":
                candidate = (-1, 0)
            elif key2 == b"M":
                candidate = (1, 0)
            else:
                candidate = current_direction
        else:
            k = key.lower()
            if k == b"w":
                candidate = (0, -1)
            elif k == b"s":
                candidate = (0, 1)
            elif k == b"a":
                candidate = (-1, 0)
            elif k == b"d":
                candidate = (1, 0)
            elif k == b"q":
                return "QUIT"
            else:
                candidate = current_direction

        if (candidate[0] * -1, candidate[1] * -1) != current_direction:
            new_direction = candidate

    return new_direction


def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    return new_head


def hit_wall_or_body(new_head, snake):
    x, y = new_head
    if x <= 0 or x >= WIDTH - 1 or y <= 0 or y >= HEIGHT - 1:
        return True
    if new_head in snake:
        return True
    return False


def draw_game(snake, food, score, speed_label):
    clear_screen()

    grid = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x in range(WIDTH):
        grid[0][x] = BORDER_CHAR
        grid[HEIGHT - 1][x] = BORDER_CHAR
    for y in range(HEIGHT):
        grid[y][0] = BORDER_CHAR
        grid[y][WIDTH - 1] = BORDER_CHAR

    fx, fy = food
    grid[fy][fx] = FOOD_CHAR

    for i, (sx, sy) in enumerate(snake):
        if 0 <= sy < HEIGHT and 0 <= sx < WIDTH:
            grid[sy][sx] = SNAKE_HEAD_CHAR if i == 0 else SNAKE_BODY_CHAR

    print(f"SNAKE GAME   |   Score: {score}")
    print("Controls: W A S D or Arrow Keys | Q to Quit")
    print("-" * WIDTH)
    for row in grid:
        print("".join(row))


def game_over_screen(score):
    clear_screen()
    print("=" * 40)
    print("               GAME OVER")
    print("=" * 40)
    print(f"Final Score: {score}")
    print("=" * 40)


def main():
    speed = choose_speed()
    snake, direction, food = create_snake_and_food()
    score = 0

    draw_game(snake, food, score, speed)

    while True:
        loop_start = time.time()

        direction = take_keyboard_input(direction)
        if direction == "QUIT":
            break

        new_head = move_snake(snake, direction)

        if hit_wall_or_body(new_head, snake):
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        draw_game(snake, food, score, speed)

        elapsed = time.time() - loop_start
        remaining = speed - elapsed
        if remaining > 0:
            time.sleep(remaining)

    game_over_screen(score)


if __name__ == "__main__":
    main()
