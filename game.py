from utils import *
from globals import *
from scene import Scene
import random
import math

class Player(Node):
    def __init__(self, x: float, y: float, width: float, height: float, color: pygame.Color = pygame.Color(0,0,0)):
        super().__init__(x, y, width, height, None, Shape.CERCLE, color)
        self.orientation: float = 0
        self.orientationStep: float = 0
        self.speed: float = 5
        body: list[Node]= []
        bodyBoneData: list[float] = [65, 70, 60, 50, 40, 30, 20, 10]
        SPACING = 20
        for i in range(0, len(bodyBoneData)):
            previous: float = width if (i==0) else bodyBoneData[i-1]
            current: float = bodyBoneData[i]
            node = Node(-SPACING, (previous-current)/2 , current, current, None, Shape.CERCLE, self.color)
            body.append(node)
        self.addChildRecursively(body)

player = Player(0, 0, 64, 64, pygame.Color(255, 10, 255))


apple = Node(0, 0, 64, 64)
apple.fillImage("assets/imgs/apple.png")

unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100, None, Shape.RECTANGLE, pygame.Color(0, 0, 0, 100))

class Game(Scene):
    def input(self):
        if gameState.sceneState == SceneState.GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    player.orientationStep = (event.key == pygame.K_RIGHT)-(event.key == pygame.K_LEFT)
                    print(player.orientation)
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.PAUSE
                if event.type == pygame.KEYUP:
                    player.orientationStep = 0

            player.orientation += player.orientationStep/10
            player.position.x += math.cos(math.radians(player.orientation))*player.speed/100
            player.position.y += math.sin(math.radians(player.orientation))*player.speed/100
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.GAME
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse.inOtherNode(unpause):
                        gameState.scene = Scenes.MENU
    def update(self):
        pass
    def draw(self, window):
        player.draw(window)
        apple.draw(window)
        if gameState.sceneState == SceneState.PAUSE:
            unpause.draw(window)

def setAppleToRandomPlace(n: Node):
    n.position.x = random.uniform(0, window.width-n.size.width)
    n.position.y = random.uniform(0, window.height- n.size.height)
