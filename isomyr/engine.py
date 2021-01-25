from datetime import datetime

import pygame

from isomyr import physics
from isomyr.config import Keys
from isomyr.event import (
    notify, PlayerDropItemEvent, PlayerPickUpItemEvent, PlayerUsingItemEvent)
from isomyr.gui.view import View
from isomyr.skin import ExaminableSkin
from isomyr.world.calendar import DateTime, SPEED_03


class GameTime(object):

    def __init__(self):
        self.time = 0

    def getTime(self):
        return(self.time)

    def updateTime(self):
        self.time = self.time + 1


class Responder(object):
    """
    This is used by the Engine object to give objects in a given scene the
    opportunity to act and react.
    """

    def update(self, scene):
        """
        Updates the physical interaction of the objects in a given scene.

        This is the means by which all objects perform actions, respond to
        stimuli, etc.

        @param scene: the scene that is currently in view, whose object will be
            updated by this call.
        """
        # Object responses: let each object run its respond() action.
        # make a copy of the object pointers in case the objects remove
        # themselves from the master list
        updateGroup = list(scene.objectList)
        for sceneObject in updateGroup:
            sceneObject.respond()
        # Note: the objects must not modify the object lists or location in
        # their event functions called by the Collision and Touch processors.
        # Detect collisons.
        physics.collisionProcessor(scene.objectList)
        # Detect touches.
        physics.touchProcessor(scene.objectList)


