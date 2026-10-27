import math
import time
import random
import pygame
from utils import *
from globals import *

class Corner:
    def __init__(self, x, y, x2, y2):
        self.distance = math.dist([x,y],[x2,y2])
        self.angle    = math.atan2(y2-y, x2-x)
class Saw(Node):
    def __init__(self, speed: float,radius: float, window: pygame.Surface):
        self.OutScreen= True
        self.angle = 0

        w, h = window.get_width(), window.get_height()

        spawnRadius = math.hypot(w/2 + radius, h/2 + radius)
        spawnAngle = random.uniform(0,2*math.pi)
        x = w/2 + math.cos(spawnAngle)*spawnRadius
        y = h/2 + math.sin(spawnAngle)*spawnRadius

        PADDING = 40
        targetX = random.uniform(PADDING, w-PADDING)
        targetY = random.uniform(PADDING, h-PADDING)
        self.angle = math.atan2(targetY - y, targetX - x)
        
        super().__init__(x, y, radius, radius, None, Shape.CERCLE, pygame.Color(255,0,0))
        self.speed = speed
    def update(self, dt: float):
        self.position.x += math.cos(self.angle)*self.speed*dt
        self.position.y += math.sin(self.angle)*self.speed*dt

    def isOutOfWindow(self, window):
        return ((self.position.x > window.width + self.size.width)  or (self.position.x < -self.size.width)
            or (self.position.y > window.height + self.size.height) or (self.position.y < -self.size.height)
        )


class SawManager:
    def __init__(self, difficultyFunc) -> None:
        self.saws: list[Saw] = []
        self.timerStart = self.timerEnd = time.time()
        self.timer = 0
        self.difficultyFunc = difficultyFunc
        self.resetTimer()

    def update(self, window, dt: float):
        self.updateTimer()
        if self.timer > self.difficultyFunc()[1]:
            self.resetTimer()
            self.spawnSaw(self.difficultyFunc()[0])
            self.spawnSaw(self.difficultyFunc()[0])
            self.spawnSaw(self.difficultyFunc()[0])
        for saw in self.saws.copy():
            saw.update(dt)
            if saw.isOutOfWindow(window):
                if not saw.OutScreen:
                    self.saws.remove(saw)
            else:
                saw.OutScreen= False

    def getAllSawsCollisions(self) -> list[tuple[Position, float]]:
        data = []
        for saw in self.saws:
            data.append((saw.position, saw.size.width))
        return data

    def updateTimer(self):
        self.timerEnd = time.time()
        self.timer = self.timerEnd - self.timerStart

    def resetTimer(self):
        self.timerStart = time.time()
        self.updateTimer()

    def spawnSaw(self, speed):
        self.saws.append(Saw(speed, 10, window))

    def draw(self, window):
        for saw in self.saws:
            saw.draw(window)
