# package

from threading import Thread

import time

from arguxserver.dao import ItemDAO



class TriggerWorker(Thread):

    def run(self):
        while(True):
            # Run once a minute.
            triggers = ItemDAO.get_all_triggers()
            for trigger in triggers:
                ItemDAO.evaluate_trigger(trigger)
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop() 
            print("THREAD")

