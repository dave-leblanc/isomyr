from unittest import TestCase

from isomyr.isometric import transform


class IsometricTransformTestCase(TestCase):

    def test_transform(self):
        self.assertEquals(transform([0, 0, 0], [0, 0]), [0, 0])
        self.assertEquals(transform([0, 0, 0], [0, 1]), [0, 1])
        self.assertEquals(transform([0, 0, 0], [1, 0]), [1, 0])
        self.assertEquals(transform([0, 0, 0], [1, 1]), [1, 1])

        self.assertEquals(transform([10, 10, 10], [0, 0]), [0, 0])
        self.assertEquals(transform([100, 100, 100], [0, 1]), [0, 1])
        self.assertEquals(transform([2, 4, 8], [1, 0]), [-1, -5])
        self.assertEquals(transform([30, 50, 70], [1, 1]), [-19, -29])

        self.assertEquals(transform([-10, -10, -10], [0, 0]), [0, 0])
        self.assertEquals(transform([-100, -100, -100], [0, 1]), [0, 1])
        self.assertEquals(transform([-2, -4, -8], [1, 0]), [3, 5])
        self.assertEquals(transform([-30, -50, -70], [1, 1]), [21, 31])
