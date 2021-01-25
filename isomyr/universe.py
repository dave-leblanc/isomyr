import math

import pygame
from pygame import display

from isomyr import handler
from isomyr.exceptions import DuplicateObjectError
from isomyr.objects.character import Player
from isomyr.thing import Thing, ThingOfThings
from isomyr.world.world import World


STAR_TYPE_M = "M"


class Star(Thing):

    def __init__(self, type=STAR_TYPE_M, color=None, mass=None, radius=None,
                 luminosity=None, temperature=None):
        self.type = type
        self.color = color
        self.mass = mass
        self.radius = radius
        self.luminosity = luminosity
        self.temperature = temperature

    def setType(self, type):
        self.type = type

    def setColor(self, color):
        self.color = color


class SolarSystem(ThingOfThings):
    """
    A simple object container for objects and metadata shared by all world
    instances in a solar system.
    """
    def __init__(self, sun=None, worlds=None):
        super(SolarSystem, self).__init__()
        self.sun = sun
        if worlds:
            self.addPlanets(worlds)

    def setSun(self, star=None):
        self.sun = star

    def getSun(self):
        return self.sun

    def addPlanet(self, world):
        super(SolarSystem, self).addObject(world)

    def addPlanets(self, worlds):
        super(SolarSystem, self).addObjects(worlds)

    def getPlanet(self, name):
        return super(SolarSystem, self).getObject(name)

    @property
    def worlds(self):
        return [x for x in self.objectList if isinstance(x, World)]


class Universe(ThingOfThings):
    """
    The object that keeps track of all worlds. This is the top-level container
    for all games.
    """
    def __init__(self, worlds=None, sceneSize=None, *args, **kwds):
        super(Universe, self).__init__(*args, **kwds)
        self.worlds = worlds or []
        self.cosmologicalConstant = 10 ** -29 # g/cm3
        self.speedOfLight = 299792458 # m/s
        self.pi = math.pi
        # Set up the causal relationships between events and event reactions
        # (handlers) for the objects in this world.
        handler.registerEventHandlers()

    def addWorld(self, name="", world=None, sceneSize=None):
        if name and not world:
            from isomyr.world.world import World
            world = World(name=name, universe=self, sceneSize=sceneSize)
        world.universe = self
        self.worlds.append(world)
        self.addObject(world)
        return world

    def getWorld(self, name=""):
        # XXX up-call to getObect
        if not name and len(self.worlds) > 0:
            return self.worlds[0]
        super(Universe, self).getObject(name)

    def getPlayer(self):
        return self.getWorld().getPlayer()
