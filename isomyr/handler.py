from isomyr import event


class IsomyrSubscriber(object):
    """
    A callable subscriber object intented to be used to respond to event
    notifications.

    There are two objects that interact in order to complete world events in
    Isomyr: an event object and the event's subscriber, the subscriber object.
    The subscriber is responsible for reacting to the event; the event object
    makes sure that the subsciber object has all the data in needs in order to
    react.

    See the docstring for isomyr.event.IsomyrEvent for more information.
    """

    def __call__(self, event):
        self.onNotice(event)

    def onNotice(self, event):
        raise NotImplementedError


class PlayerTouchPortalSubscriber(IsomyrSubscriber):
    """
    Event handler for a change scene, usually asked by doors who touched the
    player.
    """
    def onNotice(self, event):
        player = event.player
        scene = event.newScene
        event.newScene.addPlayer(event.player)
        # XXX Do we need to remove the player from the last scene?
        #event.lastScene.removePlayer(event.player)
        # XXX This whole last scene/location and current scene/location thing
        # needs to be cleaned up... maybe Memory class, MovementMemory
        # subclass? player.movementMemory would have last location, current
        # location, last scene, current scene... movementMemory.move(to, from)
        player.last_scene = event.lastScene
        player.scene = event.newScene
        player.current_scene = scene
        player.last_location = event.lastLocation
        player.location = event.newLocation
        player.current_location = event.newLocation
        # Update the view.
        scene.setView(player.last_scene.view)
        scene.view.setScene(event.newScene)
        text = ""
        if scene.name:
            text = "You are in '%s'." % scene.name
        scene.view.redrawDisplay(text=text)


class PlayerInventoryUpdateSubscriber(IsomyrSubscriber):
    """
    Event handler for an inventory change event.
    """
    def onNotice(self, event):
        player = event.player
        view = player.scene.view
        view.updateInventory(player)


class PlayerUsingItemSubscriber(PlayerInventoryUpdateSubscriber):
    """
    Event handler for an inventory item being used.
    """
    def onNotice(self, event):
        player = event.player
        item = event.item
        text = item.text.used
        if not text:
            text = "You are using the %s." % item.name
        if len(player.inventory) > 0:
            player.using = (player.using + 1) % len(player.inventory)
        super(PlayerUsingItemSubscriber, self).onNotice(event)
        player.getView().updateTextArea(text=text)
 

class PlayerPickUpItemSubscriber(PlayerInventoryUpdateSubscriber):
    """
    Event handler for when a player picks up an item.
    """
    def onNotice(self, event):
        item = event.player.pickUp()
        text = ""
        if item:
            text = item.text.pickedUp
            if not text:
                text = "You picked up the %s." % item.name
        super(PlayerPickUpItemSubscriber, self).onNotice(event)
        event.player.getView().updateTextArea(text=text)


class PlayerDropItemSubscriber(PlayerInventoryUpdateSubscriber):
    """
    Event handler for when a player drops an item.
    """
    def onNotice(self, event):
        item = event.player.drop()
        text = ""
        if item:
            text = item.text.dropped
            if not text:
                text = "You dropped up the %s." % item.name
        super(PlayerDropItemSubscriber, self).onNotice(event)
        event.player.getView().updateTextArea(text=text)


class TimeChangeSubscriber(IsomyrSubscriber):
    pass


class HourChangeSubscriber(TimeChangeSubscriber):

    def onNotice(self, event):
        hour = event.calendar.time.hours
        text = event.getMessage(hour)
        if not text:
            text = "It is now %s o'clock." % hour
        event.player.getView().updateTextArea(text=text)


class SeasonChangeSubscriber(TimeChangeSubscriber):

    def onNotice(self, event):
        pass


def registerEventHandlers():
    event.subscribe([
        # Player event subscriptions.
        (PlayerTouchPortalSubscriber(), event.PlayerTouchPortalEvent),
        (PlayerInventoryUpdateSubscriber(), event.PlayerInventoryUpdateEvent),
        (PlayerUsingItemSubscriber(), event.PlayerUsingItemEvent),
        (PlayerPickUpItemSubscriber(), event.PlayerPickUpItemEvent),
        (PlayerDropItemSubscriber(), event.PlayerDropItemEvent),
        ])
