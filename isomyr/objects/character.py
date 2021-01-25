"""
Object engine classes for Isomyr.

Note: It is very important that objects modify their location or the object
lists in their tick routines. Modifying these values in event receiver routines
will mean that often a necessary collision detection has not occurred and that
the drawn display will have errors.
"""
from isomyr.event import PlayerInventoryUpdateEvent, notify
from isomyr.physics import getDropPosition, collisionChecker
from isomyr.thing import FallableThing, PhysicalThing, PortableThing
from isomyr.util.vector import vectorToDirection, NORTH, SOUTH


class Actor(FallableThing):
    """
    Defines a new object subclass which can do human physical movement: facing,
    jumping, and a movement cycle.

    cycle: location of moviment cycle, ie leg lifted, leg down etc: integer
    facing* : to show which way the actor is facing: list of 3 facing integers
        [x, y, z]

    * Note: due to facing not being taken into account for collision detection
    and drawing routines the actor sprites must be equal dimensions on the base
    of their bounding box.
    """
    def __init__(self, velocityModifier=1, fixed=False, *args, **kwds):
        super(Actor, self).__init__(
            velocityModifier=velocityModifier, fixed=fixed, *args, **kwds)
        self.velocityModifier = velocityModifier
        self.velocity = map(lambda x: x * self.velocityModifier, SOUTH)
        self.cycle = 0
        self.facing = SOUTH


class WalkingActor(Actor):
    """
    An Actor that is capable of walking (and jumping).
    """
    def __init__(self, *args, **kwds):
        super(WalkingActor, self).__init__(*args, **kwds)
        self.walkSound = None

    def setWalkSound(self, sound):
        self.walkSound = sound

    def updatePosition(self, *args, **kwds):
        super(WalkingActor, self).updatePosition(*args, **kwds)
        # XXX If the player jumps, the sound should stop, so we need to do a
        # check against touching or something.
        # XXX If the player velocity changes, the step frequency should change
        # as well.
        if self.walkSound:
            self.walkSound.emit()

    def animateWalk(self):
        """
        Walking animation: Cycle through each of the 4 movement frames
        """
        if (self.location[0] != self.last_location[0] or 
            self.location[1] != self.last_location[1]):
            self.cycle += 1
            if self.cycle == self.skin.framesPerCycle:
                self.cycle = 0
        else:
            self.cycle = 0

    def respond(self):
        """
        For a walking actor object, its response to the world is to walk.
        """
        self.animateWalk()
        # Velocity movement: Standard object movement
        super(WalkingActor, self).respond()
 
    def jump(self):
        """Action for the actor to jump."""
        if self.falling is False:
            # Give some altitude (z-direction).
            self.velocity[2] = self.velocity[2] + 8
            self.falling = True


class NPC(WalkingActor):
    """
    An automated, non-playing actor. Characteristics include the following:
        - turns around from any collision
    """
    def eventCollision(self, otherObject, impactSide):
        """ Turn around 180 degrees and continue walking """
        # Call actors standard collision code.
        super(NPC, self).eventCollision(otherObject, impactSide)
        # Simple toggle movement.
        if self.collision_time == self.world.time.getTime():
            # XXX what about EAST and WEST?
            if self.facing == SOUTH and impactSide is 0:
                self.velocity[0] = -1 * self.velocityModifier
                self.facing = NORTH
            elif self.facing == NORTH and impactSide is 1:
                self.velocity[0] = self.velocityModifier
                self.facing = SOUTH
            self.collision_time = self.world.time.getTime()


class Monster(NPC):
    """
    An aggresive non-playing actor.
    """
    def __init__(self, velocityModifier=2, *args, **kwds):
        super(Monster, self).__init__(
            velocityModifier=velocityModifier, *args, **kwds)

    def respond(slef):
        """
        A monster's response to the world is to attack.
        """
        pass


class Player(WalkingActor):
    """
    Class capable of travelling between scenes and picking up and dropping
    objects
 
    scene: the current scene of the avatar: scene class

    inventory: the objects that the avatar is carrying: list of object_3d class
        or subclass
    using: the current object that is in the hand of the actor: integer
    max_inventory: the maximum number of objects the avatar can carry: integer
    drop_command: Flag for the event handler to show when a drop request has
        been received: boolean
    pick_up_command: Flag for the event handler to show when a pick_up request
        has been received: boolean
    current_location: Used when changing scenes for new postion vector: list of
        3
        integers [x, y, z]
    current_scene: Used when changing scenes for the new scene: scene class

    Note: This class directly modifies the scene list. Care must be taken
    when writing any code which does this as objects disappear when other
    actors may think they are still available.
    """

    def __init__(self, *args, **kwds):
        super(Player, self).__init__(*args, **kwds)
        self.current_location = self.location
        self.current_scene = None
        # Flags for pick up and drop messages from external control: perhaps
        # this means we really need a player object
        self.pick_up_command = False
        self.drop_command = False
        self.inventory = []
        self.max_inventory = 4
        self.using = 0

    def setScene(self, scene):
        super(Player, self).setScene(scene)
        self.current_scene = scene

    def getScene(self):
        return self.current_scene

    def getView(self):
        return self.getScene().getView()

    def respond(self):
        """
        Redefined tick function to allow movement between scenes.
        """
        if self.scene is not self.current_scene:
            self.location = list(self.current_location)
            self.current_scene.addObject(self)
            self.scene.removeObject(self)
            self.scene = self.current_scene
        if self.pick_up_command is True:
            self.pick_up()
        if self.drop_command is True:
            self.drop()
        super(Player, self).respond()

    def pickUp(self):
        """
        Pick_up object action.
        """
        face = vectorToDirection(self.facing)
        # XXX Wow, this whole chunk needs to be refactored.
        for i in range(len(self.touched_objects)):
            # Pick up the first object we are touching.
            isPortable = isinstance(self.touched_objects[i], PortableThing)
            haveFreeSpace = len(self.inventory) < self.max_inventory
            isFacing = face is self.touched_faces[i]
            if isFacing and isPortable and haveFreeSpace:
                item = self.touched_objects[i]
                if item.request_pick_up(self) is True:
                    self.inventory.append(item)
                    self.scene.objectList.remove(item)
                    notify(PlayerInventoryUpdateEvent(self))
                    return item
 
    def drop(self):
        """
        Drop object action.
        """
        # Check if we are carrying something to drop
        # Routine does not take into account facing rotation of an object
        if len(self.inventory) is 0:
            return
        # Get the candidate object to be dropped
        item = self.inventory[self.using]
        # Check to see if there is space for the object to be dropped
        # Create a "check" object to put in the drop location
        checkPosition = getDropPosition(self, item, self.facing, 4)
        checkObject = PhysicalThing("check object", checkPosition, item.size)
        # Check if the test object collides with any other object in the scene
        if collisionChecker(checkObject, self.scene.objectList):
            return
        # Put the object into the current scene by adding it to the scenes
        # object list
        # Check if the object wants to be dropped
        if item.request_drop(self) is False:
            return
        # Drop the object
        item.location = checkObject.location
        self.inventory.remove(item)
        notify(PlayerInventoryUpdateEvent(self))
        self.scene.objectList.append(item)
        if self.using is not 0:
            self.using = self.using - 1
        return item
