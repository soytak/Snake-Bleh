from typing import Any

from pygame import Color
from pygame.color import Color as Color

from utils import *
from globals import *
from scene import Scene
import random
import math

from utils import IKbone

class Player(IKbone):
    def __init__(self, position: Position, radius: float, parent: None | IKbone = None, color: Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(position, radius, parent, color)
        self.orientationStep: float = 0
        self.angle: float = 0
        self.speed: float = 5
        body: list[IKbone]= []
        bodyBoneData: list[float] = [65, 70, 60, 50, 40, 30, 20, 10]
        for i in range(0, len(bodyBoneData)):
            current: float = bodyBoneData[i]
            node: IKbone = IKbone(Position(-10,0), current, None, pygame.Color(100,255,100))
            body.append(node)
        self.addChildRecursively(body)

player = Player(Position(0,0), 60, None, pygame.Color(255, 10, 255))

apple = Node(0, 0, 64, 64)
apple.setImage("assets/imgs/apple.png")

unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100, None, Shape.RECTANGLE, pygame.Color(0, 0, 0, 100), "Quit", pygame.Color(255,255,255))
score = Node(window.width/2-200/2, 20, 200, 100, None, Shape.RECTANGLE, pygame.Color(0,0,0,0), "0", pygame.Color(0,0,0))

class Game(Scene):
    points: int = 0
    def input(self):
        if gameState.sceneState == SceneState.GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    player.orientationStep = (event.key == pygame.K_RIGHT)-(event.key == pygame.K_LEFT)
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.PAUSE
                if event.type == pygame.KEYUP:
                    player.orientationStep = 0

            player.angle += player.orientationStep/10
            player.position.x += math.cos(math.radians(player.angle))*player.speed/100
            player.position.y += math.sin(math.radians(player.angle))*player.speed/100
            player.update()
            if(player.bodyInCerle(apple.getCenterPosition(), 5)):
                setNodeToRandomPlace(apple)
                self.points+=1
                score.setText(str(self.points))
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
        score.draw(window)
        if gameState.sceneState == SceneState.PAUSE:
            unpause.draw(window)

def setNodeToRandomPlace(n: Node):
    n.position.x = random.uniform(0, window.width-n.size.width)
    n.position.y = random.uniform(0, window.height- n.size.height)
