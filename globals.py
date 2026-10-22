from utils import *

class GameState:
    scene = Scenes.GAME
    sceneState= SceneState.GAME
gameState = GameState()


class Mouse(Node):
    def update(self):
        mouse.position.x = pygame.mouse.get_pos()[0]
        mouse.position.y = pygame.mouse.get_pos()[1]


mouse = Mouse(0,0,0,0)

window= pygame.display.set_mode((800, 600))
window.fill((0,0,0))
pygame.display.set_caption("Snake bleh!")
