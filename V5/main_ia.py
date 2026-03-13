import sys
import pygame
import random

from core.ia_game import IaGame as Game
from core.base_board import GRID_SIZE
from ui.view import GameView, CELL_SIZE, LEFT_MARGIN, TOP_MARGIN, BOARD_SPACING
from ui.manager import SoundManager
from ui.manager import ImageManager

pygame.init()

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval IA – V5")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen, WIDTH, HEIGHT)
    sound = SoundManager()

    game.set_starting_player(True)

    # Variables para retraso IA
    game.ai_pending_shot = None
    game.ai_delay = 0

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- TURNO DEL JUGADOR ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.my_turn and not game.game_over:
                    coords = game.click_to_coords(*event.pos)
                    if coords:
                        r, c = coords
                        hit, sunk = game.player_shoot(r, c)

                        view.add_effect("hit" if hit else "miss", r, c)
                        (sound.play_hit() if hit else sound.play_miss())

                        if sunk:
                            view.add_enemy_sunk_ship(sunk)
                            sound.play_sunk()

                        # --- CAMBIO DE TURNO SOLO SI AGUA ---
                        if not game.game_over:
                            if not hit:  # agua → pasa turno
                                game.my_turn = False
                                game.ai_pending_shot = None
                            # si hit o sunk → mantiene turno

        # --- TURNO DE LA IA CON RETRASO ---
        if not game.my_turn and not game.game_over:

            # Preparar disparo si no hay uno pendiente
            if game.ai_pending_shot is None:
                game.ai_pending_shot = game.ai_choose_shot()
                game.ai_delay = 1400  # ms

            game.ai_delay -= dt

            if game.ai_delay <= 0:
                r, c = game.ai_pending_shot
                hit, sunk = game.ai_shoot(r, c)

                view.add_effect("hit" if hit else "miss", r, c)
                (sound.play_hit() if hit else sound.play_miss())

                if sunk:
                    sound.play_sunk()

                game.ai_pending_shot = None

                # --- CAMBIO DE TURNO SOLO SI AGUA ---
                if not game.game_over:
                    if not hit:  # agua → pasa turno al jugador
                        game.my_turn = True
                    # si hit o sunk → IA mantiene turno

        view.draw(game)
        pygame.display.flip()


if __name__ == "__main__":
    main()