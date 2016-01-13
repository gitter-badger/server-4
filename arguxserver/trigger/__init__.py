"""Trigger Module for Worker-Class."""

from threading import (
    Thread
)

import time

from sqlalchemy.orm import (
    sessionmaker
)

from arguxserver.dao import DAO


class TriggerWorker(Thread):

    """
    TriggerWorker class.

    Evaluates all triggers and creates alert objects.
    """

    def __init__(self):
        super(TriggerWorker, self).__init__()
        self.daemon = True

    def run(self):

        Session = sessionmaker()
        session = Session()

        dao = DAO(session)

        """Thread body."""
        while True:

            # Run once a minute.
            triggers = dao.trigger_dao.get_all_triggers()
            for trigger in triggers:
                dao.trigger_dao.evaluate_trigger(trigger)

            session.flush()
            session.commit()
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.stop()

        session.close()
