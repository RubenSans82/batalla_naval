import random
from board import Board, GRID_SIZE, EMPTY, SHIP, HIT, MISS

LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120
CELL_SIZE = 50


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
