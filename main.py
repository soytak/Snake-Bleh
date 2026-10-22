import pygame
from globals import *
from enum import Enum

from game import Game
from menu import Menu

pygame.init()

game = Game()
menu = Menu()

while gameState.scene != Scenes.QUIT:
    mouse.update()
    if gameState.scene == Scenes.GAME:
        game.input()
        game.update()
        window.fill((255,255,255))

        game.draw(window)
    if gameState.scene == Scenes.MENU:
        menu.input()
        menu.update()
        window.fill((255,255,255))

        menu.draw(window)

    pygame.display.flip()

pygame.quit()
quit(0)