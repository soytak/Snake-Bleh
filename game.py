from typing import Any

from pygame import Color, Surface
from pygame.color import Color as Color

from utils import *
from globals import *
from scene import Scene
import random
import math

from saw import *
from IKbone import *

DEFAULT_SPEED = 180
FAST_SPEED = 360
class Player(IKbone):
    def __init__(self, position: Position, radius: float, parent: None | IKbone = None, color: Color = pygame.Color(0, 0, 0)) -> None:
        super().__init__(position, radius, parent, color)
        self.orientationStep: float = 0
        self.angle: float = 0
        self.speed: float = DEFAULT_SPEED
        body: list[IKbone]= []
        bodyBoneData: list[float] = [30, 35, 30, 25, 24, 23, 22, 21, 20, 15, 10, 5]
        for i in range(0, len(bodyBoneData)):
            current: float = bodyBoneData[i]
            node: IKbone = IKbone(Position(-10,0), current, None, pygame.Color(100,255,100))
            body.append(node)
        self.addChildRecursively(body)

    def getAngleRadian(self) -> float | None:
        return math.radians(self.angle+180) #180 make it works, if it work it works


class Game(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
    def reset(self):
        self.points: int = 0
        self.sawManager = SawManager(lambda: (self.points+100, 5-max(self.points/8, 0.5)))
        self.bg = Node(0,0, window.width, window.height)
        self.bg.setImage("assets/imgs/grass.png")
        self.player = Player(Position(200,200), 30, None, pygame.Color(70, 200, 70))

        self.apple = Node(200, 200, 64, 64)
        self.apple.setImage("assets/imgs/apple.png")

        self.unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100, None, Shape.RECTANGLE, pygame.Color(0, 0, 0, 100), "Quit", pygame.Color(255,255,255))
        self.score = Node(window.width/2-200/2, 20, 200, 100, None, Shape.RECTANGLE, pygame.Color(0,0,0,0), "0", pygame.Color(255,255,255))

        self.deathBox = Node( window.get_width()/2-400/2, window.get_height()/2-250/2 ,400,250, None, Shape.RECTANGLE, pygame.Color(0,0,0,100))
        self.goToTitle= Node( window.get_width()/2-200/2, window.get_height()/2 ,200,100, None, Shape.RECTANGLE, pygame.Color(0,0,0), "Go to menu", pygame.Color(255,255,255))
        self.ScoreText= Node( window.get_width()/2-100/2, window.get_height()/2-100 ,100,100, None, Shape.RECTANGLE, pygame.Color(0,0,0,0), "", pygame.Color(255,255,255))

    def input(self):
        if gameState.sceneState == SceneState.GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.PAUSE
        elif gameState.sceneState == SceneState.DEATH:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse.inOtherNode(self.goToTitle):
                        gameState.scene = Scenes.MENU
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.GAME
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse.inOtherNode(self.unpause):
                        gameState.scene = Scenes.MENU
    def update(self, dt: float):
        self.sawManager.update(window, dt)
        if gameState.sceneState != SceneState.GAME: return
        k = pygame.key.get_pressed()
        self.player.orientationStep = (k[pygame.K_RIGHT])-(k[pygame.K_LEFT])
        self.player.speed = FAST_SPEED if k[pygame.K_UP] else DEFAULT_SPEED
        self.player.angle += self.player.orientationStep*180*dt
        self.player.position.x += math.cos(math.radians(self.player.angle))*self.player.speed*dt
        self.player.position.y += math.sin(math.radians(self.player.angle))*self.player.speed*dt
        self.player.update()
        if(self.player.bodyInCerle(self.apple.getCenterPosition(), 5)):
            setNodeToRandomPlace(self.apple)
            self.points+=1
            self.score.setText(str(self.points))
            
        if self.isSawPlayerCollision() or self.isOutOfBound():
            gameState.sceneState = SceneState.DEATH
            self.ScoreText.setText("Score: "+ str(self.points))

    def isSawPlayerCollision(self):
        for cercle in self.sawManager.getAllSawsCollisions():
            if self.player.bodyInCerle(cercle[0], cercle[1]):
                return True
        return False

    def isOutOfBound(self):
        return not rect_collision(self.player.position, Size(self.player.radius, self.player.radius), Position(0,0), Size(window.width, window.height))

    def draw(self, window):
        self.bg.draw(window)
        if gameState.sceneState != SceneState.DEATH: self.player.draw(window, False)
        self.apple.draw(window)
        self.sawManager.draw(window)
        if gameState.sceneState != SceneState.DEATH: self.score.draw(window)
        if gameState.sceneState == SceneState.PAUSE:
            self.unpause.draw(window)
        if gameState.sceneState == SceneState.DEATH:
                    self.deathBox.draw(window)
                    self.goToTitle.draw(window)
                    self.ScoreText.draw(window)

def setNodeToRandomPlace(n: Node):
    PADDING = 50
    n.position.x = random.uniform(PADDING, window.width-n.size.width - PADDING)
    n.position.y = random.uniform(PADDING, window.height- n.size.height - PADDING)
