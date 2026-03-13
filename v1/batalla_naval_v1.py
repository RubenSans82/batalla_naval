import pygame
import random
import sys

pygame.init()

# ---------------------------
# CONSTANTES (OK como globales)
# ---------------------------

GRID_SIZE = 8
CELL_SIZE = 50

LEFT_MARGIN = 60
TOP_MARGIN = 80
BOARD_SPACING = 120

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2

BLUE = (80, 140, 220)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
BACKGROUND = (220, 220, 240)

EMPTY = 0
SHIP = 1
MISS = 2
HIT = 3

FLEET = [4, 3, 2, 2, 1, 1]

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)


# ---------------------------
# FUNCIONES DE MODELO
# ---------------------------

def create_board():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]


def place_fleet(board):
    ships = []
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
                        if board[r][c + i] != EMPTY:
                            ok = False
                            break
                        cells.append((r, c + i))
            else:
                if r + size > GRID_SIZE:
                    ok = False
                else:
                    for i in range(size):
                        if board[r + i][c] != EMPTY:
                            ok = False
                            break
                        cells.append((r + i, c))

            if ok:
                for rr, cc in cells:
                    board[rr][cc] = SHIP
                ships.append(cells)
                placed = True
    return ships


def get_ship_rectangles(ships, offset_x, offset_y):
    rects = []
    for ship in ships:
        rows = [r for r, _ in ship]
        cols = [c for _, c in ship]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        x = offset_x + min_c * CELL_SIZE
        y = offset_y + min_r * CELL_SIZE
        w = (max_c - min_c + 1) * CELL_SIZE
        h = (max_r - min_r + 1) * CELL_SIZE

        rects.append((ship, pygame.Rect(x, y, w, h)))
    return rects


def all_ships_sunk(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == SHIP:
                return False
    return True


# ---------------------------
# FUNCIONES DE LÓGICA DE JUEGO
# ---------------------------

def init_game_state():
    player_board = create_board()
    enemy_board = create_board()
    enemy_view = create_board()

    player_ships = place_fleet(player_board)
    enemy_ships = place_fleet(enemy_board)

    state = {
        "player_board": player_board,
        "enemy_board": enemy_board,
        "enemy_view": enemy_view,
        "player_ships": player_ships,
        "enemy_ships": enemy_ships,
        "player_turn": True,
        "game_over": False,
        "winner": None,
    }
    return state


def handle_player_shot(state, mx, my):
    if not state["player_turn"] or state["game_over"]:
        return

    enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
    enemy_y = TOP_MARGIN

    if mx <= enemy_x or my <= enemy_y:
        return

    c = (mx - enemy_x) // CELL_SIZE
    r = (my - enemy_y) // CELL_SIZE

    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
        return

    enemy_board = state["enemy_board"]
    enemy_view = state["enemy_view"]

    if enemy_view[r][c] != EMPTY:
        return

    if enemy_board[r][c] == SHIP:
        enemy_board[r][c] = HIT
        enemy_view[r][c] = HIT

        if all_ships_sunk(enemy_board):
            state["game_over"] = True
            state["winner"] = "Jugador"
    else:
        enemy_view[r][c] = MISS
        state["player_turn"] = False


def handle_ai_turn(state):
    if state["player_turn"] or state["game_over"]:
        return

    player_board = state["player_board"]

    while True:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        if player_board[r][c] in (EMPTY, SHIP):
            break

    if player_board[r][c] == SHIP:
        player_board[r][c] = HIT
        if all_ships_sunk(player_board):
            state["game_over"] = True
            state["winner"] = "IA"
    else:
        player_board[r][c] = MISS
        state["player_turn"] = True


# ---------------------------
# FUNCIONES DE DIBUJO
# ---------------------------

def draw_player_board(screen, state):
    player_board = state["player_board"]
    player_ships = state["player_ships"]

    player_x = LEFT_MARGIN
    player_y = TOP_MARGIN

    pygame.draw.rect(
        screen, BLACK,
        (player_x - 5, player_y - 5, GRID_SIZE * CELL_SIZE + 10, GRID_SIZE * CELL_SIZE + 10),
        3
    )

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = player_board[r][c]
            color = BLUE
            if cell == MISS:
                color = WHITE
            elif cell == HIT:
                color = RED
            elif cell == SHIP:
                color = GRAY

            pygame.draw.rect(
                screen, color,
                (player_x + c * CELL_SIZE, player_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen, BLACK,
                (player_x + c * CELL_SIZE, player_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

    for cells, rect in get_ship_rectangles(player_ships, player_x, player_y):
        pygame.draw.rect(screen, WHITE, rect, 4)


def draw_enemy_board(screen, state):
    enemy_view = state["enemy_view"]
    enemy_ships = state["enemy_ships"]

    enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
    enemy_y = TOP_MARGIN

    pygame.draw.rect(
        screen, BLACK,
        (enemy_x - 5, enemy_y - 5, GRID_SIZE * CELL_SIZE + 10, GRID_SIZE * CELL_SIZE + 10),
        3
    )

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = enemy_view[r][c]
            color = BLUE
            if cell == MISS:
                color = WHITE
            elif cell == HIT:
                color = RED

            pygame.draw.rect(
                screen, color,
                (enemy_x + c * CELL_SIZE, enemy_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen, BLACK,
                (enemy_x + c * CELL_SIZE, enemy_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

    for cells, rect in get_ship_rectangles(enemy_ships, enemy_x, enemy_y):
        if all(enemy_view[r][c] == HIT for r, c in cells):
            pygame.draw.rect(screen, WHITE, rect, 4)


def draw_screen(screen, state):
    screen.fill(BACKGROUND)

    player_x = LEFT_MARGIN
    player_y = TOP_MARGIN
    enemy_x = LEFT_MARGIN + GRID_SIZE * CELL_SIZE + BOARD_SPACING
    enemy_y = TOP_MARGIN

    screen.blit(big_font.render("Tu tablero", True, BLACK), (player_x, player_y - 40))
    screen.blit(big_font.render("Tablero enemigo", True, BLACK), (enemy_x, enemy_y - 40))

    draw_player_board(screen, state)
    draw_enemy_board(screen, state)

    if state["game_over"]:
        msg = big_font.render(f"Fin del juego: {state['winner']} gana", True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 60))


# ---------------------------
# BUCLE PRINCIPAL
# ---------------------------

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval - Versión 1 (Modular)")

    clock = pygame.time.Clock()
    state = init_game_state()

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_player_shot(state, *event.pos)

        if not state["player_turn"] and not state["game_over"]:
            pygame.time.delay(400)
            handle_ai_turn(state)

        draw_screen(screen, state)
        pygame.display.flip()


if __name__ == "__main__":
    main()
