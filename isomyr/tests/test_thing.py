from unittest import TestCase

from isomyr.thing import Thing
from isomyr.world.world import Scene


class ThingOfThingsRemoveObjectTestCase(TestCase):

    def setUp(self):
        self.scene = Scene(0)
        self.scene.addObject(Thing(name="apple"))
        self.scene.addObject(Thing(name="orange"))
        self.scene.addObject(Thing())

    def test_byName(self):
        self.assertEquals(len(self.scene.objectList), 3)
        result = self.scene.removeObject(name="apple")
        self.assertEquals(result, True)
        self.assertEquals(len(self.scene.objectList), 2)

    def test_byInstance(self):
        self.assertEquals(len(self.scene.objectList), 3)
        instance = self.scene.getObject("orange")
        result = self.scene.removeObject(instance=instance)
        self.assertEquals(result, True)
        self.assertEquals(len(self.scene.objectList), 2)

    def test_byNameWithNotFoundError(self):
        pass

    def test_withNoIndexError(self):
        pass
