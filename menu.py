from utils import *
from globals import *
from scene import Scene

bg: Node = Node(0, 0, window.get_width(), window.get_height(), None, Shape.RECTANGLE, pygame.Color(100, 100, 255))
title: Node= Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100, None, Shape.RECTANGLE, pygame.Color(0,0,0,0), "Snek bleh") 
quit: Node = Node(window.get_width()/2-200/2, window.get_height()/2-100/2+ 200, 200, 100, None, Shape.RECTANGLE, pygame.Color(100, 30, 30), "Quit")
play: Node = Node(window.get_width()/2-200/2, window.get_height()/2-100/2- 200, 200, 100, None, Shape.RECTANGLE, pygame.Color(100, 100, 100), "Play")

class Menu(Scene):
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState.scene = Scenes.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.inOtherNode(quit):
                    gameState.scene = Scenes.QUIT
                if mouse.inOtherNode(play):
                    gameState.scene = Scenes.GAME
                    gameState.sceneState = SceneState.GAME
    def update(self, dt: float):
        pass
    def draw(self, window):
        bg.draw(window)
        quit.draw(window)
        play.draw(window)
        title.draw(window)