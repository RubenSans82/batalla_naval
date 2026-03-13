import sys
import pygame

from core.lan_game import LanGame as Game
from core.base_board import GRID_SIZE
from ui.view import GameView, CELL_SIZE, LEFT_MARGIN, TOP_MARGIN, BOARD_SPACING
from ui.manager import SoundManager
from ui.manager import ImageManager
from net.network import NetThread

pygame.init()

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("server", "client"):
        print("Uso: python main_lan.py [server|client] [ip_servidor]")
        sys.exit(1)

    role = sys.argv[1]
    server_ip = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval LAN – V5")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen, WIDTH, HEIGHT)
    sound = SoundManager()

    game.set_starting_player(role == "server")

    def on_result(r, c, hit):
        game.apply_result(r, c, hit)
        view.add_effect("hit" if hit else "miss", r, c)
        (sound.play_hit() if hit else sound.play_miss())

    def on_sunk(coords):
        game.apply_sunk(coords)
        view.add_enemy_sunk_ship(coords)
        sound.play_sunk()

    def on_gameover():
        game.apply_gameover()

    net = NetThread(game, on_result, on_sunk, on_gameover, role, server_ip)
    net.start()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.my_turn and not game.game_over:
                    coords = game.click_to_coords(*event.pos)
                    if coords:
                        r, c = coords
                        if game.local_shot_request(r, c):
                            net.send_shot(r, c)

        # --- SALIR CUANDO EL JUEGO TERMINE ---
        if game.game_over:
            running = False

        view.draw(game)
        pygame.display.flip()

    # --- CIERRE LIMPIO ---
    net.stop()        # Detener hilo de red
    net.join()        # Esperar a que termine
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()