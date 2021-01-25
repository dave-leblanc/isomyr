import pygame
from pygame.locals  import QUIT, KEYDOWN, K_ESCAPE

from variableIsoProjection import transform as transformOrig


def transform(point, origin=[400, 400, 0], rollAngle=40, yawAngle=0,
              pitchAngle=45):
    return transformOrig(point, origin, rollAngle, yawAngle, pitchAngle)


minWidth = 200
maxWidth = 600


def makeFloor(screen):
    color = (32, 32, 32)
    points = [
        transform([minWidth, minWidth, 0]),
        transform([minWidth, maxWidth, 0]),
        transform([maxWidth, maxWidth, 0]),
        transform([maxWidth, minWidth, 0])]
    pygame.draw.polygon(screen, color, points)


def makeNorthWall(screen):
    # This isn't working right now... maybe because the staring view (top-down)
    # doesn't show the vertical wall? Dunno... need to actually examine the
    # code and the math.
    color = (32, 32, 32)
    origin = [400, 0, 200]
    points = [
        transform([minWidth, 0, 0], origin=origin),
        transform([minWidth, 0, maxWidth - minWidth], origin=origin),
        transform([maxWidth, 0, maxWidth - minWidth], origin=origin),
        transform([maxWidth, 0, 0], origin=origin)]
    print points
    pygame.draw.polygon(screen, color, points)

def makeWestWall(screen):
    # This isn't working right now... maybe because the staring view (top-down)
    # doesn't show the vertical wall? Dunno... need to actually examine the
    # code and the math.
    color = (32, 32, 32)
    points = [
        transform([maxWidth, minWidth, 0]),
        transform([maxWidth, minWidth, maxWidth - minWidth]),
        transform([maxWidth, maxWidth, maxWidth - minWidth]),
        transform([maxWidth, maxWidth, 0])]
    pygame.draw.polygon(screen, color, points)

def makeFloorGrid(screen):
    color = (128, 128, 128)
    gridSpacing = 25
    for x in xrange(minWidth, maxWidth + gridSpacing, gridSpacing):
        lineStart = transform([x, minWidth, 0])
        lineEnd = transform([x, maxWidth, 0])
        pygame.draw.line(screen, color, lineStart, lineEnd)
    for y in xrange(minWidth, maxWidth + gridSpacing, gridSpacing):
        lineStart = transform([minWidth, y, 0])
        lineEnd = transform([maxWidth, y, 0])
        pygame.draw.line(screen, color, lineStart, lineEnd)
           
pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True

while running:
    for event in pygame.event.get():
        if (event.type == QUIT or 
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            running = False
        makeFloor(screen)
        makeFloorGrid(screen)
        makeNorthWall(screen)
        makeWestWall(screen)
        pygame.display.flip()
