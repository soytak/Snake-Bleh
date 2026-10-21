import pygame
import random
from enum import Enum

pygame.init()

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

class Player(Node):
    def __init__(self, x, y, width, height, surface=None):
        super().__init__(x, y, width, height, surface)
        self.velocity= pygame.Vector2(0,0)

def node_collision(node, node2):
    return (node.position.x <= (node2.position.x + node2.size.width) and
            (node.position.x+ node.size.width) >= node2.position.x and
            node.position.y <= (node2.position.y + node2.size.height) and
            (node.position.y+ node.size.height) >= node2.position.y
            )

class Scene(Enum):
    GAME = 1
    MENU = 2
    QUIT = 3
class SceneState(Enum):
    GAME = 1
    UPGRADE = 2
    DEATH = 3
    PAUSE = 4

window= pygame.display.set_mode((800, 600))
window.fill((0,0,0))
pygame.display.set_caption("Snake bleh!")

scene = Scene.GAME
sceneState= SceneState.GAME

mouse = Node(0,0,0,0)


player_x = 0
player_y = 0
player_vel_x = 0
player_vel_y = 0
player = pygame.surface.Surface((64,64))
player.fill((255,10,255))

# player = Player(0, 0, 64, 64)
# player.fill()

apple_node = Node(0,0,64,64)
apple = pygame.surface.Surface((apple_node.size.width,apple_node.size.height))
apple.fill((255,100,100))
apple = pygame.image.load("assets/imgs/apple.png").convert_alpha()
apple = pygame.transform.scale(apple, (apple_node.size.width,apple_node.size.height))

unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100)
unpause.fill()

while scene == Scene.GAME:
    if sceneState == SceneState.GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene = Scene.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_vel_x = -0.2
                if event.key == pygame.K_RIGHT:
                    player_vel_x = 0.2
                if event.key == pygame.K_ESCAPE:
                    sceneState = SceneState.PAUSE
            else:
                player_vel_x = 0
                player_vel_y = 0



        player_x += player_vel_x
        player_y += player_vel_y
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene = Scene.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sceneState = SceneState.GAME
            if event.type == pygame.MOUSEMOTION:
                mouse.position.x, mouse.position.y = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if node_collision(mouse, unpause):
                    scene = Scene.MENU



    window.fill((255,255,255))

    window.blit(player, (player_x,player_y))
    window.blit(apple, (apple_node.position.x,apple_node.position.y))

    if sceneState == SceneState.PAUSE:
        unpause.draw(window)

    pygame.display.flip()


pygame.quit()
quit(0)