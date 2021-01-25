import pygame


#class sprite_group:
#    def __init__(self, dimension):
#        self.num_sprites = dimension
#        self.sprites = range(dimension)

def update_images(object_group):
    """Updates all the images for every object.

    object_group: the objects whose state will be analysed to find the right
        image: list of objects_3d or subclass
    Returns sprite_group : sprite_group: a list of sprites which hold the new
        images: list of sprites 
    """
    sprite_group = []
    for obj in object_group:
        sprite = pygame.sprite.Sprite()
        sprite.image = obj.skin.getImage()
        sprite.rect = sprite.image.get_rect()
        sprite_group.append(sprite)
    return sprite_group

def ordered_draw(sprite_group, iso_draw_order, surface):
    """
    Draws the sprites to the surface and returns a rect list for surface
    update.

    sprite_group: a list of sprites which will be plotted on the surface: list
        of sprites
    order: an array of the object numbers in depth order: list of integers
    surface: The pygame display area to be drawn into: surface
    Returns rect: a list of drawn rectangles for updating : list of rect
    """
    # XXX This seems kind of convoluted. What about an empty list and appending
    # to it?
    rect = range(len(sprite_group))
    for sp in range(len(sprite_group)):
        rect[sp] = surface.blit(
            sprite_group[iso_draw_order[sp]].image,
            sprite_group[iso_draw_order[sp]].rect)
    return rect


def combine_rectangles(sprite_rect, old_rect):
    """
    Combine the old sprite rectangles with the new sprite rectangles and update
    those rectangles.

    Sprite_rect: the list of new sprite rectangles : list of rect old_rect: the
    list of old rectangles for updating : list of rect Returns update_rect: the
    combined list of rectangles : list of rect

    The function ensures that if a new object appears or disappears then the
    old rectangles or new sprites are included in the update and no dirty lines
    are left on the display.
    """

    # Case of the rectangle lists being the same length
    if len(old_rect)>0 and len(old_rect) == len(sprite_rect):
        update_rect = range(len(sprite_rect))
        for rect in range(len(sprite_rect)):
            update_rect[rect] = sprite_rect[rect].union(old_rect[rect])
    # Case of the old rectangle list is bigger than the sprite rectangle list          
    elif len(old_rect) > 0 and len(old_rect) > len(sprite_rect):
        update_rect = range(len(sprite_rect))
        for rect in range(len(sprite_rect)):
            update_rect[rect] = sprite_rect[rect].union(old_rect[rect])
        for rect in range(len(sprite_rect), len(old_rect)):
            update_rect.append(old_rect[rect])
    # Case of the old rectangle list is smaller than the sprite rectangle list 
    elif len(old_rect) > 0 and len(old_rect) < len(sprite_rect):
        update_rect = range(len(old_rect))
        for rect in range(len(old_rect)):
            update_rect[rect] = sprite_rect[rect].union(old_rect[rect])
        for rect in range(len(old_rect), len(sprite_rect)):
            update_rect.append(sprite_rect[rect])
    else:
        update_rect = sprite_rect
    return(update_rect)
