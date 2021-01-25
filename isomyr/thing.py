from isomyr.exceptions import ObjectNotFoundError
from isomyr.util.vector import addVectors, reverseDirection


TOP_SIDE = 0
NORTH_SIDE = 0
EAST_SIDE = 0
SOUTH_SIDE = 0
WEST_SIDE = 0
BOTTOM_SIDE = 5


class ThingText(object):

    def __init__(self):
        self.pickedUp = None
        self.examined = None
        self.used = None
        self.dropped = None
        self.entered = None
        self.exitted = None
        
    def setPickedUp(self, text):
        """
        The text that will be rendered when the thing is picked up.
        """
        self.pickedUp = text

    def setExamined(self, text):
        """
        The text that will be rendered when the thing is examined.
        """
        self.examined = text

    def setUsed(self, text):
        """
        The text that will be rendered when the thing is used.
        """
        self.used = text

    def setDropped(self, text):
        """
        The text that will be rendered when the thing is dropped.
        """
        self.dropped = text

    def setEntered(self, text):
        """
        The text that will be rendered when the thing is entered.
        """
        self.entered = text

    def setExitted(self, text):
        """
        The text that will be rendered when the thing is exitted.
        """
        self.exitted = text


class ProtoThing(object):
    """
    The base abstract thing in a game universe, providing basic attributes and
    methods that are shared by all things.
    """
    def __init__(self, name="", parent=None, children=None, scene=None):
        self.name = name
        self.parent = parent
        self.children = parent or []
        self.text = ThingText()
        self.setScene(scene)

    def setScene(self, scene):
        self.scene = scene

    def getScene(self):
        return self.scene


class ThingOfThings(ProtoThing):
    """
    A thing that can be defined as an amalgamation of other things. Candidate
    subclasses might include objects that represent a universe, a world, or a
    scene.
    """
    def __init__(self, objectList=None, *args, **kwds):
        super(ThingOfThings, self).__init__(*args, **kwds)
        self.objectList = objectList or []

    def addObject(self, objectInstance):
        if objectInstance in self.objectList:
            return
        objectInstance.setScene(self)
        self.objectList.append(objectInstance)

    def addObjects(self, objectList):
        for instance in objectList:
            self.addObject(instance)

    def getObject(self, name):
        for objectInstance in self.objectList:
            if objectInstance.name == name:
                return objectInstance
        return None

    def getObjectIndex(self, name):
        try:
            instance = self.getObject(name)
            return self.objectList.index(instance)
        except ValueError:
            raise ObjectNotFoundError

    def removeObject(self, instance=None, name=""):
        if name:
            instance = self.getObject(name)
        if not instance:
            raise ObjectNotFoundError
        if not name:
            name = instance.name
        index = self.getObjectIndex(name)
        removed = self.objectList.pop(index)
        if removed:
            return True
        return False


class Thing(ProtoThing):
    """
    This class is meant to be a base class for physical things, but it can be
    used to represent any object that won't be interacting with objects in a
    physical manner.
    """
    def __init__(self, location=None, size=None, fixed=True,
                 skin=None, parent=None, children=None, *args,  **kwds):
        super(Thing, self).__init__(*args, **kwds)
        self.location = location or [0, 0, 0]
        self.last_location = location
        self.velocity = [0, 0, 0]
        self.size = size
        self.fixed = fixed
        if skin:
            self.setSkin(skin)
        else:
            self.skin = skin

    def setWorld(self, world):
        self.world = world

    def getWorld(self):
        return self.world

    def setSkin(self, skin):
        self.skin = skin
        self.skin.setController(self)


class PhysicalThing(Thing):
    """
    Base 3d object used for physical interactions.

    pos: location vector in space: list of 3 integers [x, y, z]
    size: size, dimension vector relative to the location: list of 3 integers
        [width-x, width-y, height-z]
    fixed: A flag indicating if an object can is fixed in location : boolean
    vel: velocity vector : list of 3 integers [vx, vy, vz]
    old_pos: The previous location vector of the object (unused ??): list of 3
        integers [x, y, z]
    """
    def __init__(self, weight=None, *args, **kwds):
        super(PhysicalThing, self).__init__(*args, **kwds)
        self.weight = weight

    def eventCollision(self, otherObject, impactSide):
        """
        Collision event handler. A function to record a collision with other
        objects.

        otherObject: The other object that collided with this object: object_3d
            or subclass
        impactSide: The face hit by the other object: face integer (0-5)
        """
        return

    def eventTouch(self, impact, otherObject, impactSide):
        """
        Touch event handler. A function to record a collision with other
        objects.
 
        impact: Indicates if the other object has touched this object: boolean
        otherObject: The other object that collided with this object: object_3d
            or subclass
        impactSide: The face hit by the other object: face integer (0-5)
        """
        return

    def respond(self):
        """
        For this base object, its response to the world is no response. Perfect
        for solid, non-changing game elements like the ground.
        """
        pass


