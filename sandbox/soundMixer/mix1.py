import time

import pygame


pygame.init()
sound = pygame.mixer.Sound("forest1.wav")

channel = sound.play()
# set the volume of the channel
# so the sound is only heard to the left
channel.set_volume(1, 0)
time.sleep(2)
channel.set_volume(0, 0)

channel = sound.play()
channel.set_volume(0, 1)
time.sleep(2)
channel.set_volume(0, 0)

channel = sound.play()
channel.set_volume(1, 1)
time.sleep(2)
channel.set_volume(0, 0)
