# core/lan_board.py
from .base_board import BaseBoard, GRID_SIZE, EMPTY, SHIP
import random

FLEET = [4, 3, 2, 2, 1, 1]


class LanBoard(BaseBoard):
    def __init__(self):
        super().__init__()
        self.place_fleet()

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