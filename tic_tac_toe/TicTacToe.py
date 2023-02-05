# TIC TAC TOE GAME TO TEST EXPERIMENT WITH NEURAL NETWORKS

import pygame
from pygame import Surface
import numpy as np
from numpy import ndarray

pygame.init()

BOARD_CLR = (0, 0, 0)
BG_CLR = (255, 255, 255)
P1_CLR = (255, 0, 0)
P2_CLR = (0, 0, 255)
FONT = pygame.font.SysFont("monospace", 100)


class TicTacToe:
    board = np.zeros((3, 3))
    player = 1
    game_over = False
    winner = None
    winStates = np.array([
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        [[0, 0], [1, 1], [2, 2]],
        [[2, 0], [1, 1], [0, 2]]
    ])

    def __init__(self, screen: Surface):
        self.screen = screen
        self.size = self.screen.get_height()
        self.grid_size = self.size // 3
        self.draw_board()

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for i in range(1, 3):
            pygame.draw.line(self.screen, BOARD_CLR, (0, i * self.grid_size),
                             (self.size, i * self.grid_size), 5)
            pygame.draw.line(self.screen, BOARD_CLR, (i * self.grid_size, 0),
                             (i * self.grid_size, self.size), 5)

    def draw_figure(self, pos: ndarray, player: int):
        pos = pos * self.grid_size
        if player == 1:
            margin = self.grid_size//7
            pygame.draw.circle(self.screen, P1_CLR, pos +
                               self.grid_size//2, self.grid_size//2 - margin, self.grid_size//20)
        else:
            margin = self.grid_size//5
            pygame.draw.line(self.screen, P2_CLR, pos + margin,
                             pos + self.grid_size - margin, self.grid_size//20)
            pygame.draw.line(self.screen, P2_CLR, pos + [margin, self.grid_size - margin], pos + [
                             self.grid_size - margin, margin], self.grid_size//20)

    def check_win(self):
        for state in self.winStates:
            if self.board[state[0][0], state[0][1]] == self.board[state[1][0], state[1][1]] == self.board[state[2][0], state[2][1]] != 0:
                self.game_over = True
                self.winner = self.board[state[0][0], state[0][1]]
                return True
        return False

    def check_draw(self):
        if 0 not in self.board:
            self.game_over = True
            self.winner = 0
            return True
        return False

    def draw_winner(self):
        if self.winner == 1:
            text = FONT.render("O wins!", 1, P1_CLR)
        elif self.winner == -1:
            text = FONT.render("X wins!", 1, P2_CLR)
        else:
            text = FONT.render("Draw!", 1, BOARD_CLR)
        self.screen.blit(text, (self.size//2 - text.get_width() //
                                2, self.size//2 - text.get_height()//2))
        pygame.display.update()

    def reset(self):
        self.board = np.zeros((3, 3))
        self.player = 1
        self.game_over = False
        self.winner = None
        self.draw_board()

    def click(self, pos):
        if self.game_over:
            return
        x = pos[0]
        y = pos[1]
        if self.board[x, y] == 0:
            self.board[x, y] = self.player
            self.draw_figure(pos, self.player)
            self.player *= -1
            self.check_win()
            self.check_draw()
