import pygame
TEXTFONT = pygame.font.SysFont(pygame.font.get_default_font(), 30)
from utils import *

class GameState:
    scene = Scenes.MENU
    sceneState= SceneState.GAME
gameState = GameState()


class Mouse(Node):
    def update(self, dt: float):
        mouse.position.x = pygame.mouse.get_pos()[0]
        mouse.position.y = pygame.mouse.get_pos()[1]

mouse = Mouse(0,0,0,0)

window= pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
window.fill((0,0,0))
pygame.display.set_caption("Snake bleh!")
