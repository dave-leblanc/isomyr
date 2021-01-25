from isomyr import sprites
from isomyr.util.vector import addVectors


def newTransform(coord, offset):
    pass


def transform(coord, offset):
    """
    Transform 3d coordinates into 2d location based on the size of the
    screen and an a y offset.

    @param coord: 3 dimensional coordinate to be transformed to an isometric 2d
        coordinate: list of 3 integers [x, y, z]
    @param offset: 2 dimensional offset for the isometric coordinate: list of 2
        integers [x, y]

    Returns trans_coord: a 2d isometric coordinate: list of 2 integers [x, y]

    Note: A side effect for speed: isometric transform scales x and y values to
    1.118 times their actual value and the z scale coordinate stays as 1:
    therefore all sprites need to be drawn with this ratio.
    """
    # Transformation coordinates that are returned.
    trans_coord = [0, 0]
    # Calculate x coordinate.
    trans_coord[0] = (coord[0] - coord[1]) + offset[0]
    # Calculates y coordinate.
    trans_coord[1] = ((coord[0] + coord[1]) >> 1) - coord[2] + offset[1]
    return trans_coord


def group_transform(object_group, sprite_group, offset):
    """
    Calculate the isometric location of an object group.

    @param object_group: a list of objects for the 3d coordinates to be
        transformed: list of objects_3d or subclass
    @param sprite_group: a list of sprites which will be plotted with the
        isometric coordinates: list of sprites
    @param offset: 2d vector to add to the isometric coordinates: list of 2
        integers [x, y]

    Relies on the same scale system as transform_iso. This is important for
    matching sprite dimensions to object coordinates.
    """
    for index in range(len(sprite_group)):
        # Finds the isometric coordinate based on the objects location vector
        # and a display offset.
        location = transform(object_group[index].location, offset)
        # Put the new isometric coordinates of the current object into the
        # sprite array.
        sprite_group[index].rect.left = (
            location[0] - object_group[index].size[1])
        sprite_group[index].rect.top = (
            location[1] - object_group[index].size[2])


def order(object_group):
    """
    Sorts the objects into a depth order for drawing in the isometric view.

    @param object_group: a list of objects to be depth sorted: list of
        objects_3d or subclass

    Returns order: an array of the object numbers in depth order: list of
        integers

    Note: Under rare conditions this algorithm will not produce a perfect
    representation due to the use of single sprites for any dimension boundary
    box.  This is most obvious when 3 long objects overlap in a three way tie.
    """
    # Define the array to return with the object number in an isometric order.
    order = range(len(object_group))

    # Define front precalculate matrix.
    front = range(len(object_group))
    #for i in range(3):
    #    front[i] = range(len(object_group))

    # Precalculate the front location of each objects coordinates.
    for obj in range(len(object_group)):
        front[obj] = addVectors(
            object_group[obj].location, 
            addVectors(object_group[obj].size, [-1, -1, -1]))

    # Sort the objects, based on x then y then z of the objects being in front
    # of the other object.
    for i in range(len(object_group)):
        for j in range(len(object_group) - 1):
            for k in range(3):
                if object_group[order[j]].location[k] > front[order[j+1]][k]:
                    order[j], order[j+1] = order[j+1], order[j]
                    break
    return order

def viewDraw(view, object_group, offset):
    """ Draw the sprites to the screen based on isometric ordered sorting

    @param object_group: a list of objects to be displayed (usually only the
        objects that are visiable)
    @param offset: 2d vector to add to the isometric coordinates: list of 2
        integers [x, y]

    Returns rect: A list of pygame rectangles where the sprites were
        drawn : list of rect
    """
    # Calculate the isometric order of drawing the sprites from object
    # information
    draw_order = order(object_group)
    # Put the correct images for all the skins into a sprite group
    sprite_group = sprites.update_images(object_group)
    # Calculate the screen coordinates of the sprites from the object data
    group_transform(object_group, sprite_group, offset)
    # Draw sprites in isometric order to the screen
    return sprites.ordered_draw(sprite_group, draw_order, view)
