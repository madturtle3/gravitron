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


def change(points: list[Body]):
    for i in range(len(points)):
        if points[i].movable:
            ddx=0.0
            ddy=0.0
            for other_point in points:
                ddx += -other_point.mass*(points[i].x-other_point.x)/points[i].mass/360
                ddy += -other_point.mass*(points[i].y-other_point.y)/points[i].mass/360
            points[i].dx += ddx
            points[i].dy += ddy
            points[i].x += points[i].dx
            points[i].y += points[i].dy


window = pygame.display.set_mode((500, 500))
x,y = (0,0)
zoom=1.0
clock = pygame.time.Clock()
points: list[Body] = [Body(0,0,mass=5,movable=False)]
keys: set[int] = set()
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
            points.append(Body(xe*zoom-250,ye*zoom-250,(xs-xe)/10,(ys-ye)/10))
            
    if pygame.K_RIGHT in keys:
        x+=5
    if pygame.K_LEFT in keys:
        x-=5
    if pygame.K_UP in keys:
        y-=5
    if pygame.K_DOWN in keys:
        y+=5
    if pygame.K_EQUALS in keys:
        zoom*=1.25
    if pygame.K_MINUS in keys:
        zoom *=.75

    change(points)
    window.fill((255, 255, 255))
    for body in points:
        pygame.draw.circle(window, (0, 0, 0), ((body.x-x)*zoom+250, zoom*(body.y-y)+250), math.log(body.mass+1)*15)
    pygame.display.flip()
    clock.tick(60)
