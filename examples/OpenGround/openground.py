import os

from pygame import (
    K_DOWN, K_LEFT, K_RETURN, K_RIGHT, K_SPACE, K_UP, K_l, K_x, K_z)

from isomyr.config import Keys
from isomyr.engine import Engine
from isomyr.objects.portal import Portal
from isomyr.skin import Skin, DirectedAnimatedSkin
from isomyr.util.loaders import ImageLoader
from isomyr.thing import PhysicalThing
from isomyr.world.world import worldFactory


dirname = os.path.dirname(__file__)


# Set the custom keys for the game
customKeys = Keys(
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
# can be imported (i.e., you don't have to be in the same directory as the
# tutorial to run it).
print dirname
imageLoader = ImageLoader(basedir=dirname, transparency=(255, 255, 255))


# Tile setup.
sliceSizeX, sliceSizeY = (348, 176)
originX, originY = (1084, 302)
tiles = [
    # column 1
    (originX - 5 * (sliceSizeX / 2), originY - sliceSizeY / 2),
    (originX - 5 * (sliceSizeX / 2), originY + sliceSizeY / 2),
    # column 2
    (originX - 2 * sliceSizeX, originY - sliceSizeY),
    (originX - 2 * sliceSizeX, originY),
    # column 3
    (originX - 3 * (sliceSizeX / 2), originY - sliceSizeY / 2),
    (originX - 3 * (sliceSizeX / 2), originY + sliceSizeY / 2),
    # column 4
    (originX - sliceSizeX, originY - sliceSizeY),
    (originX - sliceSizeX, originY),
    # column 5
    (originX - sliceSizeX / 2, originY - sliceSizeY / 2),
    (originX - sliceSizeX / 2, originY + sliceSizeY / 2),
    # column 6
    (originX, originY - sliceSizeY),
    (originX, originY),
    # column 7
    (originX + sliceSizeX / 2, originY - sliceSizeY / 2),
    (originX + sliceSizeX / 2, originY + sliceSizeY / 2),
    ]


# Map the isometric tiles to each other.
map = {
    tiles[0]: {
        "scene": None,
        "N": None, "E": tiles[2], "S": tiles[3], "W": None},
    tiles[1]: {
        "scene": None,
        "N": None, "E": tiles[3], "S": None, "W": None},
    tiles[2]: {
        "scene": None,
        "N": None, "E": None, "S": tiles[4], "W": tiles[0]},
    tiles[3]: {
        "scene": None,
        "N": tiles[0], "E": tiles[4], "S": tiles[5], "W": tiles[1]},
    tiles[4]: {
        "scene": None,
        "N": tiles[2], "E": tiles[6], "S": tiles[7], "W": tiles[3]},
    tiles[5]: {
        "scene": None,
        "N": tiles[3], "E": tiles[4], "S": None, "W": None},
    tiles[6]: {
        "scene": None,
        "N": None, "E": None, "S": tiles[8], "W": tiles[4]},
    tiles[7]: {
        "scene": None,
        "N": tiles[4], "E": tiles[8], "S": tiles[9], "W": tiles[5]},
    tiles[8]: {
        "scene": None,
        "N": tiles[6], "E": tiles[10], "S": tiles[11], "W": tiles[7]},
    tiles[9]: {
        "scene": None,
        "N": tiles[7], "E": tiles[11], "S": None, "W": None},
    tiles[10]: {
        "scene": None,
        "N": None, "E": None, "S": tiles[12], "W": tiles[8]},
    tiles[11]: {
        "scene": None,
        "N": tiles[8], "E": tiles[12], "S": tiles[13], "W": tiles[9]},
    tiles[12]: {
        "scene": None,
        "N": tiles[10], "E": None, "S": None, "W": tiles[11]},
    tiles[13]: {
        "scene": None,
        "N": tiles[11], "E": None, "S": None, "W": None}}


def loadScene(world, coords):
    name = "%sx%s" % coords
    scene = world.addScene(name)
    #filename = os.path.join(dirname, "backgrounds", "%s.png" % name)
    filename = os.path.join("backgrounds", "%s.png" % name)
    image = imageLoader.load(filename=filename)
    scene.setSkin(Skin(image))
    ground = PhysicalThing(
        "ground", [-1000, -1000, -100], [2000, 2000, 100])
    scene.addObject(ground)
    map[coords]["scene"] = scene
    return scene


def connectScene(data):
    scene = data.get("scene")
    # North boundary of open area.
    if data.get("N"):
        destination = map[data.get("N")]["scene"]
        connectionN = Portal(
            name="boundary", location=[-20, 0, -20], size=[20, 180, 120],
            toScene=destination, toLocation=[160, 90, 0])
    else:
        connectionN = PhysicalThing(
            name="boundary", location=[-20, 0, -20], size=[20, 180, 120])

    # East boundary of open area.
    if data.get("E"):
        destination = map[data.get("E")]["scene"]
        connectionE = Portal(
            name="boundary", location=[0, -20, -20], size=[180, 20, 120],
            toScene=destination, toLocation=[90, 160, 0])
    else:
        connectionE = PhysicalThing(
            name="boundary", location=[0, -20, -20], size=[180, 20, 120])

    # South boundary of open area.
    if data.get("S"):
        destination = map[data.get("S")]["scene"]
        connectionS = Portal(
            name="boundary", location=[180, 0, -20], size=[20, 180, 120],
            toScene=destination, toLocation=[20, 90, 0])
    else:
        connectionS = PhysicalThing(
            name="boundary", location=[180, 0, -20], size=[20, 180, 120])

    # West boundary of open area.
    if data.get("W"):
        destination = map[data.get("W")]["scene"]
        connectionW = Portal(
            name="boundary", location=[0, 180, -20], size=[180, 20, 120],
            toScene=destination, toLocation=[90, 20, 0])
    else:
        connectionW = PhysicalThing(
            name="boundary", location=[0, 180, -20], size=[180, 20, 120])


    # Add all the connections.
    scene.addObjects([connectionN, connectionE, connectionS, connectionW])


def connectScenes():
    for coord, data in map.items():
        connectScene(data)


def setupWorld():
    """
    Create the world, the scenes that can be visited, the objects in the
    scenes, and the player.
    """
    # Create the world.
    world = worldFactory(name="Wilderness World")
    # Create all the scenes.
    for coords in tiles:
        scene = loadScene(world, coords)
        if coords == (originX, originY):
            startScene = scene

    # Create the player and set his animated skin.
    explorer = startScene.addPlayer(
        name="Tim the Explorer", location=[90, 90, 50], size=[14, 14, 30])
    southFacing = imageLoader.load(fileGlob="explorer/south/small/*.gif")
    eastFacing = imageLoader.load(fileGlob="explorer/east/small/*.gif")
    # Mirror the images to complete the player animation.
    explorer.setSkin(
        DirectedAnimatedSkin(southFacing, eastFacing))
    connectScenes()
    return world


def run():
    # Setup the pygame display, the window caption and its icon.
    titlebar = os.path.join(dirname, "titlebar.png")
    # Create an isomyr engine and start it.
    engine = Engine(displayOffset=[202, 182], keys=customKeys,
                    titleFile=titlebar)
    engine.setStartingWorld(setupWorld(), welcomeMessage="Welcome to Isomyr!")
    engine.run()


if __name__ == "__main__":
    run()

