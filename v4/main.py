import sys
import pygame

from core.board import GRID_SIZE
from core.game import Game
from ui.view import GameView, CELL_SIZE, LEFT_MARGIN, TOP_MARGIN, BOARD_SPACING, BACKGROUND
from net.network import NetThread

pygame.init()

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("server", "client"):
        print("Uso: python main.py [server|client]")
        sys.exit(1)

    role = sys.argv[1]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval - Versión 4.2 (Red + MVC)")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen, WIDTH, HEIGHT)

    game.set_starting_player(role == "server")

    # -----------------------------
    # CALLBACKS
    # -----------------------------
    def on_result(r, c, hit):
        game.apply_result(r, c, hit)

    def on_sunk(coords):
        cells = game.apply_sunk(coords)
        view.add_enemy_sunk_ship(cells)

    def on_gameover():
        game.game_over = True
        game.winner = "Jugador"

    # -----------------------------
    # Hilo de red
    # -----------------------------
    net = NetThread(game, on_result, on_sunk, on_gameover, role)
    net.start()

    # -----------------------------
    # Bucle principal
    # -----------------------------
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.my_turn and not game.game_over:
                    coords = game.click_to_coords(*event.pos)
                    if coords:
                        r, c = coords
                        if game.local_shot_request(r, c):
                            net.send_shot(r, c)

        view.draw(game)
        pygame.display.flip()


if __name__ == "__main__":
    main()