class MovableThing(PhysicalThing):

    def __init__(self, velocityModifier=1, *args, **kwds):
        super(MovableThing, self).__init__(*args, **kwds)
        self.velocityModifier = velocityModifier
        self.last_scene = None

    def respond(self):
        """
        For movable objects, the response to the world is to move.
        """
        self.last_location = self.location
        self.location = addVectors(self.location, self.velocity)


class FallableThing(MovableThing):
    """
    The object_falling class defines objects which can be pulled by falling.

    If the object is touching something falling will be turned off and will not
    be applied.

    If the object is not touching something falling will be turned on and it
    will descend until it touches something. 

    falling: if falling is turned on: boolean
    coltime: the last collision time: float
    touching: if the actor is touching something: boolean
    touched_faces: list of faces being touched: list of face integers (0-5)
    touched_objects: list of objects being touched: list of object_3d class or
        subclass
    """

    def __init__(self, *args, **kwds):
        super(FallableThing, self).__init__(*args, **kwds)
        # Flag to show if falling is being applied
        # XXX renmae to self.falling
        self.falling = False
        # Flag to show if this object is touching on its bottom z face
        self.touching = False
        # List for the other objects being touched and by what face
        self.touched_objects = []
        self.touched_faces = []
        # Time of the collision? Doesnt seem to be used
        self.collision_time = 0

    def respond(self):
        """
        For falling objects, the response to the world is to fall.
        """
        if self.touching is False:
                self.falling = True
        if self.falling is True:
                self.velocity[2] = self.velocity[2] - 1
        # Clear the touching information for the next tick.
        self.touching = False
        self.touched_objects = []
        self.touched_faces = []
        super(FallableThing, self).respond()

    def updatePosition(self, offset):
        """
        Action to change velocity based on movement.

        offset: the value for the velocity: list of 3 integers [vx, vy, vz]
        """
        if self.falling is False:
            self.velocity = offset
            self.facing = reverseDirection([0, 0, 0], offset)
            collision_time = self.world.getGameTime()

    def eventCollision(self, otherObject, impactSide):
        """
        Redefined collision event handler for falling and touching.
        """
        # When colliding with something on the z axis while falling is on
        if impactSide == BOTTOM_SIDE and self.falling is True:
            self.velocity[2] = 0
            self.falling = False
        self.collision_time = self.world.getGameTime()
        return

    def eventTouch(self, impact, otherObject, impactSide):
        """
        Redefined touch event handler for falling and touching.
        """
        # Add the impact information to the touching lists of objects and faces
        if impact is True:
            self.touched_objects.append(otherObject)
            self.touched_faces.append(impactSide)
        if impact is True and impactSide == BOTTOM_SIDE:
            self.velocity[2] = 0
            self.touching = True
            self.falling = False
        # This gets called because the two objects are not touching, not
        # because this object is not touching any other objects.
        else:
            #self.falling = True
            pass

    def stop(self):
        """
        Sets the objects velocity in all directions to zero.
        """
        if self.falling is False:
            self.velocity = [0, 0, 0]


class PortableThing(FallableThing):
    """
    A class for objects that can be picked up.

    @param pickedup: A flag indicating if the object is being carried: boolean
    @param carrier: The object that is carrying this object: object_3d or
        subclass
    """

    def __init__(self, *args, **kwds):
        super(PortableThing, self).__init__(*args, **kwds)
        self.pickedup = False
        self.carrier = None
 
    def request_pick_up(self, avatar):
        """
        A handler to manage a pickup event.

            avatar: The object that wants to pick up this object
        """
        self.carrier = avatar
        self.pickedup = True
        return(True)

    def request_drop(self, scene):
        """
        A handler to manage a drop event.

            scene: The scene to put this object into: scene class
        """
        self.pickedup = False
        self.carrier = None
        return(True)

