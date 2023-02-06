from Game import Game
import pygame

game = Game()

running = True

while running:

    for event in game.getEvents():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.step()
            else:
                game.handleInput(event)

    game.renderFrame()
    game.fpsController.tick(game.FPS)
