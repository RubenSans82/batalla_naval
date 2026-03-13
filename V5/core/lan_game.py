from .base_game import BaseGame
from .lan_board import LanBoard
from .base_board import HIT, MISS, EMPTY


class LanGame(BaseGame):
    def __init__(self):
        super().__init__(LanBoard)

    def local_shot_request(self, r, c):
        if not self.my_turn or self.game_over:
            return False
        if self.enemy_view[r][c] != EMPTY:
            return False
        return True

    def apply_result(self, r, c, hit):
        self.enemy_view[r][c] = HIT if hit else MISS
        self.my_turn = hit  # <<--- regla correcta

    def apply_sunk(self, coords):
        self.enemy_sunk_ships.append(coords)
        return coords

    def apply_gameover(self):
        self.game_over = True
        self.winner = "Jugador"