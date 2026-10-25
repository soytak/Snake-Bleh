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
        self.lock: bool = False

    def lockGraphicRotation(self) -> Node:
        self.lock = True
        return self
    def unlockGraphicRotation(self) -> Node:
        self.lock = False
        return self

    def update(self):
        pass

    def draw(self, window: pygame.Surface):
        self.drawChildrens(window)
        if not self.surface: return
        rotatedSurface = pygame.transform.rotate(self.surface, self.getGlobalOrientation()) if not self.lock else self.surface
        if self.surface and window:
            window.blit(rotatedSurface, (self.getGlobalPosition().x, self.getGlobalPosition().y))
        elif window and self.shape == Shape.RECTANGLE:
            window.blit(rotatedSurface, (self.getGlobalPosition().x, self.getGlobalPosition().y))
            #pygame.draw.rect(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))
        elif window and self.shape == Shape.CERCLE:
            window.blit(rotatedSurface, (self.getGlobalPosition().x, self.getGlobalPosition().y))
            #pygame.draw.ellipse(window, self.color, (self.getGlobalPosition().x, self.getGlobalPosition().y, self.size.width, self.size.height))

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

class IKbone():
    RANGE = 50

    def __init__(self, position: Position, radius: float, parent: None | IKbone = None, color: pygame.Color = pygame.Color(0,0,0)) -> None:
        self.radius = radius
        self.color = color
        self.childs: list[IKbone] = []
        self.position: Position = position
        """Cashed centered position"""
        self.parent= parent
        if parent: self.addParent(parent)

    def update(self):
        self.updateSelfPosition()
        for child in self.childs:
            child.update()

    def updateSelfPosition(self):
        if not self.parent: return
        # revert global to local position
        dx = self.position.x - self.parent.position.x
        dy = self.position.y - self.parent.position.y
        angle = math.atan2(dy, dx)
        self.position = Position(
            self.parent.position.x + math.cos(angle) * self.RANGE,
            self.parent.position.y + math.sin(angle) * self.RANGE,
        )

    def getAngleRadian(self) -> float:
        return math.atan2(self.position.y, self.position.x)

    def draw(self, window: pygame.Surface):
        for child in self.childs:
            child.draw(window)
        pygame.draw.circle(window, self.color, (self.position.x, self.position.y), self.radius)

    def addChild(self, child: IKbone):
        child.parent = self
        self.childs.append(child)
    def addParent(self, parent: IKbone):
        parent.addChild(self)

    def addChildRecursively(self, n: list[IKbone]):
        parent = self
        for node in n:
            parent.addChild(node)
            parent = node


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