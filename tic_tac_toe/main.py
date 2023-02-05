from TicTacToe import TicTacToe
import pygame
import numpy as np


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tic Tac Toe")
    game = TicTacToe(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over:
                    pos = np.array(pygame.mouse.get_pos()) // game.grid_size
                    game.click(pos)

                if game.game_over:
                    game.draw_winner()
                    pygame.time.delay(1000)
                    game.reset()

        pygame.display.update()


if __name__ == "__main__":
    main()
