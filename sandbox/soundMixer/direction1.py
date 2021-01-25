import time

import pygame


pygame.init()
sound = pygame.mixer.Sound("stream2.wav")

channel = sound.play(loops=-1)
channel.set_volume(.2,.2)
time.sleep(3)

channel.set_volume(.8,.8)
time.sleep(3)
