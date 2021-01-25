import pygame
from pygame.locals  import QUIT, KEYDOWN, K_ESCAPE

from variableIsoProjection import transform as transformOrig


def transform(point, origin=[400, 400, 0], rollAngle=40, yawAngle=0,
              pitchAngle=45):
    return transformOrig(point, origin, rollAngle, yawAngle, pitchAngle)


originalPoints = [
    [200, 200, 0],
    [200, 600, 0],
    [600, 600, 0],
    [600, 200, 0]]

baseArgs = [
    (32, 32, 32),                   # color
    [transform(originalPoints[0]),  # square points
     transform(originalPoints[1]),
     transform(originalPoints[2]),
     transform(originalPoints[3])]
    ]

def makeGrid(screen):
    color = (128, 128, 128)
    for x in xrange(200, 625, 25):
        lineStart = transform([x, 200, 0])
        lineEnd = transform([x, 600, 0])
        pygame.draw.line(screen, color, lineStart, lineEnd)
    for y in xrange(200, 625, 25):
        lineStart = transform([200, y, 0])
        lineEnd = transform([600, y, 0])
        pygame.draw.line(screen, color, lineStart, lineEnd)
           
pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True

while running:
    for event in pygame.event.get():
        if (event.type == QUIT or 
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            running = False
        pygame.draw.polygon(screen, *baseArgs)
        makeGrid(screen)
        pygame.display.flip()
