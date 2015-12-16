"""Trigger Module for Worker-Class."""

from threading import Thread

import time

from arguxserver.dao import ItemDAO



class TriggerWorker(Thread):

    """
    TriggerWorker class.

    Evaluates all triggers and creates alert objects.
    """

    def run(self):
        """Thread body."""
        while True:
            # Run once a minute.
            print("run")
            triggers = ItemDAO.get_all_triggers()
            for trigger in triggers:
                ItemDAO.evaluate_trigger(trigger)
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop()

