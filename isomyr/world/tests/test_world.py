from unittest import TestCase

from isomyr.universe import SolarSystem, Star
from isomyr.world.world import World


class SolarSystemTestCase(TestCase):

    def setUp(self):
        self.system = SolarSystem()

    def test_creation(self):
        self.assertEquals(self.system.sun, None)
        self.assertEquals(self.system.worlds, [])

    def test_addPlanet(self):
        mercury = World("Mercury")
        self.system.addPlanet(mercury)
        planet = self.system.getPlanet("Mercury")
        self.assertEquals(planet, mercury)

    def test_addPlanets(self):
        mercury = World("Mercury")
        venus = World("Venus")
        self.assertEquals(self.system.worlds, [])
        self.system.addPlanets([mercury, venus])
        self.assertEquals(self.system.worlds, [mercury, venus])
