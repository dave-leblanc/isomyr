import pygame

from isomyr.gui.component import (
    TitleView, SceneView, InventoryView)
from isomyr.gui.textarea import TextAreaView


class View(object):

    def __init__(self, displayOffset, sceneSize=(400, 360),
                 titleFile="", font=None, titleView=None, sceneView=None,
                 inventoryView=None, textAreaView=None,
                 textAreaSize=(100, 300), textAreaPosition=(0, 400)):
        self.scene = None
        # Offset from the top left corner of the window for the isomyr
        # display.
        self.displayOffset = displayOffset
        self.sceneSize = sceneSize
        self.surface = pygame.display.set_mode(self.sceneSize)
        self.viewSize = self.getSurface().get_size()
        self.titleFile = titleFile
        self.font = font
        self.views = []
        self.changedRectangles = []
        self.loadFont(font)
        self.textAreaSize = textAreaSize
        self.textAreaPosition = textAreaPosition
        self.initializeViews(
            titleView=titleView, sceneView=sceneView,
            inventoryView=inventoryView, textAreaView=textAreaView)

    def initializeViews(self, titleView, sceneView, inventoryView,
                        textAreaView):
        if not titleView:
            titleView = TitleView(self)
        if not sceneView:
            sceneView = SceneView(self)
        if not inventoryView:
            inventoryView = InventoryView(self)
        if not textAreaView:
            textAreaRectangle = pygame.Rect(
                self.textAreaPosition + self.textAreaSize)
            textAreaView = TextAreaView(
                parent=self, rectangle=textAreaRectangle)
        for view in [titleView, sceneView, inventoryView, textAreaView]:
            self.views.append(view)

    def getView(self, viewType):
        for viewInstance in self.views:
            if isinstance(viewInstance, viewType):
                return viewInstance

    def getSurface(self):
        return self.surface

    def loadFont(self, font):
        """
        Load the default font.
        """
        if not font:
            self.font = pygame.font.SysFont(
                "bitstreamverasansmono", 10, bold=False, italic=False)
        else:
            self.font = font

    def setScene(self, scene, prelude="", text=""):
        self.scene = scene
        if prelude:
            text = "%s\n\n%s" % (prelude, text)
        self.redrawDisplay(text=text)

    def updateTitle(self):
        self.getView(TitleView).updateDisplay()

    def updateScene(self):
        self.getView(SceneView).updateDisplay()

    def updateInventory(self, player):
        self.getView(InventoryView).updateDisplay(player)

    def updateTextArea(self, text=""):
        self.getView(TextAreaView).updateDisplay(text)

    def updateDisplay(self, text=""):
        # XXX seems we don't need this... why?
        #self.updateTitle()
        self.updateScene()
        self.updateInventory(self.scene.world.player)
        # XXX not sure if this is actually necessary
        self.updateTextArea(text)

    def redrawDisplay(self, text=""):
        self.scene.setView(self)
        # XXX seems we don't need this... why?
        #self.updateTitle()
        self.getView(SceneView).redrawDisplay()
        self.updateInventory(self.scene.world.player)
        # XXX not sure if this is actually necessary
        self.updateTextArea(text)
