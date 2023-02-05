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
    board: ndarray = np.zeros((3, 3))
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

    winBoards = np.zeros((len(winStates), 3, 3))

    for i, state in enumerate(winStates):
        for j, k in state:
            winBoards[i, j, k] = 1

    print(winBoards)

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

    def check_win(self) -> bool:
        for first, second, third in self.winStates:
            if self.board[first[0], first[1]] == \
                    self.board[second[0], second[1]] == \
                    self.board[third[0], third[1]] != 0:
                return True

        return False

        # for board in self.winBoards:
        #     if abs((board * self.board).sum()) == 3:
        #         return True
        # return False

    def check_draw(self) -> bool:
        if 0 not in self.board:
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

        if self.board[pos[0], pos[1]] == 0:

            self.board[pos[0], pos[1]] = self.player
            self.draw_figure(pos, self.player)

            if self.check_win():
                self.game_over = True
                self.winner = self.player

            if self.check_draw():
                self.winner = 0
                self.game_over = True

            self.player *= -1

            if self.game_over:
                self.draw_winner()
                pygame.time.delay(1000)
                self.reset()

    def minimax(self, maximizing=True, depth=10) -> tuple[int, int]:

        if depth == 0:
            return 0

        empty_spaces = []

        for i, row in enumerate(self.board):
            for j, column in enumerate(row):
                if column == 0:
                    empty_spaces.append([i, j])

        buffer = -np.inf if maximizing else np.inf
        return_i = -1

        for i, j in empty_spaces:
            self.board[i, j] = self.player

            if self.check_draw():
                score = 0

            elif self.check_win():
                score = 100 if maximizing else -100

            else:
                self.player *= -1
                score, _ = self.minimax(not maximizing, depth-1)
                score /= depth
                self.player *= -1

            if score > buffer if maximizing else score < buffer:
                buffer = score
                return_i = i + j * 3

            self.board[i, j] = 0

        return (buffer, return_i)
