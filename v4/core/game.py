from core.board import Board, GRID_SIZE, EMPTY, HIT, MISS, SHIP

LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120
CELL_SIZE = 50


class Game:
    def __init__(self):
        self.player_board = Board()
        self.enemy_view = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.player_board.place_fleet()

        self.my_turn = False
        self.game_over = False
        self.winner = None

    def set_starting_player(self, am_i_server):
        self.my_turn = am_i_server

    def click_to_coords(self, mx, my):
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        if mx <= enemy_x or my <= enemy_y:
            return None

        c = (mx - enemy_x) // CELL_SIZE
        r = (my - enemy_y) // CELL_SIZE

        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            return r, c
        return None

    # -------------------------
    # YO DISPARO
    # -------------------------
    def local_shot_request(self, r, c):
        if not self.my_turn or self.game_over:
            return None

        if self.enemy_view[r][c] != EMPTY:
            return None

        return True

    # -------------------------
    # RECIBO RESULT
    # -------------------------
    def apply_result(self, r, c, hit):
        self.enemy_view[r][c] = HIT if hit else MISS
        self.my_turn = hit

    # -------------------------
    # RECIBO SUNK (lista completa)
    # -------------------------
    def apply_sunk(self, coords):
        # coords es una lista [(r,c), (r,c), ...]
        # no modificamos enemy_view (ya tiene HITs)
        return coords

    # -------------------------
    # RECIBO SHOT DEL ENEMIGO
    # -------------------------
    def receive_enemy_shot(self, r, c):
        hit = self.player_board.receive_shot(r, c)

        sunk_ship = None
        if hit:
            for ship in self.player_board.ships:
                if all(self.player_board.grid[rr][cc] == HIT for rr, cc in ship):
                    if (r, c) in ship:
                        sunk_ship = ship
                        break

        if hit and self.player_board.all_sunk():
            self.game_over = True
            self.winner = "Enemigo"

        self.my_turn = not hit

        return hit, sunk_ship