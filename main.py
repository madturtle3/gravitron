import pygame
import math
import dataclasses
pygame.init()

@dataclasses.dataclass
class Body:
    x: float
    y: float
    dx: float=0
    dy: float=0
    mass: float=1
    movable: bool=True
    def distancefrom(self,other: "Body"):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)


def change(points: list[Body]):
    newpoints: list[Body] = []
    for point in points:
        if point.movable:
            ddx=0.0
            ddy=0.0
            for other_point in points:
                distanceapart = point.distancefrom(other_point)
                if other_point != point:
                    dify,difx = (point.y-other_point.y)/distanceapart,(point.x-other_point.x)/distanceapart
                    ddy += -dify*point.mass*other_point.mass/distanceapart
                    ddx += -difx*point.mass*other_point.mass/distanceapart
            point.dx += ddx
            point.dy += ddy
            point.x += point.dx
            point.y += point.dy
        newpoints.append(point)
    return newpoints


window = pygame.display.set_mode((500, 500))
x,y = (0,0)
zoom=1.0
clock = pygame.time.Clock()
points: list[Body] = []
keys: set[int] = set()
speed = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            keys.add(event.key)
        if event.type == pygame.KEYUP:
            keys.remove(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            xs,ys=pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            xe,ye = pygame.mouse.get_pos()
            points.append(Body((xs-250)/zoom+x,(ys-250)/zoom+y,(xs-xe)/zoom/10,(ys-ye)/zoom/10,mass=1.0))
    
    if pygame.K_LEFTBRACKET in keys:
        speed *=.75
    if pygame.K_RIGHTBRACKET in keys:
        speed *=1.25
    if pygame.K_RIGHT in keys:
        x+=5/zoom
    if pygame.K_LEFT in keys:
        x-=5/zoom
    if pygame.K_UP in keys:
        y-=5/zoom
    if pygame.K_DOWN in keys:
        y+=5/zoom
    if pygame.K_EQUALS in keys:
        zoom*=1.25
    if pygame.K_MINUS in keys:
        zoom *=.75
    if pygame.K_SPACE in keys:
        points=change(points)
    window.fill((0, 0, 0))
    for body in points:
        pygame.draw.circle(window, (255, 255, 255), ((body.x-x)*zoom+250, zoom*(body.y-y)+250), math.log(body.mass+1)*zoom*10)
    pygame.display.flip()
    clock.tick(60)
