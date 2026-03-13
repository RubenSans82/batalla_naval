import sys
import pygame

from board import GRID_SIZE
from game import Game
from view import GameView, CELL_SIZE, LEFT_MARGIN, TOP_MARGIN, BOARD_SPACING, BACKGROUND

pygame.init()

WIDTH = GRID_SIZE * CELL_SIZE * 2 + BOARD_SPACING + LEFT_MARGIN * 2
HEIGHT = GRID_SIZE * CELL_SIZE + TOP_MARGIN * 2


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batalla Naval - Versión 3 (POO + módulos)")

    clock = pygame.time.Clock()
    game = Game()
    view = GameView(screen, WIDTH, HEIGHT)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.player_shot(*event.pos)

        if not game.player_turn and not game.game_over:
            pygame.time.delay(400)
            game.ai_turn()

        view.draw(game)
        pygame.display.flip()


if __name__ == "__main__":
    main()
