class RelationshipMixin(object):

    def __init__(self, name=""):
        self.children = []
        self.name = name
        self.parent = None

    def __repr__(self):
        return "<%s object %s>" % (self.__class__.__name__, self.name)

    def addChild(self, child):
        """
        This class is indended to be used by child object when they set their
        parent object.
        """
        if child in self.children:
            return
        self.children.append(child)
        child.setParent(self)

    def removeChild(self, child):
        pass

    def setParent(self, parent):
        """
        This is intended to be used by objects that contain an instance of this
        object.
        """
        self.parent = parent
        if self in parent.children:
            return
        self.parent.addChild(self)

    def removeParent(self, parent):
        pass
