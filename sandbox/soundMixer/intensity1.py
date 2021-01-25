from math import pi
import time

import pygame


pygame.init()
sound = pygame.mixer.Sound("footsteps.wav")
channel = sound.play(loops=-1)
volume_at_source = 0.5
sound_cutoff = 0.003

for radius in xrange(1, 100):
    intensity = volume_at_source / (float(radius) ** 2)
    if intensity < sound_cutoff:
        break
    channel.set_volume(intensity, intensity)
    time.sleep(1)
