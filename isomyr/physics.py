"""
Collision detection, response and touch detection
"""
import sys
from random import randint

from isomyr.thing import FallableThing, PhysicalThing
from isomyr.util.vector import (
    addVectors, replaceVector, reverseDirection, divideVectors,
    multiplyVectors, subtractVectors)


# XXX Often referred to as imp in the code so perhaps Impact would be a better
# name. Also used for touch routines as well.
# XXX Hrm, it it's used for touch routines as well, maybe Contact would be a
# better name.
class Collider(object):
    """
    Stores the impact of a collision.

    impact: indicates an impact: Boolean
    impactSide_object1: hit face number of the first object: integer 0-5
    impactSide_object2: hit face number of the second object: integer 0-5
    impact_time: the integer time of the collision (now really a distance)
        see collision detect routine: integer
    """

    def __init__(self):
        self.impact = False
        self.impactSide_object1 = 0
        self.impactSide_object2 = 0
        self.impact_time = 0


def detectCollision(object1, object2):
    """
    Discovers if there is a collision between two objects.

    object1: The first object to be detected: class or subclass of object_3d
    object2: The second object to be detected: class or subclass of object_3d
    Returns imp: a Collider with the impact time and faces hit on both
        objects: class Collider.

    Notes: Simple collision detection, does not handle if objects pass
    completely through each other if they have high velocity and the objects
    are small.
    """
    imp = Collider()
    for i in range(3):
        # Check if intersecting.
        if (object1.location[i] + object1.size[i]) <= object2.location[i]:
            return imp
        if object1.location[i] >= (object2.location[i] + object2.size[i]):
            return imp
    # If intersecting, calculate the first face impacted.
    imp.impact = True
    imp.impact_time = sys.maxint
    for i in range(3):
        impact_time_face1 = (
           object1.location[i] + 
           object1.size[i] - 
           object2.location[i])
        impact_time_face2 = (
           object2.location[i] +
           object2.size[i] -
           object1.location[i])
        if impact_time_face1 < impact_time_face2:
            impactSide_object1 = i << 1
            impactSide_object2 = (i << 1) + 1
            impact_time_coord = impact_time_face1
        elif impact_time_face1 >=  impact_time_face2:
            impactSide_object1 = (i << 1) + 1
            impactSide_object2 = i << 1
            impact_time_coord = impact_time_face2
        if impact_time_coord < imp.impact_time:
            imp.impact_time = impact_time_coord
            imp.impactSide_object1 = impactSide_object1
            imp.impactSide_object2 = impactSide_object2
    return imp


def collisionProcessor(obj_group):
    """
    Detects collisions amongst all object pairs and moves them back until
    just before the collision and runs the object collision responses.

    obj_group: A list of objects within the scene: list of class or subclass of
        object_3d
    """
    imp = Collider()
    #runs the collision routines until no impacts occur.
    while True:
        noimpact = True
        for object1 in range(len(obj_group)):
            for object2 in range(object1+1, len(obj_group)):
                # If both objects are not fixed call the collision detector to
                # get the first object collided with and time of collision,
                # faces collided with.
                if (obj_group[object1].fixed is False or
                    obj_group[object2].fixed is False): 
                    imp = detectCollision(
                        obj_group[object1], obj_group[object2])
                    if imp.impact is True:
                        # Collision response, currently just moving the two
                        # objects apart to just touching.
                        collisionResponse(
                            obj_group[object1], obj_group[object2], imp)
                        obj_group[object1].eventCollision(
                            obj_group[object2], imp.impactSide_object1)
                        obj_group[object2].eventCollision(
                            obj_group[object1], imp.impactSide_object2)
                        noimpact = False
        if noimpact is True:
            break 


