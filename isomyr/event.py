from isomyr.exceptions import EventSubscriberNotFound


# The event subscribers is a list of functions and/or methods that will be
# called whenever notify is called.
subscribers = {}


def subscribe(*args):
    """
    @param args: either a list of (function, eventClass) tuples or a function
        and eventClass.

        function: the subscribing function that will be called by C{notify}.
        eventClass: the event class that, instances of which the subscriber
            function is interested in.
    """
    if len(args) == 1 and isinstance(args[0], list):
        handlerEventPairs = args[0]
    else:
        function, eventClass = args
        handlerEventPairs = [(function, eventClass)]
    for function, eventClass in handlerEventPairs:
        subscribers.setdefault(eventClass, [])
        subscribers[eventClass].append(function)


def unsubscribe(function, eventClass):
    index = subscribers[eventClass].index(function)
    del subscribers[eventClass][index]


def notify(event):
    """
    The notify function takes a single parameter, an event. Subscribers are
    functions which should know what to do when they are executed with the
    event parameter.

    @param event: an arbitrary event object.
    """
    eventSubscribers = subscribers.get(event.__class__)
    if not eventSubscribers:
        raise EventSubscriberNotFound
    for subscriber in eventSubscribers:
        subscriber(event)


class IsomyrEvent(object):
    """
    A base class for events in Isomyr.

    Event objects are an abstraction that act as a link between two objects
    whose attributes are needed to perform some action in response to an event,
    but whose attribute are not necessarily functionally related (and thus not
    something that can be placed in a single object.

    By having an event object, all the data that is necessary in order to
    complete an event reaction (i.e., handle the event) may be assigned as
    various attributes to the event object itself. Seeing that the event object
    is passed to the handler, the handler will then have access to all the data
    it needs in order to execute its particular response.

    When subclassing the IsomyrEvent object, one should keep this in mind and
    add as attributes only that data which is needed by the handler.
    """


class PlayerTouchPortalEvent(IsomyrEvent):
    """
    An event for when the player moves from one scene to another.

    @param player: the object representing the player in the game.
    @param portal: the object the player touched which initiated the scene
        change.
    """
    def __init__(self, player, portal):
        self.player = player
        self.lastScene = player.scene
        self.newScene = portal.toScene
        self.lastLocation = player.location
        self.newLocation = portal.toLocation


class PlayerEvent(IsomyrEvent):
    """
    A base class for player events.
    """
    def __init__(self, player):
        self.player = player


class PlayerInventoryUpdateEvent(PlayerEvent):
    """
    An event for when the player picks something up or puts it down.

    @param player: the object representing the player in the game.
    """


class PlayerUsingItemEvent(PlayerEvent):
    """
    An event for when the player uses something in the inventory.

    @param player: the object representing the player in the game.

    We subclass the PlayerInventoryUpdateEvent here (instead of just using that
    event with a new handler) because we care about the order of execution. We
    want to be sure that The "use" event happens first, so that the inventory
    display gets updated after the inventory item swap has occurred.

    If the order didn't matter, we'd instead have two subscribers listening to
    one event.
    """
    def __init__(self, item, *args):
        self.item = item
        super(PlayerUsingItemEvent, self).__init__(*args)


class PlayerPickUpItemEvent(PlayerEvent):
    """
    An event for when the player picks an item up.
    """


class PlayerDropItemEvent(PlayerEvent):
    """
    An event for when the player picks an item up.
    """


class TimeEvent(IsomyrEvent):

    def __init__(self, player, calendar):
        self.player = player
        self.calendar = calendar

    def getMessage(self):
        raise NotImplementedError


class TimeScaleEvent(TimeEvent):
    """
    A base event class for time scale changes.
    """


class TimeChangeEvent(TimeEvent):
    """
    A base event class for events that depend upon a particular time change.
    """


class HourChangeEvent(TimeChangeEvent):
    """
    An event for changes to the hour.
    """


class SeasonChangeEvents(TimeChangeEvent):
    """
    An event for changes in the seasons.
    """
