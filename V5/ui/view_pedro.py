import pygame
from core.board import GRID_SIZE, EMPTY, SHIP, MISS, HIT

# Configuración de dimensiones
CELL_SIZE = 50
LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120

# Colores
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
        
        # CARGA DE TEXTURA
        try:
            # Cargamos la imagen y optimizamos para Pygame con transparencia
            self.carrier_texture = pygame.image.load(r"C:\practicas\Python\Ingenieria de software\batalla_naval\V4_LAN\assets\images\Portaviones.png").convert_alpha()
            self.acorazado_texture = pygame.image.load(r"C:\practicas\Python\Ingenieria de software\batalla_naval\V4_LAN\assets\images\Acorazado.png").convert_alpha()            
            self.destructor_texture = pygame.image.load(r"C:\practicas\Python\Ingenieria de software\batalla_naval\V4_LAN\assets\images\Destructor.png").convert_alpha()            
            self.crucero_texture = pygame.image.load(r"C:\practicas\Python\Ingenieria de software\batalla_naval\V4_LAN\assets\images\Crucero.png").convert_alpha()            
            self.submarino_texture = pygame.image.load(r"C:\practicas\Python\Ingenieria de software\batalla_naval\V4_LAN\assets\images\Submarino.png").convert_alpha()                        
        except Exception as e:
            print(f"No se pudo cargar la textura: {e}")
            self.carrier_texture = None

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

    def draw_ship_visuals(self, ship, x, y):
        """Calcula el área del barco y decide si dibuja textura o marco"""
        rows = [r for r, _ in ship]
        cols = [c for _, c in ship]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        rect_x = x + min_c * CELL_SIZE
        rect_y = y + min_r * CELL_SIZE
        rect_w = (max_c - min_c + 1) * CELL_SIZE
        rect_h = (max_r - min_r + 1) * CELL_SIZE

        # MODIFICACIÓN: Aplicar textura si es el portaaviones (longitud 5)
        if len(ship) == 5 and self.carrier_texture:
            # Escalamos la imagen para que ocupe exactamente las casillas del barco
            scaled_ship = pygame.transform.scale(self.carrier_texture, (rect_w, rect_h))
            self.screen.blit(scaled_ship, (rect_x, rect_y))
        elif len(ship) == 4 and self.acorazado_texture:
            scaled_ship = pygame.transform.scale(self.acorazado_texture, (rect_w, rect_h))
            self.screen.blit(scaled_ship, (rect_x, rect_y))
        elif len(ship) == 3 and self.destructor_texture:
            scaled_ship = pygame.transform.scale(self.destructor_texture, (rect_w, rect_h))
            self.screen.blit(scaled_ship, (rect_x, rect_y))
        elif len(ship) == 2 and self.crucero_texture:
            scaled_ship = pygame.transform.scale(self.crucero_texture, (rect_w, rect_h))
            self.screen.blit(scaled_ship, (rect_x, rect_y))
        elif len(ship) == 1 and self.submarino_texture:
            scaled_ship = pygame.transform.scale(self.submarino_texture, (rect_w, rect_h))
            self.screen.blit(scaled_ship, (rect_x, rect_y))
        else:
            # Marco blanco para el resto de barcos
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
                color = BLUE
                if cell == MISS: color = WHITE
                elif cell == HIT: color = RED
                elif cell == SHIP: color = GRAY

                pygame.draw.rect(self.screen, color,
                                 (player_x + c*CELL_SIZE, player_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK,
                                 (player_x + c*CELL_SIZE, player_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for ship in board.ships:
            self.draw_ship_visuals(ship, player_x, player_y)

    def draw_enemy_board(self, game):
        enemy_view = game.enemy_view
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        pygame.draw.rect(self.screen, BLACK,
                         (enemy_x-5, enemy_y-5, GRID_SIZE*CELL_SIZE+10, GRID_SIZE*CELL_SIZE+10), 3)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = enemy_view[r][c]
                color = BLUE
                if cell == MISS: color = WHITE
                elif cell == HIT: color = RED

                pygame.draw.rect(self.screen, color,
                                 (enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK,
                                 (enemy_x + c*CELL_SIZE, enemy_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for ship in self.enemy_sunk_ships:
            self.draw_ship_visuals(ship, enemy_x, enemy_y)

    def draw(self, game):
        now = pygame.time.get_ticks()
        dt = now - self.last_time
        self.last_time = now

        self.screen.fill(BACKGROUND)

        player_x = LEFT_MARGIN
        player_y = TOP_MARGIN
        enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
        enemy_y = TOP_MARGIN

        self.screen.blit(big_font.render("Tu tablero", True, BLACK), (player_x, player_y - 40))
        self.screen.blit(big_font.render("Tablero enemigo", True, BLACK), (enemy_x, enemy_y - 40))

        self.draw_player_board(game)
        self.draw_enemy_board(game)
        self.draw_effects(dt)

        if game.game_over:
            msg = big_font.render(f"Fin del juego: {game.winner} gana", True, BLACK)
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, self.height - 60))
