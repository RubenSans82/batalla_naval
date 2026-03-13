from .board import Board, GRID_SIZE, EMPTY, SHIP, MISS, HIT
import random


class Game:
    def __init__(self):
        self.player_board = Board()
        self.enemy_board = Board()

        # Vista del tablero enemigo (lo que el jugador ve)
        self.enemy_view = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Barcos hundidos del enemigo (para dibujar marcos)
        self.enemy_sunk_ships = []

        # Estado del juego
        self.my_turn = False
        self.game_over = False
        self.winner = None

    # ---------------------------------------------------------
    #  COMÚN A AMBAS VERSIONES
    # ---------------------------------------------------------

    def set_starting_player(self, is_player):
        self.my_turn = is_player

    def click_to_coords(self, x, y):
        """
        Convierte un clic en coordenadas del tablero enemigo.
        La vista se encarga de calcular márgenes.
        """
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

    # ---------------------------------------------------------
    #  MÉTODOS USADOS EN MULTIJUGADOR
    # ---------------------------------------------------------

    def local_shot_request(self, r, c):
        """
        Comprueba si el jugador puede disparar en (r,c).
        Devuelve True si el disparo es válido y debe enviarse por red.
        """
        if not self.my_turn:
            return False

        if self.enemy_view[r][c] in (HIT, MISS):
            return False

        self.my_turn = False
        return True

    def apply_result(self, r, c, hit):
        """
        El rival nos informa del resultado de nuestro disparo.
        """
        self.enemy_view[r][c] = HIT if hit else MISS

    def apply_sunk(self, coords):
        """
        El rival nos informa de que un barco ha sido hundido.
        """
        self.enemy_sunk_ships.append(coords)
        return coords

    def apply_gameover(self, winner="Jugador"):
        self.game_over = True
        self.winner = winner

    def receive_enemy_shot(self, r, c):
        """
        Usado solo en multijugador.
        El rival dispara a nuestro tablero.
        Devuelve (hit, sunk_coords)
        """
        hit = self.player_board.shoot(r, c)

        sunk_coords = None
        if hit:
            sunk_coords = self.player_board.check_sunk(r, c)

        if self.player_board.all_sunk():
            self.game_over = True
            self.winner = "Rival"

        return hit, sunk_coords

    # ---------------------------------------------------------
    #  MÉTODOS NECESARIOS PARA LA RAMA IA
    # ---------------------------------------------------------

    def player_shoot(self, r, c):
        """
        El jugador dispara al tablero enemigo.
        Devuelve: (hit, sunk_coords)
        """
        hit = self.enemy_board.shoot(r, c)

        sunk_coords = None
        if hit:
            sunk_coords = self.enemy_board.check_sunk(r, c)
            if sunk_coords:
                self.enemy_sunk_ships.append(sunk_coords)

        self.enemy_view[r][c] = HIT if hit else MISS

        if self.enemy_board.all_sunk():
            self.game_over = True
            self.winner = "Jugador"

        return hit, sunk_coords

    def ai_choose_shot(self):
        """
        IA muy simple: elige una casilla aleatoria no disparada.
        """
        while True:
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            if self.player_board.grid[r][c] in (EMPTY, SHIP):
                return r, c

    def ai_shoot(self, r, c):
        """
        La IA dispara al tablero del jugador.
        Devuelve: (hit, sunk_coords)
        """
        hit = self.player_board.shoot(r, c)

        sunk_coords = None
        if hit:
            sunk_coords = self.player_board.check_sunk(r, c)

        if self.player_board.all_sunk():
            self.game_over = True
            self.winner = "IA"

        return hit, sunk_coords