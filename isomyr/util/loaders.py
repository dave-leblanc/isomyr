import os
from glob import glob

import pygame


class ResourceLoader(object):

    def __init__(self, basedir="."):
        self.basedir = os.path.abspath(basedir)

    def loadAction(self, filename):
        return filename

    def load(self, filename=None, filenames=None, fileGlob=None):
        """
        Loads a list of files.
        """
        if filename:
            filenames = filename
        if filenames and not isinstance(filenames, list):
            filenames = [filenames]
        if fileGlob and not filenames:
            match = os.path.join(self.basedir, fileGlob)
            filenames = sorted(glob(match))
        elif not isinstance(filenames, list):
            filenames = [filenames]
        files = []
        for filename in filenames:
            fullPath = os.path.join(self.basedir, filename)
            files.append(self.loadAction(fullPath))
        return files

class ImageLoader(ResourceLoader):

    def __init__(self, transparency=None, **kwargs):
        super(ImageLoader, self).__init__(**kwargs)
        self.transparency = transparency

    def loadAction(self, fullPath):
        loadedImage = pygame.image.load(fullPath).convert()
        # Load images using a colorkey transparency, if provided.
        if self.transparency:
            loadedImage.set_colorkey(self.transparency)
        return loadedImage


class SoundLoader(ResourceLoader):

    def loadAction(self, fullPath):
        return pygame.mixer.Sound(fullPath)

    def load(self, *args, **kwds):
        return super(SoundLoader, self).load(*args, **kwds)[0]
