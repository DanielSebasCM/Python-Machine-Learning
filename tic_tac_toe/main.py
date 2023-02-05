from TicTacToe import TicTacToe
import pygame
import numpy as np


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tic Tac Toe")
    game = TicTacToe(screen)
    playBot = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over:
                    pos = np.array(pygame.mouse.get_pos()) // game.grid_size
                    game.click(pos)
                    pygame.display.update()

                if playBot and game.player == -1:
                    _, botPlay = game.minimax()
                    game.click(np.array([botPlay % 3, botPlay//3]))
                    pygame.display.update()

        pygame.display.update()


if __name__ == "__main__":
    main()
