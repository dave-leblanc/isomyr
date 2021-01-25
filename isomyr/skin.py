"""
Defines the animated images to draw for an object type and object state.
"""
from datetime import datetime

from pygame import transform

from isomyr.exceptions import (
    SkinCycleSequenceMismatchError, SkinDirectionalImageError,
    SkinImageCorrelationMismatchError, SkinImageCountError)
from isomyr.util import vector


class Skin(object):
    """The base skin class used to represent an object type on the screen.

    images: The images used to display an object type: list of image
    getImage(obj) : returns the image to display based on the state of the
        object.
    """

    def __init__(self, images=None):
        self.images = images or []
        self.controller = None

    def setController(self, controller):
        """
        The controller is the object/thing that wears the skin.
        """
        self.controller = controller

    # Default behaviour returns image 0 from the images.
    def getImage(self):
        """
        Returns the image to display based on the state of an object.
        """
        return self.images[0]


class AnimatedSkin(Skin):
    """
    Simple animated skin that cycles through each images image every tick.
    """
    def __init__(self, images):
        super(AnimatedSkin, self).__init__(images)
        self.index = 0
        self.counter = 0
        self.speed = .5

    def getImage(self):
        """
        Redefined image query to allow cycled animation.
        """
        image = self.images[self.index]
        self.counter += 1
        if self.counter > len(self.images) / self.speed:
            self.counter = 0
        speedAdjusted = int(self.counter * self.speed)
        self.index = speedAdjusted % len(self.images)
        return image


class DirectedAnimatedSkin(Skin):
    """
    Animated skin who has a different image for each direction they face and
    for each frame of animation.

    This skin requires a list of 12 images which are divided into 4 directions
    of facing on the x, y plane and 3 cycles in each direction. Each image
    direction group comprises of 3 images which are animated in the sequence
    [0, 1, 0, 2], to complete a full movement.

    For:
        facing [1, 0, 0]: images [0, 1, 2]
        facing [0, -1, 0]: images [3, 4, 5]
        facing [0, 1, 0]: images [6, 7, 8]
        facing [-1, 0, 0]: images [9, 10, 11]
    """
    def __init__(self, south, east, north=None, west=None, frameSequence=None,
                 framesPerCycle=None):
        self.south = south
        self.east = east
        self.north = north or []
        self.west = west or []
        if not self.north:
            for image in self.east:
                self.north.append(transform.flip(image, 1, 0))
        if not self.west:
            for image in self.south:
                self.west.append(transform.flip(image, 1, 0))
        # Make sure that every direction has the same image count.
        directionCount = 4 # S,E,N,W
        imageCount = len(self.south + self.east + self.north + self.west)
        if imageCount != directionCount * len(self.south):
            raise SkinImageCorrelationMismatchError
        # Set the frames per cycle.
        if not framesPerCycle:
            if frameSequence:
                framesPerCycle = len(frameSequence)
            else:
                framesPerCycle = imageCount / directionCount
        self.framesPerCycle = framesPerCycle
        # Set the order in which the frames are displayed.
        if not frameSequence:
            frameSequence = xrange(self.framesPerCycle)
        self.frameSequence = frameSequence
        # Make sure that there as as many frame sequnces as there are frames
        # per cycle.
        if len(self.frameSequence) != self.framesPerCycle:
            raise SkinCycleSequenceMismatchError
        # Make sure that the total number of unique skin images macthes the
        # previously calculated image count.
        expectedImageCount = len(set(self.frameSequence)) * directionCount
        if imageCount != expectedImageCount:
            raise SkinImageCountError

    def getImage(self):
        """Redefined getImage to allow multidirectional animation."""
        if self.controller.facing == vector.SOUTH:
            return self.south[self.frameSequence[self.controller.cycle]]
        if self.controller.facing == vector.EAST:
            return self.east[self.frameSequence[self.controller.cycle]]
        if self.controller.facing == vector.WEST:
            return self.west[self.frameSequence[self.controller.cycle]]
        if self.controller.facing == vector.NORTH:
            return self.north[self.frameSequence[self.controller.cycle]]
        raise SkinDirectionalImageError


class ExaminableSkin(Skin):
    """
    A skin subclass to allow a more detailed picture of an object when its
    being examined.

    examine_image: detailed image of the object: image class
    """
    def __init__(self, images, examine_image):
        super(ExaminableSkin, self).__init__(images)
        self.examine_image = examine_image
