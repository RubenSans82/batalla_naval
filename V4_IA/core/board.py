import random

GRID_SIZE = 8

EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3

FLEET = [4, 3, 2, 2, 1, 1]

class Board:
    def __init__(self):
        # Matriz del tablero
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Lista de barcos, cada uno es una lista de coordenadas [(r,c), (r,c)...]
        self.ships = []

        # Colocación automática de barcos
        self.place_all_ships()

    # ---------------------------------------------------------
    #  COLOCACIÓN DE BARCOS
    # ---------------------------------------------------------

    def place_all_ships(self):
        
        ship_sizes = FLEET

        for size in ship_sizes:
            placed = False
            while not placed:
                r = random.randint(0, GRID_SIZE - 1)
                c = random.randint(0, GRID_SIZE - 1)
                horizontal = random.choice([True, False])

                if self.can_place_ship(r, c, size, horizontal):
                    self.place_ship(r, c, size, horizontal)
                    placed = True

    def can_place_ship(self, r, c, size, horizontal):
        """
        Comprueba si un barco cabe sin solaparse.
        """
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
        """
        Coloca un barco en el tablero.
        """
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

    # ---------------------------------------------------------
    #  DISPAROS Y HUNDIMIENTOS
    # ---------------------------------------------------------

    def shoot(self, r, c):
        """
        Aplica un disparo en (r,c).
        Devuelve True si es HIT, False si es MISS.
        """
        if self.grid[r][c] == SHIP:
            self.grid[r][c] = HIT
            return True
        elif self.grid[r][c] == EMPTY:
            self.grid[r][c] = MISS
            return False
        else:
            # Ya estaba disparado (HIT o MISS)
            return False

    def check_sunk(self, r, c):
        """
        Comprueba si el disparo en (r,c) ha hundido un barco.
        Devuelve la lista de coordenadas del barco hundido o None.
        """
        for ship in self.ships:
            if (r, c) in ship:
                # ¿Todas las casillas están en estado HIT?
                if all(self.grid[rr][cc] == HIT for (rr, cc) in ship):
                    return ship
        return None

    def all_sunk(self):
        """
        Devuelve True si todos los barcos están hundidos.
        """
        for ship in self.ships:
            for (r, c) in ship:
                if self.grid[r][c] != HIT:
                    return False
        return True