from unittest import TestCase

from isomyr import event
from isomyr import handler


class FakeEvent1(event.IsomyrEvent):

    def __init__(self, name, responses):
        self.name = name
        self.responses = responses

class FakeEvent2(event.IsomyrEvent):

    def __init__(self, name, responses):
        self.name = name
        self.responses = responses

class FakeSubscriber1(handler.IsomyrSubscriber):

    def onNotice(self, event):
        event.responses.append("sub1 got %s" % event.name)


class FakeSubscriber2(handler.IsomyrSubscriber):

    def onNotice(self, event):
        event.responses.append("sub2 got %s" % event.name)


class SubscriberTestCase(TestCase):

    def setUp(self):

        class Subscriber(handler.IsomyrSubscriber):

            def onNotice(self, event):
                self.event = event

        self.subscriber = Subscriber()

    def test_onNotice(self):
        self.subscriber.onNotice("my event")
        self.assertEquals(self.subscriber.event, "my event")

    def test_call(self):
        self.subscriber("my event")
        self.assertEquals(self.subscriber.event, "my event")


class MultipleSubscriberTestCase(TestCase):

    def setUp(self):
        # Clear out the subscribers that are defined in the handler module.
        event.subscribers = {}
        self.notificationResponses = []
        event.subscribe([
            (FakeSubscriber1(), FakeEvent1),
            (FakeSubscriber2(), FakeEvent2),
            ])

    def tearDown(self):
        """
        Clear out the subscribers that have been added by the test.
        """
        event.subscribers = {}

    def test_event1(self):
        """
        Make sure that when event1 notifies its subscribers, only the
        subscibers get the message.
        """
        event.notify(FakeEvent1("evt1", self.notificationResponses))
        self.assertEquals(self.notificationResponses, ["sub1 got evt1"])

    def test_event2(self):
        """
        Make sure that when event2 notifies its subscribers, only the
        subscibers get the message.
        """
        event.notify(FakeEvent2("evt2", self.notificationResponses))
        self.assertEquals(self.notificationResponses, ["sub2 got evt2"])
