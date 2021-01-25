from unittest import main, TestCase
from math import asin, cos, radians, sin, tan

from numpy import matrix


def getTranslationMatrix(origin, direction="initial"):
    """
    Provide a translation matrix for a given new origin.

    @param direction: valid values are "initial" or "revert"; an initial
        translation matrix will subtract the supplied origin; the revert
        direction will add the supplied origin back.
    """
    if len(origin) < 4:
        origin.append(1)
    data = [[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0]]
    if direction == "initial":
        translator = [-1, -1, -1, 1]
    else:
        translator = [1, 1, 1, 1]

    translatedOrigin = map(lambda a, b: a * b, origin, translator)
    data.append(translatedOrigin)
    return matrix(data)


def transform(point, origin=None, rollAngle=40, yawAngle=0, pitchAngle=45):
    """
    Transform a point in three dimensions, relative to an arbitrary origin, and
    project it isometrically onto a 2-dimensional plane.

    @param roll: rotation about the x-axis (transformation of y and z).
    @param yaw: rotation about the y-axis (transformation of x and z).
    @param pitch: rotation about the z-axis (transformation of x and y).
    """
    if not origin:
        origin = [0, 0, 0]
    if len(origin) == 2:
        origin.append(0)

    # Translate the point to the origin.
    if len(point) < 4:
        point.append(1)

    # Get all the angles.
    point = matrix([point])
    matrixAngle = asin(tan(radians(rollAngle)))
    yawAngle = radians(yawAngle)
    pitchAngle = radians(pitchAngle)

    # Rotation about the x-axis.
    roll = matrix([
        [1, 0, 0, 0],
        [0, cos(matrixAngle), sin(matrixAngle), 0],
        [0, -sin(matrixAngle), cos(matrixAngle), 0],
        [0, 0, 0, 1],
        ])

    # Rotation about the y-axis.
    yaw = matrix([
        [cos(yawAngle), 0, -sin(yawAngle), 0],
        [0, 1, 0, 0],
        [sin(yawAngle), 0, cos(yawAngle), 0],
        [0, 0, 0, 1],
        ])

    # Rotation about the z-axis.
    pitch = matrix([
        [cos(pitchAngle), sin(pitchAngle), 0, 0],
        [-sin(pitchAngle), cos(pitchAngle), 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        ])

    # Project on a 2-dimensional surface.
    projection2D = matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        ])

    translatedPoint = (point * getTranslationMatrix(origin)).transpose()
    rotatedPoint = roll * yaw * pitch * translatedPoint
    reTranslatedPoint = (
        rotatedPoint.transpose() *
        getTranslationMatrix(origin, direction="revert"))
    transformedPoint = projection2D * reTranslatedPoint.transpose()
    return [int(round(x)) for x in transformedPoint.flatten().tolist()[0][0:2]]


class IsometricTransformTestCase(TestCase):

    def test_transform(self):
        # As you can see, these results are very different from those produced
        # by the original Isotope transform function; they only agree on the
        # first assertion.
        self.assertEquals(transform([0, 0, 0], [0, 0]), [0, 0])
        #self.assertEquals(transform([0, 0, 0], [0, 1]), [0, 1])
        self.assertEquals(transform([0, 0, 0], [0, 1]), [-1, 1])
        #self.assertEquals(transform([0, 0, 0], [1, 0]), [1, 0])
        self.assertEquals(transform([0, 0, 0], [1, 0]), [0, 0])
        #self.assertEquals(transform([0, 0, 0], [1, 1]), [1, 1])
        self.assertEquals(transform([0, 0, 0], [1, 1]), [0, 1])

        #self.assertEquals(transform([10, 10, 10], [0, 0]), [0, 0])
        self.assertEquals(transform([10, 10, 10], [0, 0]), [14, 0])
        #self.assertEquals(transform([100, 100, 100], [0, 1]), [0, 1])
        self.assertEquals(transform([100, 100, 100], [0, 1]), [141, 1])
        #self.assertEquals(transform([2, 4, 8], [1, 0]), [-1, -5])
        self.assertEquals(transform([2, 4, 8], [1, 0]), [5, 1])
        #self.assertEquals(transform([30, 50, 70], [1, 1]), [-19, -29])
        self.assertEquals(transform([30, 50, 70], [1, 1]), [56, 9])

        #self.assertEquals(transform([-10, -10, -10], [0, 0]), [0, 0])
        self.assertEquals(transform([-10, -10, -10], [0, 0]), [-14, 0])
        #self.assertEquals(transform([-100, -100, -100], [0, 1]), [0, 1])
        self.assertEquals(transform([-100, -100, -100], [0, 1]), [-142, 1])
        #self.assertEquals(transform([-2, -4, -8], [1, 0]), [3, 5])
        self.assertEquals(transform([-2, -4, -8], [1, 0]), [-4, 0])
        self.assertEquals(transform([-30, -50, -70], [1, 1]), [-57, -7])

if __name__ == "__main__":
    main()
