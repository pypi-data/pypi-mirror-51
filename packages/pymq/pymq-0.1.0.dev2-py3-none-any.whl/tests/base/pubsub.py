import abc
import queue
import threading
import time
from typing import NamedTuple

import pymq


class SimpleEvent:
    pass


class Payload(NamedTuple):
    name: str
    value: int


class EventWithPayload:
    payload: Payload

    def __init__(self, payload: Payload) -> None:
        self.payload = payload


class StatefulListener:
    invocations: queue.Queue

    def __init__(self) -> None:
        super().__init__()
        self.invocations = queue.Queue()

        pymq.add_listener(self.typed_stateful_event_listener)
        pymq.add_listener(self.stateful_event_listener, 'some/channel')

    def typed_stateful_event_listener(self, event: SimpleEvent):
        self.invocations.put(('typed_stateful_event_listener', event))

    def stateful_event_listener(self, event):
        self.invocations.put(('stateful_event_listener', event))


# noinspection PyUnresolvedReferences
class AbstractPubSubTest(abc.ABC):

    def test_stateful_event_listener(self):
        listener = StatefulListener()

        pymq.publish('hello', channel='some/channel')

        title, e = listener.invocations.get(timeout=2)
        self.assertEquals('stateful_event_listener', title)
        self.assertEquals('hello', e)

        self.assertTrue(listener.invocations.empty())

    def test_typed_stateful_event_listener(self):
        listener = StatefulListener()

        event = SimpleEvent()
        pymq.publish(event)

        title, e = listener.invocations.get(timeout=2)
        self.assertEquals('typed_stateful_event_listener', title)
        self.assertIsInstance(e, SimpleEvent)

        self.assertTrue(listener.invocations.empty())

    def test_remove_typed_listener_is_never_called(self):
        called = threading.Event()

        def listener(event: SimpleEvent):
            called.set()

        pymq.add_listener(listener)
        pymq.remove_listener(listener)
        pymq.publish(SimpleEvent())

        time.sleep(0.25)
        self.assertFalse(called.is_set())

    def test_publish_on_exposed_listener_with_channel(self):
        invocations = queue.Queue()

        @pymq.listener('some/channel')
        def listener(event):
            invocations.put(event)

        pymq.publish('hello', channel='some/channel')
        self.assertEqual('hello', invocations.get(timeout=1))
        self.assertTrue(invocations.empty())

    def test_publish_on_exposed_listener_with_type(self):
        invocations = queue.Queue()

        @pymq.listener
        def listener(event: SimpleEvent):
            invocations.put(event)

        pymq.publish(SimpleEvent())
        pymq.publish(SimpleEvent())
        self.assertIsInstance(invocations.get(timeout=1), SimpleEvent)
        self.assertIsInstance(invocations.get(timeout=1), SimpleEvent)
        self.assertTrue(invocations.empty())

    def test_publish_on_same_channel(self):
        invocations = queue.Queue()

        @pymq.listener('some/channel')
        def listener(event):
            invocations.put(event)

        pymq.publish('hello1', channel='some/channel')
        pymq.publish('hello2', channel='some/channel')
        pymq.publish('hello3', channel='some/non-existing/channel')
        self.assertEqual('hello1', invocations.get(timeout=1))
        self.assertEqual('hello2', invocations.get(timeout=1))
        self.assertTrue(invocations.empty())

    def test_publish_on_channel_routes_correctly(self):
        invocations1 = queue.Queue()
        invocations2 = queue.Queue()

        @pymq.listener('channel/1')
        def listener1(event):
            invocations1.put(event)

        @pymq.listener('channel/2')
        def listener(event):
            invocations2.put(event)

        pymq.publish('event1', channel='channel/1')
        pymq.publish('event2', channel='channel/2')

        self.assertEqual('event1', invocations1.get(timeout=1))
        self.assertEqual('event2', invocations2.get(timeout=1))
        self.assertTrue(invocations1.empty())
        self.assertTrue(invocations2.empty())

    def test_event_serialization(self):
        called = threading.Event()

        def listener(event: EventWithPayload):
            called.payload = event.payload
            called.set()

        pymq.add_listener(listener)
        pymq.publish(EventWithPayload(Payload('foobar', 42)))

        self.assertTrue(called.wait(2))
        self.assertIsInstance(called.payload, Payload)
        self.assertEqual('foobar', called.payload.name)
        self.assertEqual(42, called.payload.value)

    def test_publish_pattern(self):
        invocations = queue.Queue()

        @pymq.listener('channel/*', True)
        def listener1(event):
            invocations.put(event)

        pymq.publish('event1', channel='channel/1')
        pymq.publish('event2', channel='channel/2')

        self.assertEqual('event1', invocations.get(timeout=1))
        self.assertEqual('event2', invocations.get(timeout=1))
        self.assertTrue(invocations.empty())
