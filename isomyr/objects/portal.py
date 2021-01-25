from isomyr.event import PlayerTouchPortalEvent, notify
from isomyr.objects.character import Player
from isomyr.thing import PhysicalThing


class Portal(PhysicalThing):
    """
    An object which can signal to lead actors for a scene change if they touch
    the portal.
    """
    def __init__(self, toScene=None, toLocation=None, *args, **kwds):
        super(Portal, self).__init__(*args, **kwds)
        self.toScene = toScene or self.scene
        self.toLocation = toLocation or [0, 0, 0]

    def eventTouch(self, impact, otherObject, impactSide):
        if isinstance(otherObject, Player):
            notify(PlayerTouchPortalEvent(otherObject, self))
