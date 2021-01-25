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

originalArgs = [
    (32, 32, 32), # color
    [x[0:2] for x in originalPoints]]

baseArgs = [
    (128, 128, 128),                # color
    [transform(originalPoints[0]),  # square points
     transform(originalPoints[1]),
     transform(originalPoints[2]),
     transform(originalPoints[3])]
    ]

pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True

while running:
    for event in pygame.event.get():
        if (event.type == QUIT or 
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            running = False
        pygame.draw.polygon(screen, *originalArgs)
        pygame.draw.polygon(screen, *baseArgs)
        pygame.display.flip()
