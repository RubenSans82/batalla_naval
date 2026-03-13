import pygame
import random
import sys

pygame.init()

# ---------------------------
# CONSTANTES
# ---------------------------

GRID_SIZE = 8
CELL_SIZE = 50

LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2

BLUE = (80, 140, 220)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
BACKGROUND = (220, 220, 240)

EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3

FLEET = [4, 3, 2, 2, 1, 1]

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)


# =========================================================
# CLASE BOARD
# =========================================================

class Board:
    def __init__(self):
        self.grid = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships = []  # lista de barcos, cada barco es lista de (r,c)

    def place_fleet(self):
        for size in FLEET:
            placed = False
            while not placed:
                r = random.randint(0, GRID_SIZE - 1)
                c = random.randint(0, GRID_SIZE - 1)
                horizontal = random.choice([True, False])

                ok = True
                cells = []

                if horizontal:
                    if c + size > GRID_SIZE:
                        ok = False
                    else:
                        for i in range(size):
                            if self.grid[r][c+i] != EMPTY:
                                ok = False
                                break
                            cells.append((r, c+i))
                else:
                    if r + size > GRID_SIZE:
                        ok = False
                    else:
                        for i in range(size):
                            if self.grid[r+i][c] != EMPTY:
                                ok = False
                                break
                            cells.append((r+i, c))

                if ok:
                    for rr, cc in cells:
                        self.grid[rr][cc] = SHIP
                    self.ships.append(cells)
                    placed = True

    def receive_shot(self, r, c):
        """Devuelve True si es impacto."""
        if self.grid[r][c] == SHIP:
            self.grid[r][c] = HIT
            return True
        else:
            self.grid[r][c] = MISS
            return False

    def all_sunk(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == SHIP:
                    return False
        return True


# =========================================================
# CLASE GAME
# =========================================================

class Game:
    def __init__(self):
        self.player_board = Board()
        self.enemy_board = Board()
        self.enemy_view = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.player_board.place_fleet()
        self.enemy_board.place_fleet()

        self.player_turn = True
        self.game_over = False
        self.winner = None

    def player_shot(self, mx, my):
        if not self.player_turn or self.game_over:
            return

        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        if mx <= enemy_x or my <= enemy_y:
            return

        c = (mx - enemy_x) // CELL_SIZE
        r = (my - enemy_y) // CELL_SIZE

        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
            return

        if self.enemy_view[r][c] != EMPTY:
            return

        hit = self.enemy_board.receive_shot(r, c)
        self.enemy_view[r][c] = HIT if hit else MISS

        if hit and self.enemy_board.all_sunk():
            self.game_over = True
            self.winner = "Jugador"
        elif not hit:
            self.player_turn = False

    def ai_turn(self):
        if self.player_turn or self.game_over:
            return

        while True:
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            if self.player_board.grid[r][c] in (EMPTY, SHIP):
                break

        hit = self.player_board.receive_shot(r, c)

        if hit and self.player_board.all_sunk():
            self.game_over = True
            self.winner = "IA"
        elif not hit:
            self.player_turn = True


# =========================================================
# CLASE GAMEVIEW (DIBUJO)
# =========================================================

class GameView:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, board, x, y, show_ships):
        pygame.draw.rect(self.screen, BLACK, (x-5, y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board.grid[r][c]
                color = BLUE
                if cell == MISS:
                    color = WHITE
                elif cell == HIT:
                    color = RED
                elif cell == SHIP and show_ships:
                    color = GRAY

                pygame.draw.rect(self.screen, color, (x + c*CELL_SIZE, y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x + c*CELL_SIZE, y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Marcos
        for ship in board.ships:
            if show_ships or all(board.grid[r][c] == HIT for r, c in ship):
                self.draw_ship_frame(ship, x, y)

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

    def draw_enemy_view(self, enemy_view, enemy_board, x, y):
        pygame.draw.rect(self.screen, BLACK, (x-5, y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = enemy_view[r][c]
                color = BLUE
                if cell == MISS:
                    color = WHITE
                elif cell == HIT:
                    color = RED

                pygame.draw.rect(self.screen, color, (x + c*CELL_SIZE, y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x + c*CELL_SIZE, y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Marcos solo si hundidos
        for ship in enemy_board.ships:
            if all(enemy_view[r][c] == HIT for r, c in ship):
                self.draw_ship_frame(ship, x, y)

    def draw(self, game):
        self.screen.fill(BACKGROUND)

        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        self.screen.blit(big_font.render("Tu tablero", True, BLACK), (player_x, player_y - 40))
        self.screen.blit(big_font.render("Tablero enemigo", True, BLACK), (enemy_x, enemy_y - 40))

        self.draw_board(game.player_board, player_x, player_y, True)
        self.draw_enemy_view(game.enemy_view, game.enemy_board, enemy_x, enemy_y)

        if game.game_over:
            msg = big_font.render(f"Fin del juego: {game.winner} gana", True, BLACK)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 60))


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval - Versión 2 (POO)")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.player_shot(*event.pos)

        if not game.player_turn and not game.game_over:
            pygame.time.delay(400)
            game.ai_turn()

        view.draw(game)
        pygame.display.flip()


if __name__ == "__main__":
    main()
