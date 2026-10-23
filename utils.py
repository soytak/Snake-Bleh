from enum import Enum
import pygame
import typing
import math


class Shape(Enum):
    SURFACE   =0
    RECTANGLE =1
    CERCLE    =2
    NONE      =3

class Position:
    def __init__(self, x: float, y: float):
        self.x= x
        self.y= y
    def __add__(self, other: Position):
        return Position(self.x + other.x, self.y + other.y)
    def moveWithForce(self, force: float,orientation: float):
        self.x += math.cos(math.radians(orientation)) * force
        self.y += math.sin(math.radians(orientation)) * force

def movePositionWithForce(position: Position, force: float,orientation: float):
    position = Position(position.x + math.cos(math.radians(orientation)) * force, position.y + math.sin(math.radians(orientation)) * force)
    return position

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
        self.surface: typing.Optional[pygame.Surface] = surface
        self.shape = shape if self.surface == None else Shape.SURFACE
        self.color = color
        match shape:
            case Shape.RECTANGLE:
                self.setRect()
            case Shape.CERCLE:
                self.setEllipse()
            case Shape.NONE:
                pass
        self.orientation: float = 0 #here to work on
        self.childs: list[Node] = []
        self.parent: typing.Optional[Node] = None
        
    def draw(self, window: pygame.Surface):
        self.drawChildrens(window)
        if not self.surface: return
        if self.surface and window:
            window.blit(self.surface, (self.getGlobalPosition().x, self.getGlobalPosition().y))
        elif window and self.shape == Shape.RECTANGLE:
            pygame.draw.rect(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))
        elif window and self.shape == Shape.CERCLE:
            pygame.draw.ellipse(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))

    def drawChildrens(self, window: pygame.Surface):
        for child in self.childs:
            child.draw(window)
    def setRect(self):
        self.shape = Shape.RECTANGLE
        self.surface = pygame.surface.Surface((self.size.width,self.size.height))
        self.surface.fill(self.color)
    def setEllipse(self):
        self.shape = Shape.CERCLE
        self.surface = pygame.surface.Surface((self.size.width,self.size.height), pygame.SRCALPHA)
        pygame.draw.ellipse(self.surface, self.color, (0,0,self.size.width,self.size.height))

    def setImage(self, path):
        self.shape = Shape.SURFACE
        self.surface = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.size.width, self.size.height))

    def inOtherNode(self, node: Node) -> bool:
        return rect_collision(self.getGlobalPosition(), self.size, node.getGlobalPosition(), node.size)

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
        if self.parent: return self.parent.getGlobalPosition() + self.getLocalPosition()#movePositionWithForce(self.getLocalPosition(), 1, self.parent.getGlobalOrientation())
        return self.getLocalPosition()
    def getLocalPosition(self):
        return Position(self.position.x, self.position.y)
    def getGlobalOrientation(self) -> float:
        if self.parent: return self.parent.getGlobalOrientation() + self.orientation
        return self.orientation

class IKbone(Node):
    pass

def rect_collision(position: Position, size: Size, position2: Position, size2: Size) -> bool:
    return (position.x <= (position2.x + size2.width) and
            (position.x+ size.width) >= position2.x and
            position.y <= (position2.y + size2.height) and
            (position.y+ size.height) >= position2.y
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