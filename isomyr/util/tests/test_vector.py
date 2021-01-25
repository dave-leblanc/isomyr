from unittest import TestCase

from isomyr.util import vector

class VectorTestCase(TestCase):

    def test_addVectors(self):
        v1 = [1, 2, 3]
        v2 = [-1, 1, -8]
        v12 = vector.addVectors(v1, v2)
        self.assertEquals(v12, [0, 3, -5])

    def test_subtractVectors(self):
        v1 = [1, 2, 3]
        v2 = [-1, 1, -8]
        v12 = vector.subtractVectors(v1, v2)
        self.assertEquals(v12, [2, 1, 11])

    def test_multiplyVectors(self):
        v1 = [1, 2, 3]
        v2 = [-1, 1, -8]
        v12 = vector.multiplyVectors(v1, v2)
        self.assertEquals(v12, [-1, 2, -24])
        v1 = [1, 2, 3]
        v2 = [-1, -1, -1]
        v12 = vector.multiplyVectors(v1, v2)
        self.assertEquals(v12, [-1, -2, -3])
        v1 = [-1, -2, -3]
        v2 = [-1, -1, -1]
        v12 = vector.multiplyVectors(v1, v2)
        self.assertEquals(v12, [1, 2, 3])

    def test_divideVectors(self):
        v1 = [1, 2, 3]
        v2 = [-1, 1, -8]
        v12 = vector.divideVectors(v1, v2)
        self.assertEquals(v12, [-1, 2, -1])
        # XXX With fractional vector support, we can uncomment this.
        #self.assertEquals(v12, [-1, 2, -0.375])

    def test_replaceVector(self):
        v1 = [1, 2, 3]
        v2 = [-1, 1, -8]
        vector.replaceVector(v1, v2)
        self.assertEquals(v2, [1, 2, 3])

    def test_removeMagnitude(self):
        result = vector.removeMagnitude([1, 2, 3])
        self.assertEquals(result, [1, 1, 1])
        result = vector.removeMagnitude([1, -22, 333])
        self.assertEquals(result, [1, -1, 1])
        result = vector.removeMagnitude([1000, 22, -33333])
        self.assertEquals(result, [1, 1, -1])

    def test_reverseDirection(self):
        result = vector.reverseDirection([1, 2, 3], [0, 0, 0])
        self.assertEquals(result, [-1, -1, -1])
        result = vector.reverseDirection([0, 0, 0], [1, 2, 3])
        self.assertEquals(result, [1, 1, 1])
        result = vector.reverseDirection([1, 2, 3], [1, 2, 3])
        self.assertEquals(result, [0, 0, 0])
        result = vector.reverseDirection([1, 0, 0], [0, 0, 0])
        self.assertEquals(result, [-1, 0, 0])
        result = vector.reverseDirection([-1, 0, 0], [0, 0, 0])
        self.assertEquals(result, [1, 0, 0])
        result = vector.reverseDirection([-1, 1, 0], [0, 0, 0])
        self.assertEquals(result, [1, -1, 0])
        result = vector.reverseDirection([1, -1, 1], [0, 0, 0])
        self.assertEquals(result, [-1, 1, -1])
        result = vector.reverseDirection([1, -1, 1], [4, -4, 4])
        self.assertEquals(result, [1, -1, 1])

    def test_getLargestComponentVector(self):
        result = vector.getLargestComponentVector([0, 0, 0])
        self.assertEquals(result, [0, 0, 0])
        result = vector.getLargestComponentVector([0, -3, 0])
        self.assertEquals(result, [0, -1, 0])
        result = vector.getLargestComponentVector([0, -3, 3])
        self.assertEquals(result, [0, -1, 0])
        result = vector.getLargestComponentVector([0, 3, -3])
        self.assertEquals(result, [0, 1, 0])
        result = vector.getLargestComponentVector([0, 3, -4])
        self.assertEquals(result, [0, 0, -1])
        result = vector.getLargestComponentVector([0, 4, -4])
        self.assertEquals(result, [0, 1, 0])
        result = vector.getLargestComponentVector([-2, -3, 0])
        self.assertEquals(result, [0, -1, 0])
        result = vector.getLargestComponentVector([-42, -3, 0])
        self.assertEquals(result, [-1, 0, 0])
        result = vector.getLargestComponentVector([-42, 93, 70])
        self.assertEquals(result, [0, 1, 0])

    def test_vectorToDirection(self):

        # Unit vectors.
        result = vector.vectorToDirection([1, 0, 0])
        self.assertEquals(result, 0)
        result = vector.vectorToDirection([0, 1, 0])
        self.assertEquals(result, 2)
        result = vector.vectorToDirection([0, 0, 1])
        self.assertEquals(result, 4)
        result = vector.vectorToDirection([-1, 0, 0])
        self.assertEquals(result, 1)
        result = vector.vectorToDirection([0, -1, 0])
        self.assertEquals(result, 3)
        result = vector.vectorToDirection([0, 0, -1])
        self.assertEquals(result, 5)

        # Non-unit vectors.
        result = vector.vectorToDirection([9, 0, 0])
        self.assertEquals(result, 0)
        result = vector.vectorToDirection([0, 9, 0])
        self.assertEquals(result, 2)
        result = vector.vectorToDirection([0, 0, 9])
        self.assertEquals(result, 4)
        result = vector.vectorToDirection([-9, 0, 0])
        self.assertEquals(result, 1)
        result = vector.vectorToDirection([0, -9, 0])
        self.assertEquals(result, 3)
        result = vector.vectorToDirection([0, 0, -9])

        # Other unit combinations.
        result = vector.vectorToDirection([-1, 1, 0])
        self.assertEquals(result, 1)
        result = vector.vectorToDirection([-1, 1, -1])
        self.assertEquals(result, 1)
        result = vector.vectorToDirection([1, -1, 1])
        self.assertEquals(result, 0)
        result = vector.vectorToDirection([-1, 1, -1])
        self.assertEquals(result, 1)
        result = vector.vectorToDirection([-1, -1, -1])
        self.assertEquals(result, 1)

        # Other non-unit combinations.
        result = vector.vectorToDirection([1, 2, 3])
        self.assertEquals(result, 4)
        result = vector.vectorToDirection([1, 2, -3])
        self.assertEquals(result, 5)

    def test_squareMagnitude(self):
        result = vector.squaredMagnitude([1, 2, 3])
        self.assertEquals(result, 14)
        result = vector.squaredMagnitude([1, 1, 1])
        self.assertEquals(result, 3)
        result = vector.squaredMagnitude([2, 2, 2])
        self.assertEquals(result, 12)
        result = vector.squaredMagnitude([3, 3, 3])
        self.assertEquals(result, 27)
