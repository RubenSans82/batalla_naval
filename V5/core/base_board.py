# core/base_board.py
import random

GRID_SIZE = 8

EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3


class BaseBoard:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []

    def shoot(self, r, c):
        if self.grid[r][c] == SHIP:
            self.grid[r][c] = HIT
            return True
        elif self.grid[r][c] == EMPTY:
            self.grid[r][c] = MISS
            return False
        return False

    def check_sunk(self, r, c):
        for ship in self.ships:
            if (r, c) in ship:
                if all(self.grid[rr][cc] == HIT for (rr, cc) in ship):
                    return ship
        return None

    def all_sunk(self):
        for ship in self.ships:
            for (r, c) in ship:
                if self.grid[r][c] != HIT:
                    return False
        return True