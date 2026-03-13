import sys
import pygame
import random

from core.board import GRID_SIZE
from core.game import Game
from ui.view import GameView, CELL_SIZE, LEFT_MARGIN, TOP_MARGIN, BOARD_SPACING, BACKGROUND
from ui.sound_manager import SoundManager

pygame.init()

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval IA – Versión 5 (Efectos visuales + sonido)")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen, WIDTH, HEIGHT)
    sound = SoundManager()

    # IA empieza o no (puedes cambiarlo)
    game.set_starting_player(True)

    # --- BUCLE PRINCIPAL ---
    while True:
        clock.tick(60)

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
                        hit, sunk_coords = game.player_shoot(r, c)

                        # Efectos visuales + sonido
                        if hit:
                            view.add_effect("hit", r, c)
                            sound.play_hit()
                        else:
                            view.add_effect("miss", r, c)
                            sound.play_miss()

                        # Hundimiento
                        if sunk_coords:
                            view.add_enemy_sunk_ship(sunk_coords)
                            sound.play_sunk()
                            for (rr, cc) in sunk_coords:
                                view.add_effect("sunk", rr, cc, duration=600)

                        # ¿Fin del juego?
                        if game.game_over:
                            break

                        # Turno de la IA
                        game.my_turn = False

        # --- TURNO DE LA IA ---
        if not game.my_turn and not game.game_over:
            pygame.time.delay(400)  # pequeña pausa para dramatismo

            r, c = game.ai_choose_shot()
            hit, sunk_coords = game.ai_shoot(r, c)

            # Efectos visuales + sonido
            if hit:
                view.add_effect("hit", r, c)
                sound.play_hit()
            else:
                view.add_effect("miss", r, c)
                sound.play_miss()

            # Hundimiento
            if sunk_coords:
                sound.play_sunk()
                for (rr, cc) in sunk_coords:
                    view.add_effect("sunk", rr, cc, duration=600)

            # ¿Fin del juego?
            if not game.game_over:
                game.my_turn = True

        # --- DIBUJAR ---
        view.draw(game)
        pygame.display.flip()


if __name__ == "__main__":
    main()