def collisionResponse(object1, object2, imp):
    """
    Moves back the objects until they are adjacent on their colliding sides.

    object1: The first object to be moved: class or subclass of object_3d
    object2: The second object to be moved: class or subclass of object_3d
    imp: a Collider with the impact time and faces hit on both objects: class
    Collider.
    """

    # Calculate the collision coordinate from the face.
    coord = imp.impactSide_object1 >> 1
    # Four cases based on if the object has its fixed flag to stop pushing.
    if object1.fixed is True and object2.fixed is True:
        # Do nothing as both objects are fixed.
        return
    if object1.fixed is False and object2.fixed is True:
        if imp.impactSide_object1%2 is 0:
            object1.location[coord] = (
                object2.location[coord] - object1.size[coord] - 1)
        else:
            object1.location[coord] = (
                object2.location[coord] + object2.size[coord])
    if object1.fixed is True and object2.fixed is False:
        if imp.impactSide_object2%2 is 0:
            object2.location[coord] = (
                object1.location[coord] -
                object2.size[coord] - 1)
        else:
            object2.location[coord] = (
                object1.location[coord] +
                object1.size[coord])
    if object1.fixed is False and object2.fixed is False:
        if imp.impactSide_object1%2 is 0:
            delta = (
                object1.location[coord] +
                object1.size[coord] -
                object2.location[coord])
            object1.location[coord] = int(
                object1.location[coord] - delta / 2.0)
            object2.location[coord] = int(
                object2.location[coord] + delta / 2.0 + 1)
        else:
            delta = (
                object2.location[coord] +
                object2.size[coord] -
                object1.location[coord])
            object2.location[coord] = int(
                object2.location[coord] - delta / 2.0)
            object1.location[coord] = int(
                object1.location[coord] + delta / 2.0 + 1)



#NOTE: we are using an impact structure for touch which may not be appropriate

def touchProcessor(obj_group):
    """
    Discover if any of the objects in the group are touching and call their
    touch response routines.

    obj_group: A list of objects within the scene: list of class or subclass of
        object_3d
    """
    for object1 in range(len(obj_group)):
        for object2 in range(object1+1, len(obj_group)):
            #Detect a touch between object 1 and object 2
            imp = touch(obj_group[object1], obj_group[object2])
            if imp.impact is True:
                #Touch response, call the objects touch event handler
                obj_group[object1].eventTouch(
                    imp.impact, obj_group[object2], imp.impactSide_object1)
                obj_group[object2].eventTouch(
                    imp.impact, obj_group[object1], imp.impactSide_object2) 


def touch(object1, object2):
    """Detect if two objects are touching.

    object1: The first object to be detected: class or subclass of object_3d
    object2: The second object to be detected: class or subclass of object_3d

    imp: a Collider with the impact time and faces touched on both objects:
    class Collider.
    """
    # XXX Rewrite this with numpy and vector math.
    # Produce an imaginary collision object based on projecting object 1 in the
    # direction of object 2.
    sense_object1 = PhysicalThing(
        name="touch sense", location=[0, 0, 0], size=[0, 0, 0])
    # Take the 2 centres of the objects.
    centre_object1 = addVectors(
        object1.location, divideVectors(object1.size, [2, 2, 2]))
    centre_object2 = addVectors(
        object2.location, divideVectors(object2.size, [2, 2, 2]))
    # Find the projected vector between them.
    project_vector = multiplyVectors(reverseDirection(
        centre_object1, centre_object2), [2, 2, 2])
    # Add the projected vector to the first objects location.
    sense_object1.location = addVectors(object1.location, project_vector)
    replaceVector(object1.size, sense_object1.size)
    # Collision detect the sense object with the object 2.
    imp = detectCollision(sense_object1, object2)
    return imp


def collisionChecker(test_object, object_group):
    """Checks if the test object collides with any object in the object group.

    test_object: The object to be tested for a collision: class or subclass of
        object_3d.
    object_group: A list of objects : list of class or subclass of object_3d
    Return True/False: True for a collision : boolean
    """
    for obj in range(len(object_group)):
        #call the collision detector to get the first object collided with
        imp = detectCollision(test_object, object_group[obj])
        if imp.impact is True:
            return True
    return False

