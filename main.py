import pygame
pygame.mixer.pre_init()
pygame.init()
pygame.font.init()
pygame.mixer.init()
from globals import *
from enum import Enum

from game import Game
from menu import Menu


game = Game()
menu = Menu()
needGameReload = False

pygame.mixer.music.load("assets/nintendo_esque_music_2.mp3")
pygame.mixer.music.play(-1)

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