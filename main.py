import pygame
from globals import *
import random
from enum import Enum

from game import Game

pygame.init()

game = Game()

while gameState.scene == Scenes.GAME:
    game.input()
    game.update()

    window.fill((255,255,255))

    game.draw(window)

    pygame.display.flip()


pygame.quit()
quit(0)