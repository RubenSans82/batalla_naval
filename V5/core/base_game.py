from .base_board import GRID_SIZE, EMPTY, HIT, MISS

class BaseGame:
    def __init__(self, board_cls):
        self.player_board = board_cls()
        self.enemy_view = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.enemy_sunk_ships = []

        self.my_turn = False
        self.game_over = False
        self.winner = None

    def set_starting_player(self, is_player):
        self.my_turn = is_player

    def click_to_coords(self, x, y):
        from ui.view import LEFT_MARGIN, TOP_MARGIN, CELL_SIZE, BOARD_SPACING

        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        if x < enemy_x or y < enemy_y:
            return None

        c = (x - enemy_x) // CELL_SIZE
        r = (y - enemy_y) // CELL_SIZE

        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            return r, c
        return None

    def receive_enemy_shot(self, r, c):
        hit = self.player_board.shoot(r, c)
        sunk = self.player_board.check_sunk(r, c)

        # <<--- regla correcta
        self.my_turn = not hit

        if self.player_board.all_sunk():
            self.game_over = True
            self.winner = "Rival"

        return hit, sunk