class Engine(object):
    """
    Isometric game engine class.

    @param world: the world instance that the scene is a part of.
    @param offset: The location of the 0, 0, 0 point on the screen: list of
        integers [x, y]
    @param keys: the keyboard control set for the player to control the player:
        key class
    @param titlefile: The filename of the titlebar image to be used for the
        information display: string
    @param font: The font object to be used for the information display text:
        font class

    @attrib title_sprite: The titlebar image: sprite class
    @attrib responder: The isomyr element used by the engine to simulate the
        players scene: simulator class
    """

    def __init__(self, keys=None, gameSpeed=SPEED_03, *args, **kwds):
        self.initializePygame()
        self.gameSpeed = gameSpeed
        self.gametime = GameTime()
        self.world = None
        self.universe = None
        self.view = View(*args, **kwds)
        # Define the keys using default values.
        # XXX Users should be able to define new keymappings by adjusting
        # settings in a # configuration file.
        if not keys:
            keys = Keys()
        self.keys = keys

        # The minimum number of microseconds that should elapse between frames.
        self.ticksLimit = 50

        # Instantiate the object that provides scene objects the opportunity to
        # react to changes in their environment.
        self.responder = Responder()

    def initializePygame(self):
        pygame.init()

    def setStartingWorld(self, world, time=None, welcomeMessage=""):
        """
        Set the world where the starting scene takes place. The world instance
        will have a universe attribute on it for where that world exists.
        
        Note that additional worlds are set/created with the Universe object.
        """
        self.world = world
        self.world.setWorldTime(time)
        self.setUniverse(world.universe)
        scene = world.player.getScene()
        text = "You are in '%s'.\n" % scene.name
        self.view.setScene(scene, prelude=welcomeMessage, text=text)

    def setWelcomeMessage(self, message):
        self.view.updateTextArea(message)

    def setUniverse(self, universe):
        self.universe = universe
        self.universe.engine = self

    def updateLocalTimes(self, startTime):
        """
        Iterate through all the worlds, and update their current times bassed
        on their time or calendar class settings.

        @param timePassed: time in microseconds that have passed since the last
            update.
        """
        timePassed = DateTime.now() - startTime
        for world in self.universe.worlds:
            oldTime = world.getWorldTime().time or startTime
            newTime = oldTime.fromSeconds(
                oldTime.asSeconds() + (timePassed * self.gameSpeed))
            world.setWorldTime(newTime)

    def wait(self, startTicks):
        """
        Calculate the total time taken since the given start time, subtract
        that from the minimum time we're supposed to wait, and continue to wait
        for the remainder.
        """
        endTicks = pygame.time.get_ticks()
        thisLoopTicks = endTicks - startTicks
        ticksLeft = self.ticksLimit - thisLoopTicks
        if ticksLeft > 0:
            pygame.time.wait(ticksLeft)
        else:
            ticksLeft = 0
        self.gametime.updateTime()

    def run(self):
        """
        Starts the Isomyr Engine.

        @attrib quit: returns 1 for window close or ctrl-c, and 2 for game
            quit: integer
        """
        player = self.universe.getPlayer()
        self.view.updateInventory(player)
        quit = False
        while not quit:
            # Record the start time of the loop for the frame time control
            # XXX  Maybe put this in gametime class?
            startTicks = pygame.time.get_ticks()
            startTime = DateTime.now()

            # Check the players control events.
            quit = self.playerControl(
                player.scene.objectList, self.view.getSurface(), player)
            # Note: It is very important that objects modify their location or
            # the object lists in their tick routines. Modifying these values
            # in event receiver routines will mean that often a necessary
            # collision detection has not occurred.
            #
            # Update the movement of the objects in the players scene.
            self.responder.update(player.scene)
            # Update the isometric display.
            self.view.updateScene()
            # If there's any time left to wait between now and the next frame,
            # do so.
            self.wait(startTicks)
            self.updateLocalTimes(startTime)
            #print self.universe.worlds[0].getWorldTime()
        return quit

    def playerControl(self, objectList, surface, player):
        """
        Checks for key presses and quit events from the player.

        objectList: The group of objects in the players scene: list of
            object_3d class or subclass
        player: The avatar being used for the player: Avatar class
        surface: The area of the surface to draw into from the pygame window:
            surface class

        kquit: returns 1 if quit event occurs: integer
        """
        # Check movement keys based on direct access to the keyboard state.
        keys = pygame.key.get_pressed()
        # XXX Maybe put this in an event handler too...
        # Checks for the direction keys: up down left right.
        if (keys[self.keys.up] is 1 or
            keys[self.keys.down] is 1 or
            keys[self.keys.left] is 1 or
            keys[self.keys.right] is 1):
            if keys[self.keys.up] is 1:
                player.updatePosition([-1 * player.velocityModifier, 0, 0])
            if keys[self.keys.down] is 1:
                player.updatePosition([1 * player.velocityModifier, 0, 0])
            if keys[self.keys.left] is 1:
                player.updatePosition([0, 1 * player.velocityModifier, 0])
            if keys[self.keys.right] is 1:
                player.updatePosition([0, -1 * player.velocityModifier, 0])
        # If no direction key is pressed then stop the player.
        else:
            player.stop()
        # Check for the Jump key.
        if keys[self.keys.jump] is 1:
            player.jump()
        kquit = 0

        # Check other keys and window close/QUIT based on the event queue
        # system.
        for event in pygame.event.get():
            # Check for a quit program action caused by the window close and
            # Control-C keypress.
            if event.type is pygame.QUIT:
                kquit = 1
            # XXX Add a "keydown" function that all this logic can live in.
            # Check for a quit game action.
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                kquit = 2
            # XXX Add an event for the logic entailed here in the examine
            # check.
            # Check for the examine key.
            elif (event.type is pygame.KEYDOWN and
                event.key == self.keys.examine):
                # If the player is carrying an object then show its examine
                # images.
                is_examinable = isinstance(
                    player.inventory[player.using],
                    ExaminableSkin)
                if len(player.inventory) > 0 and is_examinable:
                     self.examine(objectList, player, surface)
            # Check for pick up key.
            elif (event.type is pygame.KEYDOWN and
                  event.key == self.keys.pick_up):
                notify(PlayerPickUpItemEvent(player))
            # Check for the drop key.
            elif event.type is pygame.KEYDOWN and event.key == self.keys.drop:
                notify(PlayerDropItemEvent(player))
            # Check for the using key.
            elif event.type is pygame.KEYDOWN and event.key == self.keys.using:
                if len(player.inventory) > 0:
                    item = player.inventory[player.using]
                    notify(PlayerUsingItemEvent(item, player))
        return kquit

    # XXX Move this out of the engine and into a suitably abstracted perception
    # object, or player-environment interaction object.
    def examine(self, objectList, player, surface):
        """
        Displays the examine images for the object that the player is using.

        objectList: The group of objects in the players scene: list of
            object_3d class or subclass
        player: The avatar being used for the player: Avatar class
        surface: The area of the surface to draw into from the pygame window:
            surface class

        Note: examine freezes the game and returns control when the player
        presses the examine key again
        """
        # Get the object number that we are using
        using = player.using
        quit = False
        image = 0
        # Display the examine images in sequence every keypress. If the player
        # presses the examine key then exit.
        while not quit:
            # Display the image.
            examine_image = player.inventory[using].examine_image
            examine_sprite = pygame.sprite.Sprite()
            examine_sprite.image = examine_image
            examine_sprite.rect = examine_sprite.image.get_rect()
            examine_sprite.rect.top = (
                surface.get_rect().height / 2 - examine_sprite.rect.height / 2)
            examine_sprite.rect.left = (
                surface.get_rect().width / 2 - examine_sprite.rect.width / 2)
            surface.blit(examine_sprite.image, examine_sprite.rect)
            pygame.display.flip()
            # Check for a keypress.
            done = False
            while not done:
                for event in pygame.event.get():
                    if (event.type == pygame.KEYDOWN ):
                        if (event.key == self.keys.examine):
                            quit = True
                        done = True
            image = (image + 1) % len(
                player.inventory[using].examine_image)
        # Clean up the surface and return to the main game.
        self.view.redrawDisplay(player.scene)
        self.draw_info_panel(surface, player)
