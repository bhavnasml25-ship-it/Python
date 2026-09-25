


import pygame
import random
import sys


CELL_SIZE = 24
GRID_WIDTH = 26
GRID_HEIGHT = 18
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + 70  

SPEEDS = {
    "Slow": 6,
    "Medium": 10,
    "Fast": 15,
}
SPEED_ORDER = ["Slow", "Medium", "Fast"]
SPEEDUP_EVERY = 6  # score points needed before nudging speed up slightly
MAX_SPEED_BONUS = 6


BG = (24, 27, 34)
BLACK = (12, 13, 17)
WHITE = (240, 240, 240)
GRAY = (120, 120, 130)
YELLOW = (240, 200, 60)
GRID_LINE = (34, 38, 47)


SNAKE_TOP = (86, 214, 120)
SNAKE_LIGHT = (140, 235, 165)
SNAKE_MID = (52, 168, 90)
SNAKE_DARK = (24, 100, 52)
SNAKE_HEAD_TOP = (250, 235, 90)
SNAKE_HEAD_LIGHT = (255, 245, 150)
SNAKE_HEAD_MID = (220, 180, 40)
SNAKE_HEAD_DARK = (150, 115, 15)



FOOD_LIGHT = (255, 140, 130)
FOOD_MID = (220, 60, 60)
FOOD_DARK = (130, 25, 25)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game 3D")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("consolas", 22)
        self.font_med = pygame.font.SysFont("consolas", 28, bold=True)
        self.font_big = pygame.font.SysFont("consolas", 48, bold=True)
        self.high_score = 0

        self.state = "menu"        
        
        self.selected_speed_idx = 1 
        
        
        self.reset()

 
 
    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.speed_name = SPEED_ORDER[self.selected_speed_idx]
        self.base_fps = SPEEDS[self.speed_name]
        self.fps = self.base_fps
        self.food = self.spawn_food()



    def spawn_food(self):
        occupied = set(self.snake)
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_speed_idx = (self.selected_speed_idx - 1) % len(SPEED_ORDER)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_speed_idx = (self.selected_speed_idx + 1) % len(SPEED_ORDER)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset()
                    self.state = "playing"
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif self.state == "playing":
                if event.key in (pygame.K_UP, pygame.K_w) and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != LEFT:
                    self.next_direction = RIGHT
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif self.state == "game_over":
                if event.key == pygame.K_r:
                    self.state = "menu"
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()


    def update(self):
        if self.state != "playing":
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.end_game()
            return

        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            bonus = min(self.score // SPEEDUP_EVERY, MAX_SPEED_BONUS)
            self.fps = self.base_fps + bonus
            self.food = self.spawn_food()
        else:
            self.snake.pop()


    def end_game(self):
        self.state = "game_over"
        self.high_score = max(self.high_score, self.score)


    def draw_cube(self, x, y, top, light, mid, dark, bevel=5):
        """Draw a cell as a beveled cube for a pseudo-3D effect."""
        px = x * CELL_SIZE
        py = y * CELL_SIZE + 70
        size = CELL_SIZE

        # drop shadow
        shadow_rect = (px + 3, py + 4, size - 2, size - 2)
        shadow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 70), (0, 0, size - 2, size - 2), border_radius=6)
        self.screen.blit(shadow_surf, (px + 3, py + 4))

     
     
        base_rect = (px + 1, py + 1, size - 2, size - 2)
        pygame.draw.rect(self.screen, mid, base_rect, border_radius=6)

        # top-left highlight face (gives raised look)
        highlight_poly = [
            (px + 1, py + 1 + bevel),
            (px + 1 + bevel, py + 1),
            (px + size - 1 - bevel, py + 1),
            (px + size - 1, py + 1 + bevel),
            (px + size - 1 - bevel, py + 1 + 2 * bevel),
            (px + 1 + bevel, py + 1 + 2 * bevel),
        ]
        pygame.draw.polygon(self.screen, light, highlight_poly)

        # small top face
        pygame.draw.rect(self.screen, top, (px + 1 + bevel, py + 1, size - 2 - 2 * bevel, bevel))

        # bottom-right shade (gives depth)
        shade_rect = (px + 1, py + size - 1 - bevel, size - 2, bevel)
        pygame.draw.rect(self.screen, dark, shade_rect, border_radius=4)

        # outer border for crispness
        pygame.draw.rect(self.screen, BLACK, base_rect, width=1, border_radius=6)

    def draw_food(self):
        fx, fy = self.food
        px = fx * CELL_SIZE + CELL_SIZE // 2
        py = fy * CELL_SIZE + 70 + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2

        # shadow
        shadow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 80), (CELL_SIZE // 2 + 2, CELL_SIZE // 2 + 3), radius)
        self.screen.blit(shadow_surf, (fx * CELL_SIZE, fy * CELL_SIZE + 70))

        # base sphere
        pygame.draw.circle(self.screen, FOOD_DARK, (px, py), radius)
        pygame.draw.circle(self.screen, FOOD_MID, (px, py), radius - 2)
        # highlight (upper-left) to simulate roundness
        pygame.draw.circle(self.screen, FOOD_LIGHT, (px - radius // 3, py - radius // 3), max(radius // 3, 2))

    # -----------------------------------------------------------------
    def draw_grid_lines(self):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_LINE, (x, 70), (x, SCREEN_HEIGHT), 1)
        for y in range(70, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_LINE, (0, y), (SCREEN_WIDTH, y), 1)

    # -----------------------------------------------------------------
    def draw_top_bar(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 70))
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        high_text = self.font_small.render(f"High Score: {self.high_score}", True, YELLOW)
        speed_text = self.font_small.render(f"Speed: {self.speed_name}", True, GRAY)
        self.screen.blit(score_text, (15, 22))
        self.screen.blit(speed_text, (SCREEN_WIDTH // 2 - speed_text.get_width() // 2, 22))
        self.screen.blit(high_text, (SCREEN_WIDTH - high_text.get_width() - 15, 22))

    # -----------------------------------------------------------------
    def draw_menu(self):
        self.screen.fill(BG)
        title = self.font_big.render("SNAKE", True, SNAKE_TOP)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        subtitle = self.font_small.render("Choose your speed", True, GRAY)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 140))

        start_y = 200
        gap = 60
        for i, name in enumerate(SPEED_ORDER):
            selected = (i == self.selected_speed_idx)
            color = YELLOW if selected else WHITE
            label = f"{'>  ' if selected else '   '}{name}  ({SPEEDS[name]} fps){'  <' if selected else ''}"
            text = self.font_med.render(label, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, start_y + i * gap))

        hint = self.font_small.render("UP/DOWN to choose   |   ENTER to start   |   Q to quit", True, GRAY)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, start_y + len(SPEED_ORDER) * gap + 40))

    # -----------------------------------------------------------------
    def draw_playing(self):
        self.screen.fill(BG)
        self.draw_top_bar()
        self.draw_grid_lines()

        self.draw_food()

        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                self.draw_cube(x, y, SNAKE_HEAD_TOP, SNAKE_HEAD_LIGHT, SNAKE_HEAD_MID, SNAKE_HEAD_DARK)
            else:
                self.draw_cube(x, y, SNAKE_TOP, SNAKE_LIGHT, SNAKE_MID, SNAKE_DARK)

    # -----------------------------------------------------------------
    def draw_game_over(self):
        self.draw_playing()

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.font_big.render("GAME OVER", True, (220, 60, 60))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        score_line = self.font_med.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score_line, (SCREEN_WIDTH // 2 - score_line.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        prompt = self.font_small.render("Press R for Menu   |   Q / ESC to Quit", True, GRAY)
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    # -----------------------------------------------------------------
    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_playing()
        elif self.state == "game_over":
            self.draw_game_over()

        pygame.display.flip()

    # -----------------------------------------------------------------
    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            tick_fps = self.fps if self.state == "playing" else 30
            self.clock.tick(tick_fps)


if __name__ == "__main__":
    SnakeGame().run()
