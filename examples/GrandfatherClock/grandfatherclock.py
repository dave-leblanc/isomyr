import os

from pygame import (K_DOWN, K_LEFT, K_RETURN,
                    K_RIGHT, K_SPACE, K_UP, K_l, K_x, K_z)

from isomyr.config import Keys
from isomyr.engine import Engine
from isomyr.event import HourChangeEvent
from isomyr.handler import HourChangeSubscriber
from isomyr.objects.portal import Portal
from isomyr.skin import AnimatedSkin, DirectedAnimatedSkin, Skin
from isomyr.util.loaders import ImageLoader
from isomyr.thing import MovableThing, PhysicalThing, PortableThing
from isomyr.world.calendar import SPEED_04, TimeChange
from isomyr.world.world import worldFactory


dirname = os.path.dirname(__file__)


# Set the custom keys for the game.
custom_keys = Keys(
    left=K_LEFT,
    right=K_RIGHT,
    up=K_UP,
    down=K_DOWN,
    jump=K_SPACE,
    pick_up=K_z,
    drop=K_x,
    examine=K_l,
    using=K_RETURN)


# An image loader that lets us run the tutorial anywhere the isomyr library
# can be imported (i.e., you don"t have to be in the same directory as the
# tutorial to run it).
imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))


class GrandfatherClockBong(HourChangeEvent):
    """
    A custom event class for the grandfather clock in this example.
    """
    def getMessage(self, hour):
        count = hour % 12
        prelude = ("\nYou hear the gears switch in the grandfather clock and "
                   "then an ominous pause...\n\n")
        emote = "*BONG* " * count
        sound = "chimes stop"
        if count == 1:
            sound = "chime stops"
        postlude = ("\n\nSlowly, after the %s %s echoing around "
                    "the room, the ringing in your ears fades. You find "
                    "the silence deafening." % (count, sound))
        return prelude + emote + postlude


def setupWorld():
    """
    Create the world, the scenes that can be visited, the objects in the
    scenes, and the player.
    """
    # Create the world.
    world = worldFactory(name="Clock World")

    # Create the scene.
    livingRoom = world.addScene("The Living Room")
    livingRoom.setSkin(
        Skin(imageLoader.load("livingroom.png")))

    # Create the player and set his animated skin.
    ian_curtis = livingRoom.addPlayer(
        name="Ian Curtis", location=[90, 90, 100], size=[14, 14, 50],
        velocityModifier=3)
    south_facing = imageLoader.load([
        "player/ian_curtis1.png", "player/ian_curtis2.png",
        "player/ian_curtis3.png"])
    east_facing = imageLoader.load([
        "player/ian_curtis4.png", "player/ian_curtis5.png",
        "player/ian_curtis6.png"])
    ian_curtis.setSkin(
        DirectedAnimatedSkin(south_facing, east_facing,
                             frameSequence=[0, 2, 2, 1, 1, 2, 2, 0]))

    # Put in ground and walls.
    ground = PhysicalThing(
        "ground", [-1000, -1000, -100], [2000, 2000, 100])
    wall0 = PhysicalThing("wall", [180, 0, -20], [20, 180, 120])
    wall1 = PhysicalThing("wall", [0, 180, -20], [180, 20, 120])
    wall2 = PhysicalThing("wall", [0, -20, -20], [180, 20, 120])
    wall3 = PhysicalThing("wall", [-20, 0, -20], [20, 180, 120])

    sofa = PhysicalThing(
        name="sofa", location=[20, 90, 0], size=[39, 66, 37], fixed=False)
    sofa.setSkin(
        Skin(imageLoader.load(["sofa.png"])))

    clock = PhysicalThing(
        name="grandfather clock", location=[90, 0, 0], size=[14, 14, 50])
    # XXX add support for sequence ordering like for directed animated skins
    clock.setSkin(AnimatedSkin(imageLoader.load([
        "clock/1.png", "clock/2.png", "clock/2.png", "clock/3.png",
        "clock/3.png", "clock/3.png", "clock/4.png", "clock/4.png",
        "clock/1.png", "clock/5.png", "clock/5.png", "clock/6.png",
        "clock/6.png", "clock/6.png", "clock/7.png", "clock/7.png",
        "clock/1.png",
        ])))

    # Populate the living room.
    livingRoom.addObjects([
        ground, wall0, wall1, wall2, wall3, sofa, clock,
        ])

    return world


def run():
    # Create an isomyr engine and start it.
    titlebar = os.path.join(dirname, "titlebar.png")
    engine = Engine(keys=custom_keys, gameSpeed=SPEED_04,
                    displayOffset=[200, 172], sceneSize=(400, 600),
                    titleFile=titlebar, textAreaPosition=(10, 380),
                    textAreaSize=(380, 230))
    engine.setStartingWorld(setupWorld(), welcomeMessage="Welcome to Isomyr!")
    time = engine.world.getWorldTime()
    time.setTimeEvent(
        TimeChange.hour, GrandfatherClockBong, HourChangeSubscriber())
    engine.run()


if __name__ == "__main__":
    run()
