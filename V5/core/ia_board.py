# core/ia_board.py
from .base_board import BaseBoard, GRID_SIZE, EMPTY, SHIP
import random

FLEET = [4, 3, 2, 2, 1, 1]


class IaBoard(BaseBoard):
    def __init__(self):
        super().__init__()
        self.place_all_ships()

    def place_all_ships(self):
        for size in FLEET:
            placed = False
            while not placed:
                r = random.randint(0, GRID_SIZE - 1)
                c = random.randint(0, GRID_SIZE - 1)
                horizontal = random.choice([True, False])

                if self.can_place_ship(r, c, size, horizontal):
                    self.place_ship(r, c, size, horizontal)
                    placed = True

    def can_place_ship(self, r, c, size, horizontal):
        if horizontal:
            if c + size > GRID_SIZE:
                return False
            for cc in range(c, c + size):
                if self.grid[r][cc] != EMPTY:
                    return False
        else:
            if r + size > GRID_SIZE:
                return False
            for rr in range(r, r + size):
                if self.grid[rr][c] != EMPTY:
                    return False
        return True

    def place_ship(self, r, c, size, horizontal):
        coords = []
        if horizontal:
            for cc in range(c, c + size):
                self.grid[r][cc] = SHIP
                coords.append((r, cc))
        else:
            for rr in range(r, r + size):
                self.grid[rr][c] = SHIP
                coords.append((rr, c))
        self.ships.append(coords)