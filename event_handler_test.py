import unittest
import pygame
import events
import time


class EventHandlerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    def setUp(self):
        self._results = False

    def _handler(self, an_event):
        self._results = True

    def test_handling_the_right_event(self):
        events.EventHandlerContext.addMouseButtonDownEventHandler(handlerFunction=self._handler)

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}))
        events.observeEvents()
        self.assertTrue(self._results, 'Handles the event')

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {}))
        events.observeEvents()
        self.assertFalse(self._results, 'Does not handling other events')

    def test_handling_event_without_conditions(self):
        events.EventHandlerContext.addMouseButtonDownEventHandler(handlerFunction=self._handler)

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}))
        events.observeEvents()
        self.assertTrue(self._results, 'Handles event without properties')

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': pygame.BUTTON_LEFT}))
        events.observeEvents()
        self.assertTrue(self._results, 'Handles event with properties')

    def test_handling_event_with_conditions(self):
        events.EventHandlerContext.addMouseButtonDownEventHandler(button=pygame.BUTTON_LEFT, pos=(0, 1),
                                                                  handlerFunction=self._handler)

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}))
        events.observeEvents()
        self.assertFalse(self._results, 'Do not handles event without properties')

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': pygame.BUTTON_RIGHT, 'pos': (0, 1)}))
        events.observeEvents()
        self.assertFalse(self._results, 'Do not handles event with non-matching properties')

        self._results = False
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': pygame.BUTTON_LEFT, 'pos': (0, 1)}))
        events.observeEvents()
        self.assertTrue(self._results, 'Handles event with matching properties')

    def test_handling_lot_of_subscribers(self):
        for i in range(100000):
            events.EventHandlerContext.addMouseButtonDownEventHandler(button=pygame.BUTTON_LEFT, pos=(i, 0),
                                                                      handlerFunction=self._handler)

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': pygame.BUTTON_LEFT, 'pos': (2, 0)}))

        begin = time.process_time()
        events.observeEvents()
        end = time.process_time()

        elapsed_time = end - begin
        self.assertLess(elapsed_time, 0.05)

    def test_delete_single_subscriber(self):
        events.EventHandlerContext.addMouseButtonDownEventHandler(button=pygame.BUTTON_LEFT, pos=(0, 1),
                                                                  handlerFunction=self._handler)

        self._results = False

        events.EventHandlerContext.removeEventHandlers(handlerConditions={"button": pygame.BUTTON_LEFT, "pos": (0, 1)},
                                                       eventId=pygame.MOUSEBUTTONDOWN)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {}))
        events.observeEvents()
        self.assertFalse(self._results, 'Delete single, specified handler')

    def test_delete_all_subscriber_of_eventtype(self):
        events.EventHandlerContext.addMouseButtonDownEventHandler(button=pygame.BUTTON_LEFT, handlerFunction=self._handler)

        events.EventHandlerContext.addMouseButtonDownEventHandler(button=pygame.BUTTON_RIGHT, handlerFunction=self._handler)

        events.EventHandlerContext.addMouseButtonUpEventHandler(button=pygame.BUTTON_RIGHT, handlerFunction=self._handler)

        self._results = False

        events.EventHandlerContext.removeEventHandlers(eventId=pygame.MOUSEBUTTONDOWN)

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': pygame.BUTTON_RIGHT}))
        events.observeEvents()
        self.assertFalse(self._results, 'Delete all handler from specified eventtype')

        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': pygame.BUTTON_RIGHT}))
        events.observeEvents()
        self.assertTrue(self._results, 'Leave all handler from not specified eventtype')


if __name__ == '__main__':
    unittest.main()
