# package

from threading import Thread

import time

from arguxserver.dao import ITEM_DAO



class TriggerWorker(Thread):

    def run(self):
        while(True):
            # Run once a minute.
            triggers = ITEM_DAO.getAllTriggers()
            for trigger in triggers:
                ITEM_DAO.evaluateTrigger(trigger)
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop() 
            print("THREAD")

