from utils import *
from globals import *
from scene import Scene

player_surface = pygame.surface.Surface((64,64))
player_surface.fill((255,10,255))
player = Player(0, 0, 64, 64, player_surface)


apple = Node(0, 0, 64, 64)
apple.fillImage("assets/imgs/apple.png")

unpause = Node(window.get_width()/2-200/2, window.get_height()/2-100/2, 200, 100)
unpause.fill()

class Game(Scene):
    def input(self):
        if gameState.sceneState == SceneState.GAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.vel.x = -0.2
                    if event.key == pygame.K_RIGHT:
                        player.vel.x = 0.2
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.PAUSE
                else:
                    player.vel.x = 0
                    player.vel.y = 0



            player.position.x += player.vel.x
            player.position.x += player.vel.y
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState.scene = Scenes.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameState.sceneState = SceneState.GAME
                if event.type == pygame.MOUSEMOTION:
                    mouse.position.x, mouse.position.y = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if node_collision(mouse, unpause):
                        gameState.scene = Scenes.MENU
    def update(self):
        pass
    def draw(self, window):
        player.draw(window)
        apple.draw(window)
        if gameState.sceneState == SceneState.PAUSE:
            unpause.draw(window)