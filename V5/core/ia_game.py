# core/ia_game.py
from .base_game import BaseGame
from .ia_board import IaBoard
from .base_board import HIT, MISS, EMPTY
import random


class IaGame(BaseGame):
    def __init__(self):
        super().__init__(IaBoard)
        self.enemy_board = IaBoard()

    def player_shoot(self, r, c):
        hit = self.enemy_board.shoot(r, c)
        sunk = None

        if hit:
            sunk = self.enemy_board.check_sunk(r, c)
            if sunk:
                self.enemy_sunk_ships.append(sunk)

        self.enemy_view[r][c] = HIT if hit else MISS

        if self.enemy_board.all_sunk():
            self.game_over = True
            self.winner = "Jugador"

        return hit, sunk

    def ai_choose_shot(self):
        while True:
            r = random.randint(0, 7)
            c = random.randint(0, 7)
            if self.player_board.grid[r][c] in (EMPTY, 1):
                return r, c

    def ai_shoot(self, r, c):
        hit = self.player_board.shoot(r, c)
        sunk = None

        if hit:
            sunk = self.player_board.check_sunk(r, c)

        if self.player_board.all_sunk():
            self.game_over = True
            self.winner = "IA"

        return hit, sunk