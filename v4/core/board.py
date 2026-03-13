import random

GRID_SIZE = 8
EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3

FLEET = [4, 3, 2, 2, 1, 1]


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
        if self.grid[r][c] == SHIP:
            self.grid[r][c] = HIT
            return True
        else:
            if self.grid[r][c] == EMPTY:
                self.grid[r][c] = MISS
            return False

    def all_sunk(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == SHIP:
                    return False
        return True