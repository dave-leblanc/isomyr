import math

import pygame
from pygame import display

from isomyr import handler
from isomyr.exceptions import DuplicateObjectError
from isomyr.objects.character import Player
from isomyr.thing import ThingOfThings
from isomyr.world.calendar import Calendar, DateTime, Time


class World(ThingOfThings):
    """
    The object that keeps track of all other objects.
    """
    def __init__(self, name="", sceneSize=None, universe=None, time=None,
                 axialTilt=None, solarSystem=None):
        self.name = name
        self.universe = universe
        self.time = time
        self.scenes = {}
        self.player = None
        # Axial tilt is measured in degrees.
        self.axialTilt = axialTilt or 23
        # XXX we need a units.Metric class that contains all units of
        # measurememnt for a game
        self.metric = None
        # XXX distance units need to use whatever is defined in the metric
        self.distanceToStar = 0
        # XXX percentage of sky area taken up by the sun?
        self.solarSystem = solarSystem

    def getUniverse(self):
        return self.universe

    def getSolarSystem(self):
        return self.solarSystem

    def getSun(self):
        return self.getSolarSystem().getSun()

    def addScene(self, name="", sceneObject=None):
        if name and not sceneObject:
            sceneObject = Scene(name=name, world=self)
        sceneObject.world = self
        exists = self.scenes.setdefault(name, sceneObject)
        if exists != sceneObject:
            msg = ("An object with that name has already been added to the "
                    "scene.")
            raise DuplicateObjectError(msg)
        return sceneObject

    def getScene(self, name):
        return self.scenes.get(name)

    def getPlayer(self):
        return self.player

    def getSurface(self):
        return self.player.getView().getSurface()

    def getGameTime(self):
        return self.universe.engine.gametime.getTime()

    def setWorldTime(self, time):
        """
        Set the in-game, character-experienced time for this world.
        """
        if not time:
            time = DateTime()
        timeClasses = [isinstance(time, x) for x in [Time, DateTime]]
        if True not in timeClasses:
            time = DateTime(*time.timetuple())
        if not self.time:
            self.time = Calendar(timeInstance=time)
        else:
            self.time.setTime(time)
        self.time.setWorld(self)

    def getWorldTime(self):
        return self.time


def worldFactory(universe=None, name="", sceneSize=(400, 360)):
    if not universe:
        from isomyr.universe import Universe
        universe = Universe()
    return universe.addWorld(name=name, sceneSize=sceneSize)


class Scene(ThingOfThings):
    """
    An object that represents the room or a portion of an outside area.
    """

    def __init__(self, world=None, latitude=None, altitude=None, *args,
                 **kwds):
        super(Scene, self).__init__(*args, **kwds)
        self.world = world
        self.latitude = latitude
        self.altitude = altitude
        self.view = None

    # XXX move into common base class with Thing... something like
    # SkinableMixin.
    def setSkin(self, skin):
        self.skin = skin

    def getUpdatableObjects(self):
        updatableObjects = []
        for objectInstance in self.objectList:
            if objectInstance.skin:
                updatableObjects.append(objectInstance)
        return updatableObjects

    def addPlayer(self, player=None, *args, **kwds):
        if not player:
            player = Player(*args, **kwds)
        self.world.player = player
        self.addObject(player)
        return player

    def removePlayer(self, player=None):
        self.removeObject(player)

    def getPlayer(self):
        return self.world.getPlayer()

    def setView(self, view):
        self.view = view

    def getView(self):
        return self.view

    def addObject(self, objectInstance):
        super(Scene, self).addObject(objectInstance)
        objectInstance.world = self.world
