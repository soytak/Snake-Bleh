from enum import Enum
import pygame

class Position:
    def __init__(self, x, y):
        self.x= x
        self.y= y

class Size:
    def __init__(self, width, height):
        self.width= width
        self.height= height

class Node:
    def __init__(self, x, y, width, height, surface= None):
        self.position= Position(x, y)
        self.size= Size(width, height)
        self.surface= surface
        
    def draw(self, window):
        if self.surface and window:
            window.blit(self.surface, (self.position.x, self.position.y))
    def fill(self):
        self.surface = pygame.surface.Surface((self.size.width,self.size.height))
    def fillImage(self, path):
        self.surface = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.size.width, self.size.height)) 


class Player(Node):
    def __init__(self, x, y, width, height, surface=None):
        super().__init__(x, y, width, height, surface)
        self.vel= pygame.Vector2(0,0)

def node_collision(node, node2):
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