def getDropPosition(source_object, drop_object, facing, separation):
    """Calculates a location to drop and object in front of the facing object.

    source_object: the facing object that is dropping the drop_object: class or
        subclass of object_3d
    drop_object: the object being dropped: class or subclass of object_3d
    facing: 3d facing vector : list of integers: [x, y, z]

    Notes:
    The drop object is in the direction of the facing vector and projected from
        the centre of
    the source object to its edge and then an additional amount to the centre
        of the drop object.
    after that it is offset by half the size of the drop objects size vector.
    """
    drop_half_size = divideVectors(drop_object.size, [2, 2, 2])
    # The centre of the source object.
    source_half_size = divideVectors(source_object.size, [2, 2, 2])
    source_centre = addVectors(source_object.location, source_half_size)
    # Offset from the centre of the source object to the centre of the drop
    # object.
    displ_vect = addVectors(
        multiplyVectors(facing, drop_half_size),
        multiplyVectors(facing, source_half_size))
    # Add a small offset to distance it from the source object.
    offset_vect = addVectors(
        displ_vect, multiplyVectors(
            facing, [separation, separation, separation]))
    # Produce the offset location of the corner of the drop object).
    corner_vect = subtractVectors(offset_vect, drop_half_size)
    test_pos = addVectors(corner_vect, source_centre)
    return test_pos


class Destructor(FallableThing):
    """
    A class for objects which delete themselves when they collide with
    another object.

    die: Flag to say if the object should destroy itself: boolean
    scene: The current scene of the object: scene class
    """
    def __init__(self, pos, size, objtype, scene, fixed=False):
        super(Destructor, self).__init__(pos, size, fixed=fixed)
        self.die = False
        self.scene = scene

    def act(self):
        """Redefined tick function for self destruction on collision."""
        super(Destructor, self).act()
        if self.die is True:
            self.scene.object_group.remove(self)

    def eventCollision(self, otherObject, impactSide):
        """
        Redefined collision event handler for self destruction on collision.
        """
        self.die = True


class Exploder(PhysicalThing):

    def __init__(self, pos, size, objtype, scene, fixed=True):
        super(Exploder, self).__init__(pos, size, fixed=fixed)
        self.new_object_time = 0
        self.scene = scene

    def act(self):
        super(Exploder, self).act()
        if self.new_object_time == 100:
            pos = [randint(20, 130), randint(20, 130), 100]
            self.scene.object_group.append(
                Destructor(pos, [30, 30, 30], 8, self.scene))
            self.new_object_time = 0
        self.new_object_time = self.new_object_time+1


class DelayedDestructor(FallableThing):
    """
    A class for objects which delete themselves after a set period. 
 
    die: Flag to say if the object should destroy itself: boolean
    scene: The current scene of the object: scene class
    new_object_time: Time in ticks for when this object will disolve (destroy
        itself): integer
    """
    def __init__(self, pos, size, objtype, scene, fixed = False):
        super(DelayedDestructor, self).__init__(pos, size, fixed=fixed)
        self.die = False
        self.new_object_time = 0
        self.scene = scene

    def act(self):
        """
        Redefined tick function for self destruction after a delay in time.
        """
        super(DelayedDestructor, self).act()
        if self.new_object_time == 100:
            pos = [randint(20, 130), randint(20, 130), 100]
            self.scene.object_group.remove(self)
        self.new_object_time = self.new_object_time + 1


class Disolver(PhysicalThing):

    def __init__(self, pos, size, objtype, scene, fixed=True):
        super(Disolver, self).__init__(pos, size, fixed=fixed)
        self.new_object_time = 0
        self.scene = scene

    def act(self):
        super(Disolver, self).act()
        if self.new_object_time == 30:
            pos = [randint(10, 170), randint(10, 170), 100]
            self.scene.object_group.append(
                DelayedDestructor(pos, [20, 30, 30], 8, self.scene))
            self.new_object_time = 0
        self.new_object_time = self.new_object_time + 1
