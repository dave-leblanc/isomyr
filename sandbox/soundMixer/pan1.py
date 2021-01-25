import time
from math import sin, radians

import pygame


pygame.init()
sound = pygame.mixer.Sound("forest1.wav")

channel = sound.play()
for degree in xrange(0, 90):
    left_volume = sin(radians(degree))
    right_volume = 1 - left_volume
    channel.set_volume(left_volume, right_volume)
    time.sleep(0.03)
