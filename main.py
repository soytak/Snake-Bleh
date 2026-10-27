import pygame
pygame.font.init()
from globals import *
from enum import Enum

from game import Game
from menu import Menu

pygame.init()

game = Game()
menu = Menu()
needGameReload = False

clock = pygame.time.Clock()
while gameState.scene != Scenes.QUIT:
    dt = clock.tick(60) / 1000
    mouse.update(dt)
    if gameState.scene == Scenes.GAME:
        if needGameReload:
            game.reset()
            needGameReload = False
        game.input()
        game.update(dt)
        window.fill((255,255,255))

        game.draw(window)
    else:
        needGameReload = True
    if gameState.scene == Scenes.MENU:
        menu.input()
        menu.update(dt)
        window.fill((255,255,255))

        menu.draw(window)

    pygame.display.flip()

pygame.quit()
quit(0)