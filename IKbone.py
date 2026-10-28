from globals import *
import pygame

class IKbone():
    RANGE = 20

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

        angle = self.getAngleRadian()
        if angle is None: return
        self.position = Position(
            self.parent.position.x + math.cos(angle) * self.RANGE,
            self.parent.position.y + math.sin(angle) * self.RANGE,
        )

    def inOther(self, node: IKbone):
        return cercleCercleCollision(self.position, self.radius, node.position, node.radius)

    def bodyInCerle(self, position: Position, radius: float):
        if(cercleCercleCollision(self.position, self.radius, position, radius)): return True
        for child in self.childs:
            if(child.bodyInCerle(position, radius)): return True
        return False

    def getAngleRadian(self) -> typing.Optional[float]:
        if not self.parent: return
        dx = self.position.x - self.parent.position.x
        dy = self.position.y - self.parent.position.y
        return math.atan2(dy, dx)

    def draw(self, window: pygame.Surface, isDebugging: bool= False):
        if isDebugging:
            for child in self.childs:
                child.draw(window, True)
            pygame.draw.circle(window, self.color, (self.position.x, self.position.y), self.radius)
            a=self.getPointAt(-90)
            if a:
                pygame.draw.circle(window, pygame.Color(100,50,50), (a.x, a.y),5)
            a=self.getPointAt(90)
            if a:
                pygame.draw.circle(window, pygame.Color(100,50,50), (a.x, a.y),5)
            return
        self.drawBody(window)

    def drawBody(self, window, isHead: bool = True):
        left = []
        right= []
        l = r = None
        if self.childs:
            r= self.childs[0].drawBody(window, False)
            if not r: return
            left = r[0]
            right= r[1]
            l=self.getPointAt(-90)
            r=self.getPointAt(90)
            if not(l and r): return
            left.append( (l.x,l.y))
            right.append((r.x,r.y))
        else:
            for i in range(-90,90,18): #180/10
                t=self.getPointAt(i)
                if not t: continue
                right.append((t.x,t.y))
            
        if not isHead:
            return (left,right)
        
        top = []
        for i in range(90,90+180,18): #180/10
            t=self.getPointAt(i)
            if not t: continue
            top.append((t.x,t.y))

        left.reverse()
        pygame.draw.polygon(window, self.color, (right+top+left))

    def getPointAt(self, angleDegree) -> typing.Optional[Position]:
        a= self.getAngleRadian()
        angle = math.radians(angleDegree)
        if a is None: return None
        return Position(self.position.x+math.cos(a+angle)*self.radius, self.position.y+math.sin(a+angle)*self.radius)

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
