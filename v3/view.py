import pygame
from board import GRID_SIZE, EMPTY, SHIP, MISS, HIT

GRID_SIZE = GRID_SIZE
CELL_SIZE = 50
LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120

BLUE = (80, 140, 220)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
BACKGROUND = (220, 220, 240)

pygame.font.init()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)


class GameView:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def draw_ship_frame(self, ship, x, y):
        rows = [r for r, _ in ship]
        cols = [c for _, c in ship]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        rect_x = x + min_c * CELL_SIZE
        rect_y = y + min_r * CELL_SIZE
        rect_w = (max_c - min_c + 1) * CELL_SIZE
        rect_h = (max_r - min_r + 1) * CELL_SIZE

        pygame.draw.rect(self.screen, WHITE, (rect_x, rect_y, rect_w, rect_h), 4)

    def draw_player_board(self, game):
        board = game.player_board
        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN

        pygame.draw.rect(self.screen, BLACK,
                         (player_x-5, player_y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board.grid[r][c]
                color = BLUE
                if cell == MISS:
                    color = WHITE
                elif cell == HIT:
                    color = RED
                elif cell == SHIP:
                    color = GRAY

                pygame.draw.rect(self.screen, color,
                                 (player_x + c*CELL_SIZE, player_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK,
                                 (player_x + c*CELL_SIZE, player_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for ship in board.ships:
            self.draw_ship_frame(ship, player_x, player_y)

    def draw_enemy_board(self, game):
        enemy_view = game.enemy_view
        enemy_board = game.enemy_board

        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        pygame.draw.rect(self.screen, BLACK,
                         (enemy_x-5, enemy_y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = enemy_view[r][c]
                color = BLUE
                if cell == MISS:
                    color = WHITE
                elif cell == HIT:
                    color = RED

                pygame.draw.rect(self.screen, color,
                                 (enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK,
                                 (enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for ship in enemy_board.ships:
            if all(enemy_view[r][c] == HIT for r, c in ship):
                self.draw_ship_frame(ship, enemy_x, enemy_y)

    def draw(self, game):
        self.screen.fill(BACKGROUND)

        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        self.screen.blit(big_font.render("Tu tablero", True, BLACK), (player_x, player_y - 40))
        self.screen.blit(big_font.render("Tablero enemigo", True, BLACK), (enemy_x, enemy_y - 40))

        self.draw_player_board(game)
        self.draw_enemy_board(game)

        if game.game_over:
            msg = big_font.render(f"Fin del juego: {game.winner} gana", True, BLACK)
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, self.height - 60))
