import pygame

from isomyr import isometric, sprites


class GUIComponent(object):
    """
    This is intended to be used as a base class, inherited by view components
    that need to have access to the parent view and refresh portions of the
    display.
    """
    def __init__(self, parent=None):
        self.parent = parent

    def updateDisplay(self, rect):
        pygame.display.update(rect)


class TitleView(GUIComponent):
    """
    The view that is responsible for renderingn the title area of the game.
    """
    def __init__(self, *args):
        super(TitleView, self).__init__(*args)
        self.loadTitleSprite()

    def loadTitleSprite(self):
        """
        Load the titlebar graphic as a sprite for drawing later. Users can
        reload their own image.
        """
        self.titleSprite = pygame.sprite.Sprite()
        self.titleSprite.image = pygame.image.load(self.parent.titleFile)
        self.titleSprite.rect = self.titleSprite.image.get_rect()

    def updateDisplay(self):
        surface = self.parent.getSurface()
        rect = surface.blit(self.titleSprite.image, self.titleSprite.rect)
        super(TitleView, self).updateDisplay(rect)


class SceneView(GUIComponent):
    """
    Draws a scene in an isometric view.
    """

    def updateRectangle(self, spriteRect):
        self.parent.changedRectangles = range(len(spriteRect))
        # XXX what's up here? this probably needs to be refactored
        for index in range(len(spriteRect)):
            self.parent.changedRectangles[index] = spriteRect[index]

    def overlayRectangles(self):
        if len(self.parent.changedRectangles) > 0:
            background = self.parent.scene.skin.getImage()
            for clearRect in self.parent.changedRectangles:
                # pygame.Surface.blit: Draw one image onto another.
                self.parent.getSurface().blit(
                    background.subsurface(clearRect), clearRect)

    def updateDisplay(self):
        """
        Updates the isometric display using update rectangles.
        """
        # Clear the old sprite location with the background.
        scene = self.parent.scene
        background = scene.skin.getImage()
        self.overlayRectangles()
        # Draw the isometric view in the display surface.
        spriteRect = isometric.viewDraw(
            scene.world.getSurface(), scene.getUpdatableObjects(),
            self.parent.displayOffset)
        # Combines the rectangles that need updating: the new sprites and the
        # old background rectangles.
        updateRect = sprites.combine_rectangles(
            spriteRect, self.parent.changedRectangles)
        # Update portions of the computer screen.
        # XXX not sure if this should be here or in the View class...
        pygame.display.update(updateRect)
        # Remember the sprite rectangles.
        self.updateRectangle(spriteRect)

    def redrawDisplay(self):
        """
        Redraws the entire display, including background.
        """
        # Display the background (pygame.Surface.blit: Draw one image onto
        # another).
        scene = self.parent.scene
        scene.world.getSurface().blit(
            scene.skin.getImage(),
            scene.skin.getImage().get_rect())
        # Update the full diplay surface to the computer screen.
        # XXX maybe this should not be called here, but instead in the
        # top-level view class...
        pygame.display.flip()
        self.updateDisplay()


class InventoryView(GUIComponent):

    def updateDisplay(self, player):
        """
        Draws the information panel on the surface.

        @param surface: The area of the surface to draw into from the pygame
            window: surface class
        param player: The avatar being used for the player: Avatar class
        """
        surface = self.parent.getSurface()
        # XXX Define rectagle area for inventory (see TitleView for an
        # example); for now, we're just going to use the title area for
        # inventory.
        titleSprite = self.parent.getView(TitleView).titleSprite
        rect = surface.blit(titleSprite.image, titleSprite.rect)
        if len(player.inventory) > 0:
            sprite_group = sprites.update_images(player.inventory)
            p = 175
            draw_order = (range(player.using, len(player.inventory)) +
                          range(player.using))
            for i in draw_order:
                sprite_group[i].rect.left = p
                sprite_group[i].rect.top = 38 - sprite_group[i].rect.height
                surface.blit(sprite_group[i].image, sprite_group[i].rect)
                text = self.parent.font.render(
                    player.inventory[i].name, 1,
                    (255, 255, 255))
                textpos = text.get_rect()
                textpos.left = (
                    p - len(player.inventory[i].name) * 3 +
                    sprite_group[i].rect.width / 2)
                textpos.top = 35
                surface.blit(text, textpos)
                p = p + sprite_group[i].rect.width + 20
        # Update the display with the panel changes.
        super(InventoryView, self).updateDisplay(rect)
