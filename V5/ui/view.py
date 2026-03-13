import pygame
from core.base_board import GRID_SIZE, EMPTY, SHIP, MISS, HIT
from ui.manager import ImageManager

CELL_SIZE = 50
LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120

BLUE = (80, 140, 220)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
BACKGROUND = (220, 220, 240)

pygame.font.init()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)


class GameView:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.enemy_sunk_ships = []
        self.effects = []
        self.last_time = pygame.time.get_ticks()
        #inicializar imagenes
        self.images = ImageManager(CELL_SIZE)

        # ---------------------------
        #   CARGAR BACKGROUND
        # ---------------------------
        try:
            bg = pygame.image.load("assets/gui/background.jpg").convert()
            self.background = pygame.transform.scale(bg, (width, height))
        except:
            self.background = None

    def add_enemy_sunk_ship(self, coords):
        self.enemy_sunk_ships.append(coords)

    def add_effect(self, effect_type, r, c, duration=300):
        self.effects.append({
            "type": effect_type,
            "r": r,
            "c": c,
            "time": duration
        })

    def draw_effects(self, dt):
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        for effect in list(self.effects):
            effect["time"] -= dt
            if effect["time"] <= 0:
                self.effects.remove(effect)
                continue

            r, c = effect["r"], effect["c"]
            x = enemy_x + c * CELL_SIZE
            y = enemy_y + r * CELL_SIZE

            if effect["type"] == "miss":
                pygame.draw.circle(self.screen, (180, 180, 255),
                                   (x + CELL_SIZE//2, y + CELL_SIZE//2), 10)

            elif effect["type"] == "hit":
                pygame.draw.rect(self.screen, (255, 80, 80),
                                 (x+5, y+5, CELL_SIZE-10, CELL_SIZE-10), 3)

            elif effect["type"] == "sunk":
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (x, y, CELL_SIZE, CELL_SIZE), 4)

    def draw_ship_frame(self, ship, x, y):
        rows = [r for r, _ in ship]
        cols = [c for _, c in ship]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        rect_x = x + min_c * CELL_SIZE
        rect_y = y + min_r * CELL_SIZE
        rect_w = (max_c - min_c + 1) * CELL_SIZE
        rect_h = (max_r - min_r + 1) * CELL_SIZE

        pygame.draw.rect(self.screen, WHITE, (rect_x, rect_y, rect_w, rect_h), 4)

    def draw_player_board(self, game):
        board = game.player_board
        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN

        pygame.draw.rect(self.screen, BLACK,
                         (player_x-5, player_y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = board.grid[r][c]
                
                # 1. Fondo de agua o barco oculto
                bg_color = BLUE
                if cell == SHIP:
                    bg_color = GRAY
                
                rect_celda = (player_x + c*CELL_SIZE, player_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, bg_color, rect_celda)
                
                # 2. Le DECIMOS al ImageManager que dibuje (Clean Code)
                x_coord = player_x + c*CELL_SIZE
                y_coord = player_y + r*CELL_SIZE

                if cell == MISS:
                    self.images.draw_miss(self.screen, x_coord, y_coord)
                elif cell == HIT:
                    self.images.draw_hit(self.screen, x_coord, y_coord)
                
                # 3. Dibujar la cuadrícula
                pygame.draw.rect(self.screen, BLACK, rect_celda, 1)

        # 4. Dibujar marcos y la imagen de "Hundido" si corresponde
        for ship in board.ships:
            esta_hundido = all(board.grid[r][c] == HIT for r, c in ship)
            if esta_hundido:
                for r, c in ship:
                    self.images.draw_sunk(self.screen, player_x + c*CELL_SIZE, player_y + r*CELL_SIZE)
                    
            self.draw_ship_frame(ship, player_x, player_y)


    def draw_enemy_board(self, game):
        enemy_view = game.enemy_view
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        pygame.draw.rect(self.screen, BLACK,
                         (enemy_x-5, enemy_y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = enemy_view[r][c]
                
                rect_celda = (enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLUE, rect_celda)
                
                x_coord = enemy_x + c*CELL_SIZE
                y_coord = enemy_y + r*CELL_SIZE

                # Usamos los nuevos métodos
                if cell == MISS:
                    self.images.draw_miss(self.screen, x_coord, y_coord)
                elif cell == HIT:
                    self.images.draw_hit(self.screen, x_coord, y_coord)

                pygame.draw.rect(self.screen, BLACK, rect_celda, 1)

        # Barcos hundidos del enemigo
        for ship in self.enemy_sunk_ships:
            for r, c in ship:
                self.images.draw_sunk(self.screen, enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE)
            
            self.draw_ship_frame(ship, enemy_x, enemy_y)

    def draw(self, game):
        now = pygame.time.get_ticks()
        dt = now - self.last_time
        self.last_time = now

        # ---------------------------
        #   DIBUJAR BACKGROUND
        # ---------------------------
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((220, 220, 240))

        # ---------------------------
        #   PANEL SEMITRANSPARENTE
        # ---------------------------
        panel = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 120))  # negro con transparencia

        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        self.screen.blit(panel, (player_x, player_y))
        self.screen.blit(panel, (enemy_x, enemy_y))

        # ---------------------------
        #   TÍTULOS
        # ---------------------------
        self.screen.blit(big_font.render("Tu tablero", True, WHITE), (player_x, player_y - 40))
        self.screen.blit(big_font.render("Tablero enemigo", True, WHITE), (enemy_x, enemy_y - 40))

        # ---------------------------
        #   TABLEROS
        # ---------------------------
        self.draw_player_board(game)
        self.draw_enemy_board(game)
        self.draw_effects(dt)

        # ---------------------------
        #   FIN DEL JUEGO
        # ---------------------------
        if game.game_over:
            msg = big_font.render(f"Fin del juego: {game.winner} gana", True, WHITE)
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, self.height - 60))