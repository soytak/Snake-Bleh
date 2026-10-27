from typing import Any

from pygame import Color
from pygame.color import Color as Color

from utils import *
from globals import *
from scene import Scene
import random
import math

from saw import *

DEFAULT_SPEED = 7
FAST_SPEED = 15
class Player(IKbone):
    def __init__(self, position: Position, radius: float, parent: None | IKbone = None, color: Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(position, radius, parent, color)
        self.orientationStep: float = 0
        self.angle: float = 0
        self.speed: float = DEFAULT_SPEED
        body: list[IKbone]= []
        bodyBoneData: list[float] = [30, 35, 30, 25, 20, 15, 10, 5]
        for i in range(0, len(bodyBoneData)):
            current: float = bodyBoneData[i]
            node: IKbone = IKbone(Position(-10,0), current, None, pygame.Color(100,255,100))
            body.append(node)
        self.addChildRecursively(body)

player = Player(Position(0,0), 30, None, pygame.Color(255, 10, 255))

apple = Node(200, 200, 64, 64)
apple.setImage("assets/imgs/apple.png")

unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100, None, Shape.RECTANGLE, pygame.Color(0, 0, 0, 100), "Quit", pygame.Color(255,255,255))
score = Node(window.width/2-200/2, 20, 200, 100, None, Shape.RECTANGLE, pygame.Color(0,0,0,0), "0", pygame.Color(0,0,0))


class Game(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.points: int = 0
        self.sawManager = SawManager(lambda: (self.points/150+0.05, 5-max(self.points/10, 0.1)))
    def input(self):
        if gameState.sceneState == SceneState.GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.PAUSE
            k = pygame.key.get_pressed()
            player.orientationStep = (k[pygame.K_RIGHT])-(k[pygame.K_LEFT])
            player.speed = FAST_SPEED if k[pygame.K_UP] else DEFAULT_SPEED
            player.angle += player.orientationStep/10
            player.position.x += math.cos(math.radians(player.angle))*player.speed/70
            player.position.y += math.sin(math.radians(player.angle))*player.speed/70
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
        self.sawManager.update(window)
        if self.isSawPlayerCollision():
            gameState.sceneState = SceneState.DEATH

    def isSawPlayerCollision(self):
        for cercle in self.sawManager.getAllSawsCollisions():
            if player.bodyInCerle(cercle[0], cercle[1]):
                return True
        return False
            
    def draw(self, window):
        player.draw(window)
        apple.draw(window)
        self.sawManager.draw(window)
        score.draw(window)
        if gameState.sceneState == SceneState.PAUSE:
            unpause.draw(window)

def setNodeToRandomPlace(n: Node):
    PADDING = 50
    n.position.x = random.uniform(PADDING, window.width-n.size.width - PADDING)
    n.position.y = random.uniform(PADDING, window.height- n.size.height - PADDING)
