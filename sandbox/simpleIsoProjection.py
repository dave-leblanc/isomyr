from math import asin, cos, radians, sin, tan

from numpy import matrix


# Viewing angle
viewAngle = radians(30)
matrixAngle = asin(tan(viewAngle))
# Top-down rotation angle
zXAngle = radians(45)


points = [
    [0, 0, 0],
    [1, 1, 1],
    [1, 1, 9],
    ]

point = matrix([points[2]]).getT()


yToZRotation = matrix([
    [1, 0, 0],
    [0, cos(matrixAngle), sin(matrixAngle)],
    [0, -sin(matrixAngle), cos(matrixAngle)]])


zToXRotation = matrix([
    [cos(zXAngle), 0, -sin(zXAngle)],
    [0, 1, 0],
    [sin(zXAngle), 0, cos(zXAngle)]])


xYProjection = matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]])


rotatedPoint = yToZRotation * zToXRotation * point
projectedPoint = xYProjection * rotatedPoint

print point
print rotatedPoint
print projectedPoint
