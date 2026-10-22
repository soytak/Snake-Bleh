from enum import Enum
import pygame
import typing


class Shape(Enum):
    RECTANGLE =1
    CERCLE    =2
    NONE      =3

class Position:
    def __init__(self, x: float, y: float):
        self.x= x
        self.y= y
    def __add__(self, other: Position):
        return Position(self.x + other.x, self.y + other.y)

class Size:
    def __init__(self, width: float, height: float):
        self.width= width
        self.height= height
    def __add__(self, other: Size):
        return Size(self.width + other.width, self.height + other.height)

class Node:
    def __init__(self, x: float, y: float, width: float, height: float,
                    surface= None, shape: Shape= Shape.NONE, color: pygame.Color = pygame.Color(0,0,0)):
        self.position = Position(x, y)
        self.size = Size(width, height)
        self.surface = surface
        self.shape = shape
        self.color = color
        self.orientation: float = 0 #here to work on
        self.childs: list[Node] = []
        self.parent: typing.Optional[Node] = None
        
    def draw(self, window: pygame.Surface):
        self.drawChildrens(window)
        if self.surface and window:
            window.blit(self.surface, (self.getGlobalPosition().x, self.getGlobalPosition().y))
        elif window and self.shape == Shape.RECTANGLE:
            pygame.draw.rect(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))
        elif window and self.shape == Shape.CERCLE:
            pygame.draw.ellipse(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))

    def drawChildrens(self, window: pygame.Surface, ox: float= 0, oy: float= 0):
        for child in self.childs:
            child.draw(window)
    def fill(self, r: int, g: int, b: int):
        self.surface = pygame.surface.Surface((self.size.width,self.size.height))
        self.surface.fill((r,g,b))
    def fillImage(self, path):
        self.surface = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.size.width, self.size.height))
    def inOtherNode(self, node: Node) -> bool:
        return node_collision(self, node)
    def addChild(self, child: Node):
        child.parent = self
        self.childs.append(child)
    def addChildRecursively(self, n: list[Node]):
        parent = self
        for node in n:
            parent.addChild(node)
            parent = node
    def printChild(self):
        for child in self.childs:
            print(self)
            child.printChild()
    def getGlobalPosition(self) -> Position:
        if self.parent: return self.parent.getGlobalPosition() + self.position
        return self.position

class IKbone(Node):
    pass

def node_collision(node: Node, node2: Node) -> bool:
    return (node.position.x <= (node2.position.x + node2.size.width) and
            (node.position.x+ node.size.width) >= node2.position.x and
            node.position.y <= (node2.position.y + node2.size.height) and
            (node.position.y+ node.size.height) >= node2.position.y
            )

class Scenes(Enum):
    GAME = 1
    MENU = 2
    QUIT = 3
class SceneState(Enum):
    GAME = 1
    UPGRADE = 2
    DEATH = 3
    PAUSE = 4