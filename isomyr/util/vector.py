"""
Vector mathematics functions.
"""
from numpy import array


SOUTH  =  [1, 0, 0]
WEST  =  [0, 1, 0]
UP = [0, 0, 1]
NORTH  =  [-1, 0, 0]
EAST  =  [0, -1, 0]
DOWN = [0, 0, -1]


def addVectors(v1, v2):
    return list(array(v1) + array(v2))


def subtractVectors(v1, v2):
    return list(array(v1) - array(v2))


def multiplyVectors(v1, v2):
    return list(array(v1) * array(v2))


def divideVectors(v1, v2):
    """
    Divides the elements of vector v1 by the elements of vector v2.
    """
    return list(array(v1) / array(v2))


def replaceVector(v1, v2):
    for index, element in enumerate(v1):
        v2[index] = element


def squish(a):
    if a == 0:
        return a
    return a / abs(a)


def squishAndSwitch(a):
    return squish(a) * -1


def removeMagnitude(v1):
    return map(squish, v1)


def getLargestComponentVector(v1):
    largest = [0] * 3
    v2 = map(abs, v1)
    largest[v2.index(max(v2))] = 1
    return multiplyVectors(largest, map(squish, v1))


def reverseDirection(v1, v2):
    """
    Defines a vector that goes in the opposite direction of the computed
    difference between two given vectors.
    """
    return map(squishAndSwitch, subtractVectors(v1, v2))


def vectorToDirection(v1):
    """
    Converts a vector to a direction. For vectors with more than one non-zero
    component, the "prominant" direction is dictated by the component that
    contributes the most (i.e., the largest one); all other components are set
    to zero. If there two or more components share a high value, the first one
    will be chosen over later ones (e.g., y will be chosen over z). Valid
    values for a direction range from 0 to 5.
    """
    face = 0
    for index, element in enumerate(getLargestComponentVector(v1)):
        if abs(element) == 1:
            if element == -1:
                element = 1
            else:
                element = 0
            face = element + (index * 2)
    return face


def squaredMagnitude(v1):
    """
    Square of the magnitude of the vector.
    """
    return sum(array(v1) * array(v1))
