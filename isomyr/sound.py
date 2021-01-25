from datetime import datetime, timedelta

import pygame


class Sound(object):

    def __init__(self, volume=(0.5, 0.5), sound=None):
        self.volume = volume
        self.file = file
        self.sound = sound

    def emit(self):
        channel = self.sound.play(loops=0)
        channel.set_volume(*self.volume)

    def setVolume(self, volume):
        self.volume = volume


class CyclicSound(Sound):

    def __init__(self, frequency=1, *args, **kwds):
        super(CyclicSound, self).__init__(*args, **kwds)
        self.frequency = timedelta(0, frequency)
        self.lastSound = None

    def emit(self):
        doEmit = False
        if not self.lastSound:
            doEmit = True
            self.lastSound = datetime.now()
        else:
            now = datetime.now()
            delta = now - self.lastSound
            if delta > self.frequency:
                doEmit = True
                self.lastSound = now
        if doEmit:
            super(CyclicSound, self).emit()

    def setFrequency(self, frequency):
        self.frequency = frequency
