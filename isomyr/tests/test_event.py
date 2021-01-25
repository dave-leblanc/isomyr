from unittest import TestCase

from isomyr import event
from isomyr import handler


class FakeEvent(object):
    pass


class BasicEventTestCase(TestCase):

    def setUp(self):
        """
        Clear out the subscribers that are defined in the handler module.
        """
        event.subscribers = {}

    def tearDown(self):
        """
        Clear out the subscribers that have been added by the test.
        """
        event.subscribers = {}

    def test_subscribe(self):

        def subscriber(event):
            pass

        self.assertEquals(len(event.subscribers), 0)
        event.subscribe(subscriber, FakeEvent)
        self.assertEquals(len(event.subscribers), 1)
        self.assertEquals(event.subscribers[FakeEvent], [subscriber])

    def test_unsubscribe(self):

        def subscriber(event):
            pass

        self.assertEquals(event.subscribers.get(FakeEvent), None)
        event.subscribe(subscriber, FakeEvent)
        self.assertEquals(len(event.subscribers), 1)
        self.assertEquals(event.subscribers[FakeEvent], [subscriber])
        event.unsubscribe(subscriber, FakeEvent)
        self.assertEquals(len(event.subscribers[FakeEvent]), 0)

    def test_notification(self):

        notificationResponses = []

        class NewDataEvent(object):
            data = "some data"

        def subscriber(event):
            notificationResponses.append(event.data)

        self.assertEquals(len(event.subscribers), 0)
        self.assertEquals(len(notificationResponses), 0)
        event.subscribe(subscriber, NewDataEvent)
        self.assertEquals(len(event.subscribers), 1)
        event.notify(NewDataEvent())
        self.assertEquals(len(notificationResponses), 1)
        self.assertEquals(notificationResponses, ["some data"])
        event.notify(NewDataEvent())
        self.assertEquals(len(notificationResponses), 2)


class PlayerTouchPortalEventTestCase(TestCase):

    def setUp(self):

        class Scene(object):

            def __init__(self, name):
                self.name = name

        class Player(object):

            def __init__(self, name, scene):
                self.name = name
                self.scene = scene
                self.location = None

        class Portal(object):

            def __init__(self, toScene):
                self.toScene = toScene
                self.toLocation = None

        lastScene = Scene("scene 1")
        newScene = Scene("scene 2")
        self.player = Player("alice", lastScene)
        self.portal = Portal(newScene)

    def test_event(self):

        notificationResponses = []

        class SceneChangeMessage(handler.IsomyrSubscriber):

            def onNotice(self, event):
                msg = "%s has moved from %s to %s" % (
                    event.player.name, event.lastScene.name,
                    event.newScene.name)
                notificationResponses.append(msg)

        class UpdateView(handler.IsomyrSubscriber):

            def onNotice(self, event):
                notificationResponses.append("view updated")

        event.subscribe([
            (SceneChangeMessage(), event.PlayerTouchPortalEvent),
            (UpdateView(), event.PlayerTouchPortalEvent),
            ])
        event.notify(
            event.PlayerTouchPortalEvent(self.player, self.portal))
        self.assertEquals(
            notificationResponses,
            ["alice has moved from scene 1 to scene 2",
             "view updated"])
