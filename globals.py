from utils import *

class GameState:
    scene = Scenes.GAME
    sceneState= SceneState.GAME
gameState = GameState()

mouse = Node(0,0,0,0)

window= pygame.display.set_mode((800, 600))
window.fill((0,0,0))
pygame.display.set_caption("Snake bleh!")
